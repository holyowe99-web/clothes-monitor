import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_slowand():
    # 抓取 Slowand 台灣官網新進商品頁面
    url = "https://m.tw.slowand.com/product/list.html?cate_no=24"
    
    # 模擬真人瀏覽器，防止被偵測為機器人
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        print(f"--- 開始連線: {url} ---")
        res = requests.get(url, headers=headers, timeout=30)
        res.encoding = 'utf-8'
        
        if res.status_code != 200:
            print(f"❌ 連線失敗，狀態碼: {res.status_code}")
            return []

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 定位商品容器 (Slowand 台灣版常見結構)
        items = soup.select('ul.prdList > li')
        print(f"DEBUG: 在頁面中找到了 {len(items)} 個潛在商品項目")

        products = []
        for i, item in enumerate(items):
            try:
                # 抓取名稱
                name_tag = item.select_one('.description .name a') or item.select_one('strong.name a')
                if not name_tag: continue
                
                # 抓取價格
                price_tag = item.select_one('.description .xans-record- span[style*="font-size:12px"]') or item.select_one('.price')
                if not price_tag: continue
                
                price_text = "".join(filter(str.isdigit, price_tag.text))
                price = int(price_text) if price_text else 0
                
                # 抓取圖片
                img_tag = item.select_one('.thumbnail img')
                img_url = img_tag['src'] if img_tag else ""
                if img_url.startswith('//'): img_url = 'https:' + img_url
                
                # 抓取連結
                link = name_tag['href']
                if not link.startswith('http'): link = 'https://m.tw.slowand.com' + link
                
                products.append({
                    "store": "Slowand",
                    "name": name_tag.text.strip(),
                    "price": price,
                    "img": img_url,
                    "url": link,
                    "is_new": True
                })
            except Exception as e:
                print(f"第 {i} 個商品解析失敗: {e}")
                
        return products
    except Exception as e:
        print(f"🚨 爬蟲執行發生致命錯誤: {e}")
        return []

if __name__ == "__main__":
    results = scrape_slowand()
    print(f"--- 抓取結束，最終獲得 {len(results)} 件商品 ---")
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
