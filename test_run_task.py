#!/usr/bin/env python3
import os
import sys
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

# 与 server.py 统一的 .env 加载逻辑
env_paths = [
    Path.cwd() / ".env",
    Path.home() / ".qinglong-mcp" / ".env",
    Path(__file__).parent / ".env",
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break

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


def run_task_and_fetch_log(token: str, task_id: int) -> int:
    headers = {"Authorization": f"Bearer {token}"}

    # 启动任务
    try:
        run_url = f"{QINGLONG_URL}/open/crons/run"
        resp = requests.put(run_url, headers=headers, json=[task_id], timeout=10)
        result = resp.json()
        if result.get("code") != 200:
            print(f"启动任务失败: {result}")
            return 1
        print(f"任务 {task_id} 已启动，开始轮询日志...")
    except Exception as e:
        print(f"启动任务失败: {e}")
        return 1

    # 轮询日志（最多约30秒）
    time.sleep(2)
    for _ in range(6):
        time.sleep(5)
        try:
            log_url = f"{QINGLONG_URL}/open/crons/{task_id}/log"
            log_resp = requests.get(log_url, headers=headers, timeout=10)
            log_result = log_resp.json()
            
            if log_result.get("code") == 200:
                log_content = log_result.get("data", "")
                if "执行结束" in log_content:
                    print("===== 执行日志 =====")
                    print(log_content if log_content else "(无日志内容)")
                    return 0
        except Exception as e:
            print(f"检查任务异常: {e}")
            break
    
    # 超时或异常
    print(f"任务 {task_id} 超时（30秒）或获取日志失败")
    return 0


def main():
    if len(sys.argv) < 2:
        print("用法: python3 run_task.py <任务ID>")
        sys.exit(1)
    try:
        task_id = int(sys.argv[1])
    except ValueError:
        print("错误: 任务ID必须是整数")
        sys.exit(1)

    token = get_token()
    if not token:
        sys.exit(1)
    exit_code = run_task_and_fetch_log(token, task_id)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

