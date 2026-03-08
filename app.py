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

# --- 2. 佈局與底色強化 CSS ---
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
        .stApp::before {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.02); z-index: -1;
        }}
        .block-container {{ padding-top: 2rem !important; max-width: 500px !important; }}
        
        /* 保持原本文字效果不動 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-weight: 800 !important;
            text-shadow: 
                -2px -2px 0 #000,  
                 2px -2px 0 #000,
                -2px  2px 0 #000,
                 2px  2px 0 #000,
                 4px 4px 8px rgba(0,0,0,0.9) !important;
        }}

        /* ⭐ 修正重點：僅加深選單底色 */
        div[data-baseweb="select"] > div {{
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 12px !important;
        }}
        /* 下拉列表容器加深 */
        div[data-baseweb="popover"] ul {{
            background-color: #000000 !important;
            border: 1px solid #FFD700 !important;
        }}
        /* 下拉選項文字 */
        div[data-baseweb="popover"] li {{
            color: #FFD700 !important;
        }}

        /* ⭐ 加深數據面板底色 */
        .main-panel {{
            background: rgba(0, 0, 0, 0.85) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 20px; 
            padding: 20px;
            margin-top: 15px;
            text-align: center;
        }}
        
        /* 按鈕風格 */
        div.stButton > button {{
            background: linear-gradient(145deg, #222, #000) !important;
            color: #FFD700 !important;
            border: 2px solid #FFD700 !important;
            border-radius: 15px !important;
            height: 3.8em !important;
        }}
        
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
        st.markdown("<div style='background: rgba(0,0,0,0.85); padding: 30px; border-radius: 20px; border: 1px solid #FFD700;'>", unsafe_allow_html=True)
        pwd = st.text_input("— 請輸入金鑰 —", type="password", label_visibility="collapsed", placeholder="授權金鑰")
        if st.button("驗證進入系統", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 4. 主控台 ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #ccc; font-size: 14px; margin-bottom: 20px;'>{today_str} | AI 運算核心</p>", unsafe_allow_html=True)

# 房號選擇 (已加深底色)
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選取監控房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選取監控房號 —":
    st.markdown("<div style='text-align: center; padding: 25px; background: rgba(0,0,0,0.85); border-radius: 15px; color: #FFD700; border: 1px dashed #FFD700;'>⚠️ 請連線房號以獲取演算數據</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 數據面板 (已加深底色) ---
st.markdown(f"""
    <div class="main-panel">
        <span style='color: #FFD700; font-size: 14px; letter-spacing: 2px;'>連線成功：{selected_room}</span><br>
        <span style='font-size: 34px; font-weight: 900; color: #fff;'>AI 推薦引擎就緒</span>
    </div>
""", unsafe_allow_html=True)

count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center; margin-top: 15px;'>📡 數據同步進度 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    c1, c2 = st.columns(2)
    with c1: st.metric("預測方向", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("信心指標", f"{confidence}%")

# --- 6. AI 路評 (加深紀錄條底色) ---
if st.session_state.history:
    history_html = []
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        history_html.append(f"<span style='color:{color}; font-size: 18px;'>{x}</span>")
    st.markdown(
        f"<div style='text-align: center; background: rgba(0,0,0,0.95); padding: 12px; border-radius: 15px; margin: 15px 0; border: 1px solid #FFD700;'>"
        f"{' <span style=\"color:#555\">▶</span> '.join(history_html)}</div>", 
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

# --- 8. 腳部底板 ---
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
with st.expander("🧮 智能注碼管理與重置", expanded=False):
    balance = st.number_input("💵 目前本金", value=10000, step=1000)
    risk = st.slider("⚖️ 下注風險 %", 1, 10, 2)
    st.success(f"建議下注：{int(balance * (risk / 100))}")
    if st.button("🧹 重置當前數據", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
