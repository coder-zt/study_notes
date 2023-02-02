from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

class FetchArticleDirver():
    
    # 初始化chrome浏览器，设置下载路径、SingleFile插件路径
    def init(self, mouser, downloadPath, rcxPath):
        self.downloadPath = downloadPath
        if not os.path.exists(downloadPath):
            print("下载目录不存在，创建下载目录")
            os.mkdir(downloadPath)
        self.mouser = mouser
        options = webdriver.ChromeOptions()
        options.add_extension(rcxPath)
        # 设置下载路径
        dir_prefs = {'profile.default_content_settings.popups':0,
                    'download.default_directory':self.downloadPath}
        options.add_experimental_option('prefs', dir_prefs)
        self.dirver = webdriver.Chrome(options=options)
    
    # 加载链接
    def loadUrl(self, url):
        self.dirver.get(url)
      
    # 判断元素是否存在  
    def isElementExist(self, xpath):
        try:
            self.dirver.find_element(By.XPATH, xpath)
            return True
        except:
            return False
        
    # 获取当前下载目录下文件数量
    def getCurrentFileCount(self):
        if os.path.exists(self.downloadPath):
            return len(os.listdir(self.downloadPath))
        else:
            print("下载目录不存在")
            return 0
        
    # 下载当前网页数据
    def fetchCurrentPage(self):
        count = self.getCurrentFileCount()
        print("当前下载目录文件数量：" + str(count))
        # 点击下载按钮
        self.mouser.click(1104,115)
        self.mouser.clickRelative(-180,125)
        while True:
            newCount = self.getCurrentFileCount()
            
            if newCount != count:
                print("文件为下载完成，退出 ===> " + str(newCount))
                break
            print("文件下载未完成，等待5s ===> " + str(newCount))
            time.sleep(5)
            
    # 下载一个集合url
    def fetchArticleList(self, urlList, existElementXpath):
        for url in urlList:
            self.loadUrl(url)
            # 判断网页数据是否加载结束
            while not self.isElementExist(existElementXpath):
                print("判断加载完成元素不存在")
            self.fetchCurrentPage()