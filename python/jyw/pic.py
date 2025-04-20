
import requests
import json
import re

SIMPLETEX_UAT="P4FIUDl3rMGShrIkHDVMGWlKLLS7LLQXKSiU0PkixHouTnSMSK5DjXmkvLBVNN8o"

def getAnwer(index):
    # api_url="https://server.simpletex.cn/api/latex_ocr_turbo"  # 接口地址
    api_url="https://server.simpletex.cn/api/latex_ocr"  # 接口地址
    data = { } # 请求参数数据（非文件型参数），视情况填入，可以参考各个接口的参数说明
    header={ "token": SIMPLETEX_UAT } # 鉴权信息，此处使用UAT方式
    file=[("file",("test.png",open("/Users/edy/owner/study_notes/python/djangotutorial/frist/img/1_" + str(index) + "_.png", 'rb')))] # 请求文件,字段名一般为file
    res = requests.post(api_url, files=file, data=data, headers=header) # 使用requests库上传文件
    # print(res.text) # 打印识别结果
    latexStr = json.loads(res.text)["res"]["latex"]
    # latexStr = "$3+6=5+2$"
    # print(latexStr) # 打印识别结果
    numbers = re.findall("\d", latexStr)
    # print(numbers)
    operator = re.findall("[-+]", latexStr)
    # print(latex2latex(latexStr))
    # res = solving(latexStr)
    if len(numbers) == 0:
        return 1
    countRes = int(numbers[0])
    # print(countRes)
    for n in numbers[1:]:
        if len(operator) > 0:
            if operator.pop(0) == "+" :
                print("+++" + n)
                countRes = countRes + int(n)   
            else:
                print("---" + n)
                countRes = countRes - int(n)   
        
    # print(countRes)
    return countRes
# # pip install latex2sympy2 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


for i in range(1, 10):
    print(str(i) + "=====> " + str(getAnwer(i)))