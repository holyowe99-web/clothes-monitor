import streamlit as st
import pd as pd
import json
import os
from datetime import datetime

# 設定網頁標題與風格
st.set_page_config(page_title="THE MONITOR", layout="wide", initial_sidebar_state="collapsed")

# 質感提升 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans TC', sans-serif;
    }
    
    .main-title {
        font-size: 50px;
        font-weight: 700;
        letter-spacing: 5px;
        color: #1a1a1a;
        margin-bottom: 0px;
        text-align: left;
    }
    
    .sub-title {
        font-size: 13px;
        color: #888;
        letter-spacing: 3px;
        margin-bottom: 40px;
        text-align: left;
    }

    .stMetric {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    
    .price-tag { font-size: 18px; font-weight: 600; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# 讀取資料
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        last_update = datetime.fromtimestamp(os.path.getmtime('data.json')).strftime('%Y.%m.%d %H:%M')
        return data, last_update
    return [], "WAITING FOR FIRST RUN"

items, update_time = load_data()
df = pd.DataFrame(items)

# --- 標題區 ---
st.markdown('<p class="main-title">THE MONITOR</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">REAL-TIME K-STYLE DATASTREAM // LAST UPDATE {update_time}</p>', unsafe_allow_html=True)

if not df.empty:
    # 統計數據
    m1, m2, m3 = st.columns(3)
    m1.metric("COLLECTION", f"{len(df)} ITEMS")
    m2.metric("NEW IN", len(df[df['is_new'] == True]))
    m3.metric("STORE", "SLOWAND TW")
    
    st.divider()

    # 商品網格展現
    cols = st.columns(4)
    for idx, item in df.iterrows():
        with cols[idx % 4]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"**{item['name']}**")
            st.markdown(f"<p class='price-tag'>NT$ {item['price']:,}</p>", unsafe_allow_html=True)
            st.link_button("VIEW ITEM", item['url'])
            st.write("---")
else:
    st.info("系統正在努力抓取資料中，請稍候並刷新網頁...")
