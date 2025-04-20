# from django.shortcuts import render
from django.http import JsonResponse
import warnings
from .utils import jywRequest
import json


warnings.filterwarnings("ignore")


def requestCode(request, phone, uuid):
    res = jywRequest.requestCode(phone, uuid)
    return JsonResponse({"message": str(res), "headers":{}})


def fetchData(request):
    reqBody = json.loads(request.body)
    # print(reqBody)
    url = reqBody["url"]
    method = reqBody["method"]
    headers = {}
    body = {}
    if "body" in reqBody:
        body = reqBody["body"]
    if "headers" in reqBody:
        headers = reqBody["headers"]
    res, headers = jywRequest.fetchData(method, url, headers, body)
    # res = ""
    print(res)
    if "系统错误，请与客服联系。" in res:
        return JsonResponse({"message": "目标网站：系统错误，请与客服联系。"})
    elif len(res) == 0:
        return JsonResponse({"message": "数据为空"})
    return JsonResponse({"message": json.loads(res), "headers":headers})
