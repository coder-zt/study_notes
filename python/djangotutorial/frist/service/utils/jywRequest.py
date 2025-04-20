import fake_useragent

from curl_cffi import requests
from loguru import logger
import base64
import json
import time
from . import latexVerify as latex
from . import proxyUtils

output_path = "/Users/edy/owner/study_notes/python/djangotutorial/frist/img/"
mobileCaptchaUrl = "https://api.jyeoo.com/api/MobileCaptcha"
captchaImgBaseUrl = "https://api.jyeoo.com/api/CaptchaImg?h=60&w=150&id="


def requestCode(number, uuid, tryCount=1):
    proxyUtils.switchProxy()

    target_url = captchaImgBaseUrl + uuid

    ua = fake_useragent.UserAgent()

    ses = requests.Session(impersonate="chrome124")
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": ua.chrome,
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
        }

        index = 1
        while True:
            captchaImgRes = ses.get(
                target_url,
                proxies=proxyUtils.proxies,
                headers=headers,
                verify=False,
                timeout=5,
                allow_redirects=True,
            )
            # print(captchaImgRes.json()["D"])
            imgBase64 = captchaImgRes.json()["D"]
            image_data = base64.b64decode(imgBase64)
            imgPath = (
                output_path + str(tryCount) + "_" + str(index) + "_" + uuid + ".png"
            )
            with open(imgPath, "wb") as f:
                f.write(image_data)
            print("开始请求ocr识别验证码...")
            value = latex.getAnwer(imgPath)
            index = index + 1
            dictV = {"m": number, "t": 1, "v": str(value), "id": uuid}
            print(dictV)
            response = ses.post(
                mobileCaptchaUrl,
                data=dictV,
                proxies=proxyUtils.proxies,
                headers=headers,
                verify=False,
                timeout=5,
                allow_redirects=True,
            )
            content = response.content.decode()

            print("发送验证码结束！====> " + content)
            if "致电客服" in content:
                # ip被封,尝试切换ip
                print("ip被封,尝试切换ip")
                return requestCode(number, uuid, tryCount + 1)
            elif "（010）" not in content:
                return content
            else:
                print("验证码错误！等待 3s后重试")
                time.sleep(3)

    except requests.RequestsError as e:
        # end = time.time()
        # time_cost = end - begin
        # 请求异常，切换IP，重新请求
        logger.error(f" RequestsError 异常: {e}")
        proxyUtils.switchProxy()
        return requestCode(number, uuid, tryCount + 1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # end = time.time()
        # time_cost = end - begin
        # incr_cnt("other_err")
        logger.error(f" Exception 异常: {e}")
        proxyUtils.switchProxy()
        return requestCode(number, uuid, tryCount + 1)
    finally:
        pass


def fetchData(method, url, requestHeaders, requestBody):
    print("fetchData url: " + url)
    target_url = url

    ua = fake_useragent.UserAgent()

    ses = requests.Session(impersonate="chrome124")
    # try:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": ua.chrome,
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
    }
    headers.update(requestHeaders)
    headers["User-Agent"] = ua.chrome
    print(headers)
    res = {}
    try:
        if method.lower() == "get":
            res = ses.get(
                target_url,
                data=requestBody,
                proxies=proxyUtils.proxies,
                headers=headers,
                verify=False,
                timeout=5,
                allow_redirects=True,
            )
        elif method.lower() == "post" :
            res = ses.post(
                target_url,
                data=requestBody,
                proxies=proxyUtils.proxies,
                headers=headers,
                verify=False,
                timeout=5,
                allow_redirects=True,
            )
        print("headers ====> ", end="")
        
        headers_dict = dict(res.headers)
        print(headers_dict)
        # headers_json = json.dumps(headers_dict,  indent=2)
        # print(headers_json)
        res = res.content.decode()
    except Exception as e:
        print(e)
        eStr = str(e)
        if "SSL_ERROR_SYSCALL" in eStr:  # ssl连接失败切换ip
            proxyUtils.switchProxy()
            return fetchData(method, url, requestHeaders, requestBody)
        res = "系统错误，请与客服联系。"
    return res,headers_dict


if __name__ == "__main__":
   print( "POST".lower())