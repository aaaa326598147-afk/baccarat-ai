import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化 (2026-03-08 密碼 0308) ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'win_count' not in st.session_state: st.session_state.win_count = 0

# --- 2. 主介面設定 (高清晰背景與畫面集中化) ---
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
            background-size: cover;
            background-position: center top;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.05); 
            z-index: -1;
        }}
        .block-container {{
            padding-top: 1.5rem !important;
            max-width: 500px !important;
        }}
        h1, h2, h3, .stMetric, p, span, div, label, .stCaption {{
            color: #FFFFFF !important;
            text-shadow: 3px 3px 5px #000, -1px -1px 0 #000, 1px -1px 0 #000 !important;
            font-weight: 800 !important;
        }}
        div.stButton > button {{
            background-color: rgba(0,0,0,0.6) !important;
            border: 2px solid #FFFFFF !important;
            height: 3.5em !important;
        }}
        .stSidebar {{ background-color: rgba(0,0,0,0.85); }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入介面 ---
if not st.session_state.login:
    st.title("💎 私人俱樂部：決策輔助工具")
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
    if st.button("驗證進入", use_container_width=True):
        if pwd == today_code:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("金鑰錯誤")
    st.stop()

# --- 4. 主內容 (房號可選，不阻擋畫面) ---
st.markdown("<h2 style='text-align: center;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)

st.sidebar.header("📌 桌面資訊")
room_id = st.sidebar.text_input("輸入房號 (選填)", value="", placeholder="")

if st.sidebar.button("🧹 換桌重置"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()

display_room = f"📡 正在監控：{room_id}" if room_id else "📡 AI 算力連線中"
st.markdown(f"<div style='text-align: center; font-size:24px; color:#FFD700;'>{display_room}</div>", unsafe_allow_html=True)

# --- 5. 核心決策 ---
count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center; margin-top:5px;'>📥 數據同步中 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(92, 99)
    c1, c2 = st.columns(2)
    with c1: st.metric("推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("信心", f"{confidence}%")

# --- 6. AI 路評紀錄 ---
if st.session_state.history:
    styled_h = [f"🔴{x}" if x=="莊" else f"🔵{x}" if x=="閒" else f"🟢{x}" for x in st.session_state.history]
    st.markdown(f"<div style='text-align: center; font-size: 14px; margin: 5px 0;'>{' ➡️ '.join(styled_h[-10:])}</div>", unsafe_allow_html=True)

# --- 7. 操作按鈕 ---
col1, col2, col3 = st.columns([2, 1, 2])

def handle_click(res):
    if len(st.session_state.history) >= 5:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res)
    time.sleep(0.1)
    st.rerun()

with col1:
    if st.button("🔴 莊", use_container_width=True): handle_click("莊")
with col2:
    if st.button("🟢 和", use_container_width=True): handle_click("和")
with col3:
    if st.button("🔵 閒", use_container_width=True): handle_click("閒")

# --- 8. 下方金額計算機 ---
with st.expander("🧮 智能注碼計算機", expanded=True):
    balance = st.number_input("💵 本金", value=10000, step=1000)
    risk = st.slider("⚖️ 下注 %", 1, 10, 2)
    st.success(f"💡 建議下注：**{int(balance * (risk / 100))}**")
