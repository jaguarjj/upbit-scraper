from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Your Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = "8380060432:AAEa5FfT_R7F7z_rIWIOBf9e6zoCcXvAAqM"
TELEGRAM_CHAT_ID = "1131407913"

# URL of the Upbit Korean-language announcements page
UPBIT_NOTICE_URL = "https://upbit.com/service_center/notice"

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

@app.route('/check-upbit', methods=['GET'])
def check_for_new_listings():
    """Checks the Upbit page for new listing announcements."""
    print("Checking for new Upbit listings...")

    try:
        response = requests.get(UPBIT_NOTICE_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching Upbit page: {e}"

    soup = BeautifulSoup(response.content, "html.parser")

    # Use a more specific selector to target only the announcement titles within the table
    listing_element = soup.select_one('div.b-notice.table-body > a.notice-item-wrap > span.tit')

    if listing_element and listing_element.parent:
        href_value = listing_element.parent.get('href')

        if href_value:
            title = listing_element.get_text().strip()
            announcement_url = "https://upbit.com" + str(href_value)  

            # Check for keywords related to a new listing
            if any(keyword in title for keyword in ["신규 거래 페어", "상장", "마켓 디지털 자산 추가", "신규 거래지원 안내"]):
                message = f"🚨 New Upbit Listing Alert! 🚨\n\nTitle: {title}\nURL: {announcement_url}"
                send_telegram_message(message)
                return "New listing found and notified."

    return "No new listings found."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)