import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

CHANNEL = "ShadeganHava"
URL = f"https://eitaa.com/{CHANNEL}"
OUTPUT = "posts.json"

def scrape():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fa-IR,fa;q=0.9",
    }

    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.select(".etme_widget_message_wrap")

    results = []
    for post in posts[-5:]:  # ۵ پست آخر
        text_el = post.select_one(".etme_widget_message_text")
        time_el = post.select_one(".etme_widget_message_date time")
        link_el = post.select_one(".etme_widget_message_date")

        if not text_el:
            continue

        # استخراج متن ساده (بدون تگ HTML)
        text = text_el.get_text(separator="\n", strip=True)

        # تاریخ
        dt_iso = time_el.get("datetime") if time_el else None
        if dt_iso:
            try:
                dt = datetime.fromisoformat(dt_iso.replace("Z", "+00:00"))
                dt_fa = dt.astimezone(timezone.utc).strftime("%Y/%m/%d - %H:%M")
            except Exception:
                dt_fa = dt_iso
        else:
            dt_fa = ""

        # لینک پست
        href = link_el.get("href") if link_el else ""
        post_link = f"https://eitaa.com{href}" if href else URL

        results.append({
            "text": text,
            "date": dt_fa,
            "link": post_link,
        })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(results)} پست ذخیره شد")

if __name__ == "__main__":
    scrape()
