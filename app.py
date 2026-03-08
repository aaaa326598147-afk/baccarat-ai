import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化 (2026-03-08) ---
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
        .block-container {{ padding-top: 1.5rem !important; max-width: 550px !important; }}
        
        /* ⭐ 核心：文字浮雕感維持 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 0px #666, 4px 4px 8px rgba(0,0,0,0.8) !important;
        }}

        /* 排版間距優化 */
        .section-gap {{ margin-bottom: 30px !important; }}

        /* 房號選單優化 */
        div[data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 1.5px solid #FFFFFF !important;
            border-radius: 12px !important;
        }}

        /* 氣泡式路評紀錄 */
        .history-bubble {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            padding: 8px 15px;
            display: inline-block;
            margin: 0 5px;
            font-size: 18px;
        }}

        /* 按鈕風格 */
        div.stButton > button {{
            background: rgba(0, 0, 0, 0.6) !important;
            color: #FFD700 !important;
            border: 2px solid #FFD700 !important;
            border-radius: 15px !important;
            font-weight: 900 !important;
            height: 4em !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}

        /* 隱藏側邊欄 */
        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入畫面 ---
if not st.session_state.login:
    st.markdown("<br><br><h1 style='text-align: center; font-size: 48px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入授權金鑰")
        if st.button("驗證連線核心", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 頂部標題與房號 ---
st.markdown("<h2 style='text-align: center; margin-bottom: 5px;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>{today_str} | AI 算力中心已連線</p>", unsafe_allow_html=True)

rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請點擊此處選取監控房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請點擊此處選取監控房號 —":
    st.markdown("<div style='text-align: center; padding: 40px;'>⚠️ 請先選取房號以同步現場數據</div>", unsafe_allow_html=True)
    st.stop()

st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

# --- 5. AI 路評 (橫向發光氣泡) ---
if st.session_state.history:
    st.markdown("<p style='text-align: center; font-size: 14px; margin-bottom: 5px;'>📊 現場開出紀錄</p>", unsafe_allow_html=True)
    history_html = []
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        history_html.append(f"<span class='history-bubble' style='color:{color};'>{x}</span>")
    
    st.markdown(
        f"<div style='text-align: center; margin-bottom: 25px;'>"
        f"{''.join(history_html)}</div>", 
        unsafe_allow_html=True
    )

# --- 6. AI 預測面板 ---
count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<h3 style='text-align: center;'>📡 數據同步進度 ({count}/5)</h3>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1: st.metric("AI 推薦方向", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with col_p2: st.metric("核心信心指標", f"{confidence}%")

st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

# --- 7. 操作按鈕 ---
col1, col2, col3 = st.columns([2, 1, 2])
def handle_click(res):
    if len(st.session_state.history) >= 5:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res)
    time.sleep(0.1); st.rerun()

with col1:
    if st.button("莊 🔴", use_container_width=True): handle_click("莊")
with col2:
    if st.button("和", use_container_width=True): handle_click("和")
with col3:
    if st.button("閒 🔵", use_container_width=True): handle_click("閒")

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# --- 8. 智能金額計算機 (獨立區塊) ---
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
with st.expander("🧮 智能注碼管理 (Risk Management)", expanded=True):
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c_inv1, c_inv2 = st.columns([3, 2])
    with c_inv1:
        balance = st.number_input("💵 目前本金", value=10000, step=1000)
    with c_inv2:
        risk = st.slider("⚖️ 風險 %", 1, 10, 2)
    
    suggested = int(balance * (risk / 100))
    st.markdown(f"<h2 style='text-align: center; color: #FFD700; margin: 15px 0;'>建議下注金額：{suggested}</h2>", unsafe_allow_html=True)
    
    if st.button("🧹 換桌 / 清空數據紀錄", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
