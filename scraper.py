import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_slowand():
    # 抓取 Slowand 台灣官網新進商品頁面
    url = "https://m.tw.slowand.com/product/list.html?cate_no=24"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        products = []
        
        # 定位商品容器
        items = soup.select('ul.prdList > li')

        for item in items:
            try:
                name_tag = item.select_one('.description strong.name a')
                if not name_tag: continue
                
                # 價格解析
                price_tag = item.select_one('.description .xans-record- span[style*="font-size:12px"]')
                price_str = price_tag.text.replace('TWD', '').replace('NT$', '').replace(',', '').strip()
                
                # 圖片與連結
                img_tag = item.select_one('.thumbnail img')
                img_url = "https:" + img_tag['src'] if img_tag['src'].startswith('//') else img_tag['src']
                link = "https://m.tw.slowand.com" + name_tag['href']
                
                products.append({
                    "store": "Slowand",
                    "name": name_tag.text.strip(),
                    "price": int(float(price_str)),
                    "img": img_url,
                    "url": link,
                    "is_new": True
                })
            except:
                continue
        return products
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    data = scrape_slowand()
    if data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"成功抓取 {len(data)} 件商品")
