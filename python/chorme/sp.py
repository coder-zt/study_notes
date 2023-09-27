from WebDriver import FetchArticleDirver
from Mouser import Mouser


dirver = FetchArticleDirver()
dirver.init(Mouser(), '/Users/edy/owner', "python/chorme/assets/1.21.38_0.crx")
urlList = ["https://juejin.cn/post/7190550643386351653", "https://juejin.cn/post/7178818904620269624"]
dirver.fetchArticleList(urlList, '//*[@id="juejin"]/div[1]/main/div/div[1]/article/h1')
