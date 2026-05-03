import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_slowand():
    url = "https://m.tw.slowand.com/category/all/24/"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/104.1'}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        products = []
        # 針對 Slowand 的 HTML 結構抓取
        items = soup.select('.prdList > li')
        for item in items:
            name_tag = item.select_one('.description .name a')
            price_tag = item.select_one('.description .xans-record- .price')
            img_tag = item.select_one('.thumbnail img')
            
            if name_tag and price_tag:
                name = name_tag.text.strip()
                price = int(price_tag.text.replace('TWD', '').replace('NT$', '').replace(',', '').split('.')[0].strip())
                img = "https:" + img_tag['src'] if img_tag['src'].startswith('//') else img_tag['src']
                link = "https://m.tw.slowand.com" + name_tag['href']
                
                products.append({
                    "store": "Slowand",
                    "name": name,
                    "price": price,
                    "old_price": price + 100, # 測試模擬降價用，實際應比對資料庫
                    "img": img,
                    "url": link,
                    "is_new": "NEW" in item.text,
                    "stock": "Out of Stock" if "품절" in item.text or "售罄" in item.text else "In Stock"
                })
        return products
    except Exception as e:
        print(f"Slowand 抓取失敗: {e}")
        return []

if __name__ == "__main__":
    print("啟動自動監控...")
    data = scrape_slowand()
    # 這裡可以持續加入 Blackup 的抓取函數
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"同步完成，共抓取 {len(data)} 件商品。")
