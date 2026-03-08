import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化 ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None

# --- 2. 佈局與文字浮雕效果 CSS ---
st.set_page_config(page_title="💎 AI 決策系統", layout="centered")

cover_image_path = "cover.jpg"
if os.path.exists(cover_image_path):
    with open(cover_image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{data}");
            background-size: cover; background-position: center top; background-attachment: fixed;
        }}
        .block-container {{ padding-top: 2rem !important; max-width: 500px !important; }}
        
        /* ⭐ 核心：還原截圖中的文字浮雕感 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 
                2px 2px 0px #666,  /* 淺灰色厚度 */
                4px 4px 8px rgba(0,0,0,0.8) !important; /* 深色散影 */
        }}

        /* ⭐ 僅修正下拉選單：改為淡灰色，不遮擋文字 */
        div[data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.2) !important; /* 淺色透明底 */
            border: 1px solid #FFFFFF !important;
            border-radius: 8px !important;
        }}
        
        /* 下拉選單內的選項：維持白底黑字確保看清 */
        div[data-baseweb="popover"] ul {{
            background-color: #FFFFFF !important;
        }}
        div[data-baseweb="popover"] li {{
            color: #333333 !important;
            font-weight: bold !important;
            text-shadow: none !important; /* 選項內不加陰影 */
        }}

        /* 隱藏原生側邊欄 */
        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入畫面 ---
if not st.session_state.login:
    st.markdown("<br><br><h1 style='text-align: center; font-size: 42px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 5, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入金鑰")
        if st.button("驗證進入系統", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True
                st.rerun()
    st.stop()

# --- 4. 主控台 ---
st.markdown("<h2 style='text-align: center;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>{today_str} | 雲端 AI 核心</p>", unsafe_allow_html=True)

# 房號選擇
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選擇監控房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控房號 —":
    st.markdown("<div style='text-align: center; padding: 20px;'>⚠️ 請選取房號以同步數據</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 數據面板 ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 20px;'>
        <span style='font-size: 14px;'>正在監控：{selected_room}</span><br>
        <span style='font-size: 32px;'>AI 運算就緒</span>
    </div>
""", unsafe_allow_html=True)

count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center;'>📡 數據同步中 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    c1, c2 = st.columns(2)
    with c1: st.metric("推薦", current_p)
    with c2: st.metric("信心", f"{confidence}%")

# --- 6. AI 路評 ---
if st.session_state.history:
    history_html = []
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        history_html.append(f"<span style='color:{color};'>{x}</span>")
    st.markdown(
        f"<div style='text-align: center; margin: 15px 0;'>"
        f"{' ▶ '.join(history_html)}</div>", 
        unsafe_allow_html=True
    )

# --- 7. 操作按鈕 ---
col1, col2, col3 = st.columns([2, 1, 2])
def handle_click(res):
    if len(st.session_state.history) >= 5:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res)
    time.sleep(0.1)
    st.rerun()

with col1:
    if st.button("莊 🔴", use_container_width=True): handle_click("莊")
with col2:
    if st.button("和", use_container_width=True): handle_click("和")
with col3:
    if st.button("閒 🔵", use_container_width=True): handle_click("閒")
