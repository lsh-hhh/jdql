import hashlib
import hmac
import json
import time

JD_API_HOST = 'https://api.m.jd.com/'


def task_url(function_id, body, cookie):
    now = int(time.time() * 1000)
    key = '12aea658f76e453faf803d15c40a72e0'.encode("utf-8")
    message = 'lite-android&' + json.dumps(body) + '&android&3.1.0&' + function_id + '&' + now.__str__() + '&846c4c32dae910ef'
    message = message.encode("utf-8")
    param_sign = hmac.new(key=key, msg=message, digestmod=hashlib.sha256).hexdigest()
    url = JD_API_HOST + 'api?functionId=' + function_id + '&body=' + json.dumps(body) + '&appid=lite-android&client=android&uuid=846c4c32dae910ef&clientVersion=3.1.0&t=' + now.__str__() + '&sign=' + param_sign
    headers = {
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'accept': '*/*',
        'accept-language': 'RN',
        'kernelplatform': 'zh-Hans-CN;q=1, ja-CN;q=0.9',
        'user-agent': 'JDMobileLite/3.1.0 (iPad; iOS 14.4; Scale/2.00)'
    }
    return url, headers


def task_get_url(function_id, request_body, cookie):
    url = f'https://api.m.jd.com/?appid=activities_platform&functionId={function_id}&body={(json.dumps(request_body)).encode().hex()}&t={int(time.time() * 1000)}'
    headers = {
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'user-agent': "jdltapp;iPad;3.1.0;14.4;network/wifi;Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        'Accept-Language': 'zh-Hans-CN;q=1,en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': "application/x-www-form-urlencoded",
        "referer": "https://an.jd.com/babelDiy/Zeus/q1eB6WUB8oC4eH1BsCLWvQakVsX/index.html"
    }
    return url, headers


if __name__ == '__main__':
    pass
