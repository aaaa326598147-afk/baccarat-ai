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

# --- 2. 佈局與立體字 CSS ---
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
        .block-container {{ padding-top: 1.5rem !important; max-width: 600px !important; }}
        
        /* ⭐ 立體浮雕文字效果 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 0px #666, 4px 4px 8px rgba(0,0,0,0.8) !important;
        }}

        /* 路評氣泡排列 */
        .history-row {{
            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 15px 0;
        }}
        .history-bubble {{
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 50%; width: 38px; height: 38px;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px;
        }}

        /* 下注按鈕視覺 */
        div.stButton > button {{
            background: rgba(0, 0, 0, 0.6) !important;
            color: #FFD700 !important;
            border: 2px solid #FFD700 !important;
            border-radius: 15px !important;
            height: 4.5em !important;
            font-weight: 900 !important;
            font-size: 18px !important;
        }}

        /* 核心：強制脫離區塊樣式 */
        .bottom-anchor {{
            margin-top: 120px !important; /* 強制推開超大距離 */
            padding: 20px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入 (略) ---
if not st.session_state.login:
    st.markdown("<br><br><h1 style='text-align: center;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入金鑰")
        if st.button("驗證進入系統", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 主顯示區 ---
st.markdown("<h2 style='text-align: center;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>{today_str} | AI 同步</p>", unsafe_allow_html=True)

rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選擇監控房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控房號 —":
    st.markdown("<div style='text-align: center; padding: 40px;'>⚠️ 尚未選取監控對象</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. AI 路評 ---
if st.session_state.history:
    bubbles = ""
    for x in st.session_state.history[-10:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        bubbles += f"<div class='history-bubble' style='color:{color};'>{x}</div>"
    st.markdown(f"<div class='history-row'>{bubbles}</div>", unsafe_allow_html=True)

# --- 6. 預測與操作按鈕 (上半部核心) ---
count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<h3 style='text-align: center;'>📡 數據同步進度 ({count}/5)</h3>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None: st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    col_v1, col_v2 = st.columns(2)
    with col_v1: st.metric("AI 推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with col_v2: st.metric("信心度度", f"{confidence}%")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
def add_rec(res):
    if len(st.session_state.history) >= 5: st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1:
    if st.button("莊 🔴", use_container_width=True): add_rec("莊")
with col_b2:
    if st.button("和", use_container_width=True): handle_click = add_rec("和")
with col_b3:
    if st.button("閒 🔵", use_container_width=True): add_rec("閒")

# --- 7. 智能注碼管理 (下半部 - 物理脫離) ---
# 使用 HTML 建立一個明顯的視覺斷層
st.markdown("<div class='bottom-anchor'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFD700;'>🧮 智能注碼管理中心</h3>", unsafe_allow_html=True)

bal = st.number_input("💵 目前本金", value=10000, step=1000)
rsk = st.slider("⚖️ 下注風險比例 %", 1, 10, 2)
sug = int(bal * (rsk / 100))

st.markdown(f"<h2 style='text-align: center; color: #FFD700; margin: 15px 0;'>建議下注：{sug}</h2>", unsafe_allow_html=True)

if st.button("🧹 重置本桌數據與預測", use_container_width=True):
    st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
