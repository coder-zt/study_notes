      
# -*- coding: utf-8 -*-

import threading

from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import warnings
import fake_useragent
# import requests
from curl_cffi import requests
from loguru import logger

warnings.filterwarnings("ignore")

total_time_cost = 0
total_time_cost_timeout = 0
timings = []


def add_to_total_time_cost(time_cost):
    lock.acquire()
    global total_time_cost
    global timings

    timings.append(time_cost)
    total_time_cost += time_cost
    lock.release()


def add_to_total_time_cost_timeout(time_cost):
    lock.acquire()
    global total_time_cost_timeout
    total_time_cost_timeout += time_cost
    lock.release()


def do_request(idx):
    incr_cnt("task")
    incr_tasking()

    proxy_server = f"http://H31335518696Z2RC:179B7DDBE85E81FD@http-cla.abuyun.com:9030"
    proxies = {
        "http": proxy_server,
        "https": proxy_server
    }

    begin = time.time()
    ses = requests.Session(impersonate="chrome124")
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'User-Agent': ua.chrome,
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        response = ses.get(
            target_url,
            proxies=proxies,
            headers=headers,
            verify=False,
            timeout=timeout,
            allow_redirects=True,

        )
        print(response.json())
        req_end = time.time()
        content_size = len(response.content)
        time_cost = req_end - begin

        # if time_cost > 2.1:
        #     raise requests.Timeout("timeout")

        add_to_total_time_cost(time_cost)
        if response.status_code == 200:
            logger.info(
                f"{idx} {response.status_code} 请求耗时：{time_cost: .2f} content_size：{content_size} ")
            incr_cnt("succ")
        else:
            logger.warning(
                f"{idx}  状态码异常: {response.status_code} 请求耗时：{time_cost: .2f} content_size：{content_size}")
            incr_cnt("status_err")

    except requests.RequestsError as e:
        end = time.time()
        time_cost = end - begin
        logger.error(f"{idx} 异常: {e} 耗时： {time_cost: .2f}")

        incr_cnt("time_out")
        # send_request_and_measure_time(time_cost, True)
        add_to_total_time_cost_timeout(time_cost)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        end = time.time()
        time_cost = end - begin
        incr_cnt("other_err")
        logger.error(f"{idx} 异常: {e} 耗时： {time_cost: .2f}")
    finally:
        decr_tasking()


def run_concurrent_requests(concurrent_requests, test_count):
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        # 开始计时
        start = time.time()

        # 启动并发请求
        for idx in req_generator():
            if idx <= test_count:
                executor.submit(do_request, idx).add_done_callback(thread_pool_callback)
            else:
                break

        # 等待所有请求完成
        executor.shutdown(wait=True)

        end = time.time()
        cost = end - start
        logger.info(
            f"task count: {task_count} succ count: {succ_count} succ rate: {succ_count * 100 / task_count : .2f}% cost: {cost: .2f}")


def thread_pool_callback(worker):
    e = worker.exception()
    if e:
        logger.error("Worker return exception: {}".format(e))


def incr_cnt(type: str, code: int = 0):
    lock.acquire()
    if type == "succ":
        global succ_count
        succ_count += 1
    elif type == "time_out":
        global time_out_cnt
        time_out_cnt += 1
    elif type == "other_err":
        global other_err_cnt
        other_err_cnt += 1
    elif type == "status_err":
        global status_err_cnt
        status_err_cnt += 1
    else:
        global task_count
        task_count += 1
    lock.release()


tasking = 0


def get_tasking():
    lock.acquire()
    global tasking
    ret = tasking
    lock.release()
    return ret


def incr_tasking():
    lock.acquire()
    global tasking
    tasking += 1
    lock.release()


def decr_tasking():
    lock.acquire()
    global tasking
    tasking -= 1
    lock.release()


def print_result():
    time_cost = time.time() - bg_time
    avg_time_cost = time_cost * concurrent_requests / succ_count if succ_count > 0 else 0
    start_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("-" * 50, "测试参数", "-" * 50)
    print("目标网址: ", target_url)
    print("请求库: ", "requests")
    print(f"开始时间: {start_time} 结束时间: {end_time} 耗时: {time_cost} 并发数: {concurrent_requests} 次数: {test_count} 成功次数: {succ_count} 超时时间: {timeout}秒")
    print(f"请求平均耗时: {avg_time_cost : .2f}s ({time_cost * concurrent_requests: .2f} / {succ_count})", )
    print("-" * 50)
    print("-" * 50, "测试结果", "-" * 50)
    print("-" * 50)
    print(f"总数: {task_count}次 成功: {succ_count}次 成功率: {succ_count * 100 / task_count: .2f}%")
    print("-" * 50, "错误详情", "-" * 50)
    print(f"超时错误: {time_out_cnt} 次  比例: {time_out_cnt * 100 / task_count: .2f}%")
    print(f"状态码异常: {status_err_cnt} 次  比例: {status_err_cnt * 100 / task_count: .2f}%")

    print(f"其他错误: {other_err_cnt}次  比例: {other_err_cnt * 100 / task_count : .2f}%")
    print("-" * 50)


task_count = 0  # 请求总次数
succ_count = 0  # 成功数
time_out_cnt = 0  # 超时
other_err_cnt = 0  # 其他错误
status_err_cnt = 0  # 状态码异常
curl_errs_cnt = {}

lock = threading.Lock()  # 锁

timeout = 5
# 超时时间
concurrent_requests = 1 #并发数
#duration_seconds = 180  # 持续时间
test_count = 5
target_url = "https://api.jyeoo.com/api/CaptchaImg?h=60&id=66b7f034-44b6-4f4f-ade1-b80b2e043c8a&w=150"
ua = fake_useragent.UserAgent()

current_time = datetime.datetime.now()
bg_time = time.time()

def req_generator():
    last = None
    idx = 0
    cnt = 0

    while True:
        if get_tasking() >= concurrent_requests:
            time.sleep(0.1)
            continue

        now = int(time.time())
        if now != last:
            cnt = 0
            idx += 1
            yield idx
        else:
            cnt += 1
            if cnt >= concurrent_requests:
                if now + 1 - time.time() > 0:
                    time.sleep(now + 1 - time.time())
                continue
            else:
                idx += 1
                yield idx

        last = now


if __name__ == "__main__":
    try:
        run_concurrent_requests(concurrent_requests, test_count)
    except KeyboardInterrupt as e:
        print("手动终止!")
    finally:
        print_result()
        exit(0)


    
    