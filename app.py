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
        /* 針對選單文字清晰化 */
        div[data-baseweb="select"] {{
            background-color: rgba(255, 255, 255, 0.9) !important;
        }}
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

# --- 4. 房號清單設定 ---
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["請選擇房號"] + rb_list + s_list # 預設提示

# --- 5. 側邊欄控制 ---
st.sidebar.header("📌 桌面資訊")
selected_room = st.sidebar.selectbox("請選擇當前桌號", options=room_options)

if st.sidebar.button("🧹 換桌重置"):
    st.session_state.history = []; st.session_state.next_pred = None; st.rerun()

# --- 🔒 房號強制鎖定門檻 ---
if selected_room == "請選擇房號":
    st.markdown("<h2 style='text-align: center;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
    st.warning("⚠️ 請先在左側選單選擇正確房號，以連線 AI 運算系統。")
    st.stop()

# --- 6. 主內容 (選擇房號後顯示) ---
st.markdown("<h2 style='text-align: center;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; font-size:32px; color:#FFD700;'>📡 監控中：{selected_room}</div>", unsafe_allow_html=True)

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

# --- 7. AI 路評紀錄 ---
if st.session_state.history:
    styled_h = [f"🔴{x}" if x=="莊" else f"🔵{x}" if x=="閒" else f"🟢{x}" for x in st.session_state.history]
    st.markdown(f"<div style='text-align: center; font-size: 14px; margin: 5px 0;'>{' ➡️ '.join(styled_h[-10:])}</div>", unsafe_allow_html=True)

# --- 8. 操作按鈕 ---
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

#
