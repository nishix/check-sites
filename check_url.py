from datetime import datetime
import os
from dotenv import load_dotenv
import pytz
import ssl
import socket
import requests
import logging

# .env ファイルから環境変数を読み込む
load_dotenv()

# 環境変数の取得
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_NOTIFY_API = os.getenv("LINE_NOTIFY_API")
MONITOR_SITES = os.getenv("MONITOR_SITES").split(',')
SSL_EXPIRY_DAYS = int(os.getenv("SSL_EXPIRY_DAYS"))

# ロギング設定
logging.basicConfig(level=logging.INFO, filename='monitoring.log')

# LINEにメッセージを送る関数
def send_line_message(message):
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    payload = {"message": message}
    requests.post(LINE_NOTIFY_API, headers=headers, data=payload)

# SSL証明書の残り日数を取得
def get_remaining_days(hostname):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                               server_hostname=hostname)
    conn.connect((hostname, 443))
    cert = conn.getpeercert()
    not_after = datetime.strptime(cert['notAfter'], r"%b %d %H:%M:%S %Y %Z").replace(tzinfo=pytz.UTC)
    tz = pytz.timezone('Asia/Tokyo')
    now_aware = datetime.now().astimezone(tz)
    remaining = (not_after.astimezone(tz) - now_aware).days
    conn.close()
    return remaining

# サイトをチェックする関数
def check_sites():
    for site in MONITOR_SITES:
        try:
            # ステータスコードのチェック
            response = requests.get(f"https://{site}")
            if response.status_code != 200:
                send_line_message(f"Status code error: {site} returned {response.status_code}")
                logging.error(f"{datetime.now()} - Status code error: {site} returned {response.status_code}")
            
            # SSL証明書の有効期限をチェック
            remaining = get_remaining_days(site)
            if remaining <= SSL_EXPIRY_DAYS:
                send_line_message(f"SSL certificate alert: {site} will expire in {remaining} days")
                logging.warning(f"{datetime.now()} - SSL certificate alert: {site} will expire in {remaining} days")
                
        except Exception as e:
            send_line_message(f"An error occurred with {site}: {str(e)}")
            logging.error(f"{datetime.now()} - An error occurred with {site}: {str(e)}")

if __name__ == "__main__":
    check_sites()

