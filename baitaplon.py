import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import schedule
import time

def crawl_baochinhphu_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Tiêu đề
    title = soup.find("h1").text.strip() if soup.find("h1") else ""

    # Mô tả từ meta
    description_tag = soup.find("meta", {"name": "description"})
    description = description_tag["content"].strip() if description_tag else ""

    # Hình ảnh chính
    image_tag = soup.find("meta", property="og:image")
    image_url = image_tag["content"].strip() if image_tag else ""

    # Nội dung bài viết
    content_div = soup.find("div", class_="detail__content")
    if content_div:
        paragraphs = content_div.find_all(["p", "h2"])
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)
    else:
        content = ""

    # Kết quả
    return {
        "Tiêu đề": title,
        "Mô tả": description,
        "Hình ảnh": image_url,
        "Nội dung": content,
        "URL": url
    }

# Hàm để chạy script và lưu dữ liệu
def run_scraper():
    url = "https://baochinhphu.vn/chinh-phu-thong-qua-ho-so-de-an-sap-xep-don-vi-hanh-chinh-cap-tinh-xa-nam-2025-10225051019423613.htm"
    print(f"🔎 Đang thu thập dữ liệu từ:\n{url}")
    
    try:
        article = crawl_baochinhphu_article(url)
        df = pd.DataFrame([article])
        filename = f"baochinhphu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')  # Lưu file Excel
        print(f"📁 Đã lưu thành công vào file Excel: {filename}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

# Set lịch chạy vào lúc 6h sáng hàng ngày
schedule.every().day.at("06:00").do(run_scraper)

# Giữ chương trình chạy liên tục
if __name__ == "__main__":
    print("🔄 Chạy lịch thu thập dữ liệu hàng ngày lúc 6h sáng...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Kiểm tra mỗi phút
