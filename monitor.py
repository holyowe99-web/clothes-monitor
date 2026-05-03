import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 設定網頁標題與專業風格
st.set_page_config(page_title="韓系服飾監控助手", layout="wide", initial_sidebar_state="collapsed")

# 專業 CSS 樣式
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; border: 1px solid #e6e9ef; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .price-now { color: #ff4b4b; font-size: 20px; font-weight: bold; }
    .price-old { color: #888; text-decoration: line-through; font-size: 14px; margin-left: 5px; }
    .new-tag { background-color: #ff8c00; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .sale-tag { background-color: #28a745; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        last_update = datetime.fromtimestamp(os.path.getmtime('data.json')).strftime('%Y-%m-%d %H:%M:%S')
        return data, last_update
    return [], "尚未同步"

items, update_time = load_data()
df = pd.DataFrame(items)

st.title("👗 韓系服飾即時監控")
st.caption(f"🕒 最後數據同步時間：{update_time} (自動定時更新)")

if not df.empty:
    # 數據預處理
    df['discount_rate'] = df.apply(lambda x: round((1 - x['price'] / x['old_price']) * 100) if x['old_price'] > x['price'] else 0, axis=1)

    # 專業儀表板
    m1, m2, m3 = st.columns(3)
    m1.metric("🔍 監控總數", len(df))
    m2.metric("✨ 今日新品", len(df[df['is_new'] == True]), delta=f"+{len(df[df['is_new'] == True])}")
    m3.metric("🔥 特價中", len(df[df['discount_rate'] > 0]), delta=f"{len(df[df['discount_rate'] > 0])} 筆", delta_color="normal")

    st.divider()

    # 排序與篩選
    sort_option = st.selectbox("排序方式", ["最新上架", "降價幅度 (高 → 低)", "價格 (低 → 高)"])
    if sort_option == "降價幅度 (高 → 低)":
        df = df.sort_values(by="discount_rate", ascending=False)
    elif sort_option == "價格 (低 → 高)":
        df = df.sort_values(by="price", ascending=True)

    # 列表顯示
    for _, item in df.iterrows():
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(item['img'], use_container_width=True)
            with c2:
                tags = ""
                if item['is_new']: tags += '<span class="new-tag">NEW</span> '
                if item['discount_rate'] > 0: tags += f'<span class="sale-tag">▼ {item["discount_rate"]}% OFF</span>'
                st.markdown(tags, unsafe_allow_html=True)
                
                st.subheader(item['name']) # 顯示韓文/官方原名
                
                stock_color = "#28a745" if item['stock'] == "In Stock" else "#888"
                stock_text = "✅ 有現貨" if item['stock'] == "In Stock" else "❌ 已售罄"
                st.markdown(f"**店鋪：** {item['store']} | <span style='color:{stock_color}'>{stock_text}</span>", unsafe_allow_html=True)
                
                st.markdown(f"<span class='price-now'>NT$ {item['price']}</span><span class='price-old'>NT$ {item['old_price']}</span>", unsafe_allow_html=True)
                st.link_button("👉 前往官網查看", item['url'])
            st.divider()
else:
    st.info("目前尚無資料，請等待首次爬蟲執行完畢。")
