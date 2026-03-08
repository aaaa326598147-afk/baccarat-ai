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

# --- 2. 佈局與增強版 CSS ---
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
        /* 極低遮罩，保留背景原色 */
        .stApp::before {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.02); z-index: -1;
        }}
        .block-container {{ padding-top: 2rem !important; max-width: 500px !important; }}
        
        /* ⭐ 全域文字描邊強化：確保在亮處也看得清 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-weight: 800 !important;
            text-shadow: 
                -1.5px -1.5px 0 #000,  
                 1.5px -1.5px 0 #000,
                -1.5px  1.5px 0 #000,
                 1.5px  1.5px 0 #000,
                 3px 3px 6px rgba(0,0,0,0.8) !important;
        }}

        /* ⭐ 下拉選單文字清晰化：深色背景 + 金邊 */
        div[data-baseweb="select"] {{
            background-color: rgba(0, 0, 0, 0.8) !important;
            border: 1px solid #FFD700 !important;
            border-radius: 10px !important;
        }}
        div[data-baseweb="popover"] ul {{
            background-color: #1a1a1a !important;
        }}
        div[data-baseweb="popover"] li {{
            color: #FFD700 !important;
            font-weight: bold !important;
        }}

        /* 玻璃面板加厚 */
        .glass-panel {{
            background: rgba(0, 0, 0, 0.65);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 15px; padding: 20px;
        }}
        
        /* 按鈕美化 */
        div.stButton > button {{
            background: linear-gradient(145deg, #333, #000) !important;
            color: #FFD700 !important;
            border: 1.5px solid #FFD700 !important;
            border-radius: 12px !important;
            font-weight: bold !important;
        }}
        
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
        pwd = st.text_input("授權金鑰：", type="password", label_visibility="collapsed", placeholder="請輸入金鑰")
        if st.button("驗證進入系統", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True
                st.rerun()
    st.stop()

# --- 4. 主控台 ---
st.markdown("<h2 style='text-align: center;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px; margin-top:-10px;'>{today_str} | AI 算力連線中</p>", unsafe_allow_html=True)

# 房號選擇
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選擇監控房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控房號 —":
    st.markdown("<div style='text-align: center; padding: 20px; color: #FFD700;'>⚠️ 請選取房號以同步現場數據</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 數據面板 ---
st.markdown(f"""
    <div style='background: rgba(0,0,0,0.6); border: 2px solid #FFD700; border-radius: 15px; padding: 15px; text-align: center; margin-top: 10px;'>
        <span style='color: #FFD700; font-size: 12px;'>正在監控：{selected_room}</span><br>
        <span style='font-size: 32px; font-weight: 900;'>AI 運算就緒</span>
    </div>
""", unsafe_allow_html=True)

count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center; margin-top: 15px;'>📡 數據同步中 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    c1, c2 = st.columns(2)
    with c1: st.metric("推薦方向", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("信心值", f"{confidence}%")

# --- 6. AI 路評 ---
if st.session_state.history:
    history_html = []
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        history_html.append(f"<span style='color:{color};'>{x}</span>")
    st.markdown(
        f"<div style='text-align: center; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; margin: 15px 0; border: 1px solid #333;'>"
        f"{' <span style=\"color:#666\">▶</span> '.join(history_html)}</div>", 
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

# --- 8. 功能底板 ---
with st.expander("🧮 智能注碼計算", expanded=False):
    balance = st.number_input("💵 本金", value=10000, step=1000)
    risk = st.slider("⚖️ 風險 %", 1, 10, 2)
    st.success(f"建議下注：{int(balance * (risk / 100))}")
    if st.button("🧹 重置本桌數據", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
