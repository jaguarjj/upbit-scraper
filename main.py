import requests
from bs4 import BeautifulSoup
import os

# Your Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = "8380060432:AAEa5FfT_R7F7z_rIWIOBf9e6zoCcXvAAqM"
TELEGRAM_CHAT_ID = "1131407913"

# URL of the Upbit Korean-language announcements page
UPBIT_NOTICE_URL = "https://upbit.com/service_center/notice"

# Keywords to look for new listings in Korean
LISTING_KEYWORDS = ["신규 거래 페어", "상장", "마켓 디지털 자산 추가", "신규 거래지원 안내"]

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")

def get_latest_listing():
    """Fetches the title of the latest Upbit listing announcement."""
    try:
        response = requests.get(UPBIT_NOTICE_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Upbit page: {e}")
        return None, None
    
    soup = BeautifulSoup(response.content, "html.parser")
    listing_element = soup.select_one('div.b-notice.table-body > a.notice-item-wrap > span.tit')
    
    if listing_element:
        title = listing_element.get_text().strip()
        href_value = listing_element.parent.get('href')
        
        if href_value:
            announcement_url = "https://upbit.com" + str(href_value)
            return title, announcement_url
    
    return None, None

if __name__ == "__main__":
    latest_title, latest_url = get_latest_listing()

    if latest_title and any(keyword in latest_title for keyword in LISTING_KEYWORDS):
        message = f"🚨 New Upbit Listing Alert! 🚨\n\nTitle: {latest_title}\nURL: {latest_url}"
        send_telegram_message(message)
    else:
        print("No new listing found.")
