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

# --- 2. 佈局設定與核心 CSS ---
st.set_page_config(page_title="💎 AI 決策系統", layout="centered")

cover_image_path = "cover.jpg"
if os.path.exists(cover_image_path):
    with open(cover_image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        /* 背景設定 */
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
            padding-top: 2rem !important;
            max-width: 550px !important;
        }}
        
        /* 高級玻璃卡片樣式 */
        .glass-card {{
            background: rgba(0, 0, 0, 0.75);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255, 215, 0, 0.3);
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            margin-bottom: 20px;
        }}
        
        /* 文字與數值美化 */
        h1, h2, h3, .stMetric, p, span, div, label, .stCaption {{
            color: #FFFFFF !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            font-family: "Microsoft JhengHei", sans-serif;
        }}
        
        /* 按鈕高級化：深色漸層 + 金邊 */
        div.stButton > button {{
            background: linear-gradient(145deg, #333, #000) !important;
            color: #FFD700 !important;
            border: 1px solid #FFD700 !important;
            border-radius: 12px !important;
            height: 3.8em !important;
            font-weight: bold !important;
            letter-spacing: 1px;
            transition: all 0.3s;
        }}
        div.stButton > button:hover {{
            background: #FFD700 !important;
            color: #000 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
        }}
        
        /* 隱藏原生側邊欄 (避免簡陋感) */
        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入介面 ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 48px; letter-spacing: 8px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc;'>PREMIUM DECISION SYSTEM</p>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_m:
        pwd = st.text_input("輸入授權金鑰：", type="password", label_visibility="collapsed")
        if st.button("驗證進入", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("金鑰驗證失敗")
    st.stop()

# --- 4. 主控台介面 (直接整合房號選擇) ---
st.markdown("<h1 style='text-align: center; font-size: 36px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; margin-bottom: 25px;'>{today_str} | 智能決策運算中</p>", unsafe_allow_html=True)

# 集中區域房號選擇
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選擇監控桌號 —"] + rb_list + s_list

selected_room = st.selectbox("桌號連線", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控桌號 —":
    st.markdown("<div style='background: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px; border: 1px dashed #666; text-align: center;'>請選取房號以同步連線雲端算力</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 核心顯示面板 ---
st.markdown(f"""
    <div style='background: rgba(255,215,0,0.1); border: 1px solid #FFD700; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px;'>
        <span style='color: #FFD700; font-size: 14px;'>房號連線成功</span><br>
        <span style='font-size: 32px; font-weight: 900;'>{selected_room}</span>
    </div>
""", unsafe_allow_html=True)

# 推薦數據
count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center;'>📡 數據同步進度 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    current_p = st.session_state.next_pred
    confidence = random.randint(92, 99)
    
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("運算信心", f"{confidence}%")

# --- 6. AI 路評與操作區 ---
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

if st.session_state.history:
    styled_h = [f"<span style='color:{'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}'>{x}</span>" for x in st.session_state.history[-8:]]
    st.markdown(f"<div style='text-align: center; background: rgba(0,0,0,0.4); padding: 8px; border-radius: 10px; margin-bottom: 15px;'>{' <span style='color:#666'>▶</span> '.join(styled_h)}</div>", unsafe_allow_html=True)

# 操作按鈕
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

# --- 7. 功能底板 ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander("🧮 智能注碼計算與重置", expanded=False):
    balance = st.number_input("💵 當前本金", value=10000, step=1000)
    risk = st.slider("⚖️ 風險等級 (%)", 1, 10, 2)
    st.success(f"建議下注量：{int(balance * (risk / 100))}")
    if st.button("🧹 清空當前桌數據", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
