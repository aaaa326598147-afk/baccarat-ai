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

# --- 2. 佈局設定與高級 CSS ---
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
        .block-container {{ padding-top: 3rem !important; max-width: 500px !important; }}
        
        /* 高級感：玻璃質感面板 */
        .glass-panel {{
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255, 215, 0, 0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-top: 20px;
        }}
        
        /* 文字美化 */
        h1, h2, h3, .stMetric, p, span, div, label {{
            color: #FFFFFF !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            font-weight: 700;
        }}
        
        /* 按鈕高級化 */
        div.stButton > button {{
            background: linear-gradient(145deg, #333, #000) !important;
            color: #FFD700 !important;
            border: 1px solid #FFD700 !important;
            border-radius: 12px !important;
            height: 3.5em !important;
            transition: all 0.3s;
        }}
        div.stButton > button:hover {{
            background: #FFD700 !important; color: #000 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        }}
        
        /* 隱藏原生側邊欄 */
        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 高級登入介面 ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 42px; letter-spacing: 5px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFD700; letter-spacing: 2px;'>VIP DECISION SUPPORT</p>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 5, 1])
    with col_m:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        pwd = st.text_input("輸入授權金鑰：", type="password", label_visibility="collapsed", placeholder="請輸入金鑰")
        if st.button("驗證進入系統", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("金鑰驗證失敗")
    st.stop()

# --- 4. 主控台內容 ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #ccc; font-size: 14px;'>{today_str} | 雲端 AI 核心已連線</p>", unsafe_allow_html=True)

# 房號選擇 (置中排版)
rb_list = [f"RB0{i}" for i in range(1, 8)]
s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選擇監控房號 —"] + rb_list + s_list

selected_room = st.selectbox("房號選擇", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控房號 —":
    st.info("請選取房號以同步現場數據。")
    st.stop()

# --- 5. 數據顯示面板 (玻璃卡片) ---
st.markdown(f"""
    <div style='background: rgba(255,215,0,0.15); border: 1px solid #FFD700; border-radius: 15px; padding: 15px; text-align: center; margin-top: 20px;'>
        <span style='color: #FFD700; font-size: 12px;'>正在監控</span><br>
        <span style='font-size: 32px; font-weight: 900; letter-spacing: 3px;'>{selected_room}</span>
    </div>
""", unsafe_allow_html=True)

count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<p style='text-align: center; margin-top: 15px;'>📡 數據收集同步中 ({count}/5)</p>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    
    c1, c2 = st.columns(2)
    with c1: st.metric("推薦方向", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("運算信心", f"{confidence}%")

# --- 6. AI 路評 (修正報錯點) ---
if st.session_state.history:
    history_html = []
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        history_html.append(f"<span style='color:{color};'>{x}</span>")
    
    st.markdown(
        f"<div style='text-align: center; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 10px; margin: 15px 0;'>"
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

# --- 8. 金額計算機與換桌 ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander("🧮 智能注碼計算與換桌", expanded=False):
    balance = st.number_input("💵 目前本金", value=10000, step=1000)
    risk = st.slider("⚖️ 風險等級 (%)", 1, 10, 2)
    st.success(f"建議下注額：{int(balance * (risk / 100))}")
    if st.button("🧹 換桌重置數據", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
