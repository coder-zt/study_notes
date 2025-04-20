from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from selenium.common.exceptions import WebDriverException

# 保存 Cookie 到文件
def save_cookies(driver, path):
    with open(path, 'w') as file:
        json.dump(driver.get_cookies(), file)

# 加载 Cookie 文件
def load_cookies(driver, path):
    driver.get("https://www.zhixue.com/")  # 必须先访问域名
    if not os.path.exists(path):
        return
    with open(path, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()  # 刷新页面应用 Cookie
 
 
def decodeStr(content):
    key = "7490697619632FCDA815BB4F424D550B"  # 原始密钥
    # 处理密钥（根据 CryptoJS 的行为，短密钥会用 MD5 哈希扩展）
    # 生成 16 字节（AES-128）的密钥
    key_bytes = key.encode("utf-8")
    if len(key_bytes) < 16:
        # 如果密钥长度不足，用 MD5 哈希扩展（类似 CryptoJS 的默认行为）
        from hashlib import md5
        key_bytes = md5(key_bytes).digest()

    # 创建 AES-ECB 解密器
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    # 解密（假设 content 是 Base64 编码字符串）
    try:
        # 如果是 Base64 编码的密文
        ciphertext = base64.b64decode(content)
        # 解密并去除 PKCS7 填充
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        # 转换为 UTF-8 字符串
        # 转换为 UTF-8 字符串
        res = decrypted.decode("utf-8")
        # print(res)
        return json.loads(res)
    except Exception as e:
        print("解密失败:", e)
  
 
# 配置代理
PROXY = "127.0.0.1:7890"  # 替换为你的代理IP和端口

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={PROXY}')

caps = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',
    'goog:loggingPrefs': {'performance': 'ALL'},   # 记录性能日志
    'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}  # 无界面模式
}

driverPath = "/Users/edy/owner/tools/chromedriver-mac-arm64/chromedriver"

driver = webdriver.Chrome(service=Service(driverPath),options=chrome_options, desired_capabilities=caps)


# 开始监听网络请求
driver.execute_cdp_cmd("Network.enable", {})

load_cookies(driver, "cookies.json")

driver.get("https://www.zhixue.com/")  # 打开百度
print("当前页面标题:", driver.title)  # 打印标题验证

input("按回车结束...")  # 保持浏览器打开（可选）


logs = driver.get_log("performance")
for item in logs:
    try:
        log = json.loads(item["message"])["message"]
        # if "Network.response" in log["method"] or "Network.request" in log["method"] or "Network.webSocket" in log["method"]:
            # pprint(log)
        if log["method"] == 'Network.responseReceived':
            url = log['params']['response']['url']
            if not ('getList4QualityLib' in url or 'getNewestList4QualityLib' in url) :  # 过滤掉初始data页面，后续可以根据 log['params']['response']['type']过滤请求类型
                continue
            print('请求', url)
            request_id = log['params']['requestId']

            # request_headers = log['params']['response']['headers']
            # response_headers = log['params']['response']['headers']
            # response_time = log['params']['response']['responseTime']
            # status_code = log['params']['response']['status']

            try:
                request_data = driver.execute_cdp_cmd('Network.getRequestPostData', {'requestId': request_id})
            except WebDriverException:  # 没有后台数据获取时会有异常
                request_data = None

            try:
                response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body']
                if 'getList4QualityLib' in url or 'getNewestList4QualityLib' in url:
                    print('响应')
                    print('响应',  decodeStr(response_body.replace('"','')))
                   
            except WebDriverException:  # 没有后台数据获取时会有异常
                response_body = None
    except:
        pass
        
save_cookies(driver, "cookies.json")     
driver.quit()  # 关闭浏览器
# tch6888724
# hwof026