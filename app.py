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
if 'win_count' not in st.session_state: st.session_state.win_count = 0

# --- 2. 主介面設定 (原圖背景邏輯) ---
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
        /* 💡 這裡將遮罩調到極淺 (0.1)，讓原圖顏色爆發出來 */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.1); 
            z-index: -1;
        }}
        /* 💡 加強文字黑色描邊，確保在亮色背景下依然清晰 */
        h1, h2, h3, .stMetric, p, span, div, label {{
            color: #FFFFFF !important;
            text-shadow: 
                2px 2px 3px #000,
                -1px -1px 0 #000,  
                1px -1px 0 #000,
                -1px 1px 0 #000,
                 1px 1px 0 #000 !important;
            font-weight: 800 !important;
        }}
        /* 按鈕半透明黑，增加質感 */
        div.stButton > button {{
            background-color: rgba(0,0,0,0.6) !important;
            border: 2px solid #FFFFFF !important;
            color: white !important;
        }}
        .stSidebar {{ background-color: rgba(0,0,0,0.8); }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    # 沒圖時才顯示黑底
    st.markdown("<style>.stApp { background-color: #121212; }</style>", unsafe_allow_html=True)

# --- 3. 登入介面 ---
if not st.session_state.login:
    st.title("💎 深夜筆電・獲利紀實")
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
    if st.button("驗證進入", use_container_width=True):
        if pwd == today_code:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("金鑰錯誤")
    st.stop()

# --- 4. 主內容 (房號與決策) ---
st.title("💎 深夜筆電・獲利紀實")
st.sidebar.header("📌 桌面資訊")
room_id = st.sidebar.text_input("請輸入房號", placeholder="例如：VIP-888")

if not room_id:
    st.warning("👈 請先輸入房號以連線雲端算力。")
    st.stop()

# (後續接原本的歷史紀錄與按鈕代碼...)
st.write(f"📡 正在監控：**{room_id}**")
