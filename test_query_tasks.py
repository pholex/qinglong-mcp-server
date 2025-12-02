#!/usr/bin/env python3
import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

QINGLONG_URL = os.getenv("QINGLONG_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    if not all([QINGLONG_URL, CLIENT_ID, CLIENT_SECRET]):
        print("错误: 请在 .env 文件中配置 QINGLONG_URL, CLIENT_ID, CLIENT_SECRET")
        return None
    try:
        url = f"{QINGLONG_URL}/open/auth/token"
        params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        return result["data"]["token"] if result.get("code") == 200 else None
    except Exception as e:
        print(f"获取 token 失败: {e}")
        return None

def get_crons(token):
    try:
        url = f"{QINGLONG_URL}/open/crons"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=10)
        result = response.json()
        return result["data"] if result.get("code") == 200 else None
    except Exception as e:
        print(f"获取任务列表失败: {e}")
        return None

token = get_token()
if token:
    result = get_crons(token)
    if result:
        crons = result.get("data", [])
        crons.sort(key=lambda x: x.get('id', 0))
        print(f"青龙面板: {QINGLONG_URL}")
        print(f"共 {result.get('total', 0)} 个任务:\n")
        for cron in crons:
            print(f"ID: {cron.get('id')}")
            print(f"名称: {cron.get('name')}")
            print(f"命令: {cron.get('command')}")
            print(f"定时: {cron.get('schedule')}")
            print(f"状态: {'启用' if cron.get('isDisabled') == 0 else '禁用'}")
            print("-" * 50)
    else:
        print("获取任务列表失败")
        sys.exit(1)
else:
    sys.exit(1)
