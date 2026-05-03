import streamlit as st
import pandas as pd

# 這裡我們先用模擬數據，等妳部署好介面，我再給你抓取這兩家網站 HTML 的爬蟲模組
# 這樣妳可以先看到妳想要的「降價排序」與「庫存標記」版面

def load_data():
    # 之後這裡會對接你的 Supabase 資料庫
    return [
        {
            "store": "Slowand",
            "name": "自製款 5%折扣 挺版西裝褲",
            "price": 912,
            "old_price": 1200,
            "img": "https://m.tw.slowand.com/web/product/big/202404/655f05a8b5e98285906236b2839b1399.jpg",
            "url": "https://m.tw.slowand.com/",
            "is_new": True,
            "stock": "In Stock"
        },
        {
            "store": "Blackup",
            "name": "極簡廓形黑色大衣",
            "price": 2500,
            "old_price": 2500,
            "img": "https://blackupglobal.com/web/product/big/202311/736d5071168c786a5f78a2e4e6f43e33.jpg",
            "url": "https://blackupglobal.com/",
            "is_new": False,
            "stock": "Out of Stock"
        }
    ]

# 設定網頁標題與手機優先排版
st.set_page_config(page_title="韓系服飾監控", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    .price-tag { color: #ff4b4b; font-size: 20px; font-weight: bold; }
    .new-tag { background-color: #ff8c00; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👗 購物監控 App")

# A. 降價幅度排序功能
items = load_data()
df = pd.DataFrame(items)
df['discount_rate'] = df.apply(lambda x: round((1 - x['price'] / x['old_price']) * 100) if x['old_price'] > x['price'] else 0, axis=1)

sort_option = st.selectbox("選擇排序方式", ["最新上架", "降價幅度 (高 → 低)"])

if sort_option == "降價幅度 (高 → 低)":
    df = df.sort_values(by="discount_rate", ascending=False)

# 顯示商品列表
for _, item in df.iterrows():
    with st.container():
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.image(item['img'], use_container_width=True)
        with col2:
            # 顯示標籤
            tags = ""
            if item['is_new']: tags += '<span class="new-tag">NEW</span> '
            if item['discount_rate'] > 0: tags += f'<span style="color:#00ff00;">▼ {item['discount_rate']}% OFF</span>'
            
            st.markdown(tags, unsafe_allow_html=True)
            st.subheader(item['name'])
            
            # C. 庫存標示
            stock_status = "✅ 有現貨" if item['stock'] == "In Stock" else "❌ 已售罄"
            color = "#00ff00" if item['stock'] == "In Stock" else "#888888"
            st.markdown(f"狀態：<span style='color:{color}'>{stock_status}</span>", unsafe_allow_html=True)
            
            st.markdown(f"<span class='price-tag'>NT$ {item['price']}</span> <small><s>NT$ {item['old_price']}</s></small>", unsafe_allow_html=True)
            
            # 連結到實際產品網頁
            st.link_button("前往官網購買", item['url'])
        st.divider()
