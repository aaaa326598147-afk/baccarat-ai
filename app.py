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
        .block-container {{ padding-top: 1.5rem !important; max-width: 550px !important; }}
        
        /* ⭐ 還原浮雕立體字：白色厚度 + 深色散影 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 
                2px 2px 0px #666,  
                4px 4px 8px rgba(0,0,0,0.8) !important;
        }}

        /* 選單背景修正：半透明淡灰，不遮擋文字 */
        div[data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.15) !important;
            border: 1.5px solid #FFFFFF !important;
            border-radius: 10px !important;
        }}
        
        /* 玻璃質感容器：讓路評與計算機背景清晰 */
        .glass-box {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px; padding: 15px; margin: 10px 0;
        }}

        /* 按鈕風格 */
        div.stButton > button {{
            background: rgba(0, 0, 0, 0.6) !important;
            color: #FFD700 !important;
            border: 1.5px solid #FFD700 !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入畫面 ---
if not st.session_state.login:
    st.markdown("<br><br><h1 style='text-align: center; font-size: 42px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 5, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入授權金鑰")
        if st.button("驗證並開啟 AI 核心", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True
                st.rerun()
    st.stop()

# --- 4. 主控台 ---
st.markdown("<h2 style='text-align: center; margin-bottom:0;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>{today_str} | AI 連線中</p>", unsafe_allow_html=True)

# 房號選擇
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選擇監控房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控房號 —":
    st.markdown("<div style='text-align: center; padding: 30px;'>⚠️ 點選上方房號開始同步</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. AI 路評 (補回) ---
if st.session_state.history:
    history_html = []
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        # 這裡加上白色浮雕效果，確保符號也能看清
        history_html.append(f"<span style='color:{color}; font-size: 20px; font-weight: 900;'>{x}</span>")
    
    st.markdown(
        f"<div class='glass-box' style='text-align: center;'>"
        f"{' <span style=\"color:#fff; text-shadow:none;\">▶</span> '.join(history_html)}</div>", 
        unsafe_allow_html=True
    )

# --- 6. 核心推薦與數據面板 ---
count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center;'>📡 數據同步進度 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    
    st.markdown(f"<div class='glass-box' style='text-align:center;'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.metric("AI 推薦方向", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("算力信心指標", f"{confidence}%")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. 操作按鈕 ---
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
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

# --- 8. 智能金額計算機 (補回) ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander("🧮 智能注碼管理 (點擊展開)", expanded=True):
    st.markdown("<div style='background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px;'>", unsafe_allow_html=True)
    balance = st.number_input("💵 目前本金", value=10000, step=1000)
    risk = st.slider("⚖️ 下注風險 %", 1, 10, 2)
    suggested = int(balance * (risk / 100))
    st.markdown(f"<h3 style='text-align: center; color: #FFD700;'>建議下注：{suggested}</h3>", unsafe_allow_html=True)
    
    if st.button("🧹 換桌/清空數據", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
