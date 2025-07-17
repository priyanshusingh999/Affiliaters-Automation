import requests, random, json, time, pyshorteners, re
from bs4 import BeautifulSoup
from config import Config
from fake_useragent import UserAgent
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is Running!'

def run_flask():
    app.run(host='0.0.0.0', port=8085)

threading.Thread(target=run_flask).start()

# ============================ ⚡ Flipkart Auto-Poster by @priyanshusingh999 ===================================================================

def get_random_flipkart_url():
    with open("flipkart_urls.txt") as f:
        urls = f.readlines()
    return random.choice(urls).strip()

def fetch_soup(url):
    ua = UserAgent()
    header = {'User-Agent': ua.random}
    payload = { 'api_key': {Config.SCRAPER_API_KEY}, 'url': url}

    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"🌐 Attempt {attempt}/{max_attempts} - Fetching URL: {url}")
            response = requests.get('https://api.scraperapi.com/', headers=header, params=payload, timeout=40)
            response.raise_for_status() 
            print("✅ Fetched:", url)
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(5)  # wait 2 seconds before retry
            else:
                print("🚫 All attempts failed.")
                return None

def extract_products(soup):
    products = []
    if not soup:
        return products

    product_divs = soup.find_all('div', class_='tUxRFH') or soup.find_all('div', class_='_1sdMkc LFEi7Z') or soup.find_all('div', class_='slAVV4')
    for product in product_divs:
        name_tag = product.find('div', class_='KzDlHZ') or product.find('div', class_='hCKiGj') or product.find('a', class_='wjcEIp')
        link_tag = product.find('a', class_='CGtC98') or product.find('a', class_='rPDeLR') or product.find('a', class_='wjcEIp')
        img_tag = product.find('img') or product.find('img', class_='_53J4C-') or product.find('img', class_='DByuf4')

        name = name_tag.get_text(strip=True) if name_tag else None
        link = "https://www.flipkart.com" + link_tag['href'] if link_tag and link_tag.get('href') else None
        image = img_tag.get('src') or img_tag.get('data-src') if img_tag else None

        if name and link and image:
            products.append({
                'name': name,
                'link': link,
                'image': image
            })
    return products

def convert_affiliate_link(link):
    print("🔄 Converting link:", link)
    KEY = Config.API_EARNING_KEY
    endpoint = "https://ekaro-api.affiliaters.in/api/converter/public"
    payload = {"deal": link,"convert_option": "convert_only"}
    headers = {"Authorization": f"Bearer {KEY}","Content-Type": "application/json"}

    try:
        res = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        if res.status_code == 200 and res.json().get("success") == 1:
            long_url = res.json()["data"]
            print(long_url)
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(long_url)
            print(short_url)
            return short_url
        print("❌ Affiliate conversion failed:", res.text)
    except Exception as e:
        print("❌ Error in affiliate link:", e)

    return convert_affiliate_link(link)  # fallback original

def post_to_telegram(product, affiliate_link):
    global last_posted_product
    TOKEN = Config.BOT_TOKEN
    CHANNEL_IDS = Config.CHANNEL_ID
    IMAGE_URL = product['image']
    MESSAGE = f"<b>{product['name']}</b>\n\n👉 <b>Check this deal:\n</b> {affiliate_link}"

    for chat_id in CHANNEL_IDS:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        payload = {
            'chat_id': chat_id,
            'photo': IMAGE_URL,
            'caption': MESSAGE,
            'parse_mode': 'HTML'
        }
        try:
            res = requests.post(url, data=payload)
            print(f"✅ Posted to Telegram: {res.json()}")
            last_posted_product = {
                'name': product['name'],
                'link': affiliate_link,
                'image': IMAGE_URL
            }
        except Exception as e:
            print("❌ Telegram Error:", e)

# 📤 Facebook page par post karna
def post_to_facebook(product, affiliate_link):
    global last_posted_product
    PAGE_ID = Config.PAGE_ID
    ACCESS_TOKEN = Config.PAGE_ACCESS_TOKEN
    IMAGE_URL = product['image']
    MESSAGE = f"{product['name']}\n\nCheck out this deal 👉 {affiliate_link}"

    post_url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"

    payload = {
        'url': IMAGE_URL,
        'caption': MESSAGE,
        'access_token': ACCESS_TOKEN
    }

    try:
        response = requests.post(post_url, data=payload)
        data = response.json()
        if "id" in data:
            print(f"✅ Posted to Facebook: https://www.facebook.com/{PAGE_ID}/posts/{data['id']}")
            last_posted_product = {
                'name': product['name'],
                'link': affiliate_link,
                'image': IMAGE_URL
            }
        else:
            print(f"❌ Facebook Post Failed:", data)
    except Exception as e:
        print("❌ Facebook Error:", e)

# 🔁 Final automation loop
def start_loop(interval=3600):  # 600 = 60 mins
    global bot_status
    while True:
        print("🔄 Starting new round...")
        url = get_random_flipkart_url()
        soup = fetch_soup(url)
        products = extract_products(soup)

        if not products:
            print("⚠️ No products found, trying next...")
            time.sleep(5)
            continue

        product = random.choice(products)
        affiliate_link = convert_affiliate_link(product['link'])

        # Post to Telegram & Facebook
        post_to_telegram(product, affiliate_link)
        post_to_facebook(product, affiliate_link)

        print(f"⏳ Sleeping for {interval} seconds...\n")
        bot_status = f"Last posted: {product['name']}"
        time.sleep(interval)

if __name__ == '__main__':
    app.run(start_loop(3600))  # 60-minute loop