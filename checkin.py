# Install the Python Requests library:
# `pip install requests dotenv`

import requests
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

def get_auth_token():
    try:
        captchaImage = requests.get(
            url="https://xiaobei.yinghuaonline.com/prod-api/captchaImage",
            headers={
                "User-Agent": "P40Pro(Harmony/2.0Beta) (uni.UNIA68F45B) UniApp/0.28.0 1440x2432",
            },
        ).json()
        code = captchaImage['showCode']
        uuid = captchaImage['uuid']
        username = config["USERNAME"]
        password = config["PASSWORD"]
        response = requests.post(
            url="https://xiaobei.yinghuaonline.com/prod-api/login",
            headers={
                "User-Agent": "P40Pro(Harmony/2.0Beta) (uni.UNIA68F45B) UniApp/0.28.0 1440x2432",
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "username": username,
                "password": password,
                "code": code,
                "uuid": uuid
            })
        )
        return response.json()["token"]
    except requests.exceptions.RequestException:
        print('Get Token Failed.')


def checkin_request():
    token = get_auth_token()
    if not token:
        return
    try:
        response = requests.post(
            url="https://xiaobei.yinghuaonline.com/prod-api/student/health",
            headers={
                "User-Agent": "P40Pro(Harmony/2.0Beta) (uni.UNIA68F45B) UniApp/0.28.0 1440x2432",
                "Authorization": "Bearer "+ token,
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "location": config["LOCATION"],
                "dangerousRegion": "2",
                "goOutRemark": "",
                "dangerousRegionRemark": "",
                "remark": "",
                "goOut": "1",
                "familySituation": "1",
                "temperature": "36",
                "healthState": "1",
                "coordinates": config["COORDINATES"],
                "contactSituation": "2"
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.json()["msg"]))
        return True
    except requests.exceptions.RequestException:
        print('Checkin failed')
        return False
