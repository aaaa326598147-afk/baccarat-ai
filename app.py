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

# --- 2. 主介面設定 (高清晰背景) ---
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
    pwd = st.text_input("輸入今日授權金鑰
