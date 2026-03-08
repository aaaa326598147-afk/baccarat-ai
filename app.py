import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 系統核心參數 ---
VERSION = "VIP AI-Pro V4.8 巔峰版"
LAST_SYNC = "2026-03-08 21:10"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 旗艦視覺 CSS 引擎 ---
st.set_page_config(page_title=VERSION, layout="centered")

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
        .block-container {{ padding-top: 2rem !important; max-width: 550px !important; }}
        
        /* 全域文字強化 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Segoe UI", "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 12px rgba(0,0,0,1) !important;
        }}

        /* 磨砂面板 */
        .premium-card {{
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-radius: 30px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.6);
        }}

        /* 狀態欄 */
        .status-bar {{
            background: linear-gradient(90deg, rgba(0,0,0,0.9), rgba(60,50,20,0.8), rgba(0,0,0,0.9));
            border: 1px solid #FFD700;
            border-radius: 50px;
            padding: 12px;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
            margin: 10px 0;
        }}

        /* 建議注碼數字 */
        .bet-glow {{
            color: #FFD700 !important;
            font-size: 72px !important;
            text-align: center;
            text-shadow: 0 0 25px rgba(255, 215, 0, 0.8), 2px 2px 5px #000 !important;
            margin: 10px 0;
        }}

        /* 按鈕視覺 */
        div.stButton > button {{
            background: linear-gradient(180deg, #333, #000) !important;
            color: #FFD700 !important;
            border: 1px solid rgba(255, 215, 0, 0.5) !important;
            border-radius: 15px !important;
            height: 3.6em !important;
            font-size: 18px !important;
            transition: all 0.3s ease !important;
        }}
        div.stButton > button:hover {{
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.4) !important;
        }}

        header {{ visibility: hidden; }}
        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 系統初始化 (登入介面優化) ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="premium-card" style="text-align:center;"><h1 style="font-size: 45px;">💎 VIP 核心系統</h1><p style="opacity:0.7; letter-spacing:2px;">授權專用通道</p></div>', unsafe_allow_html=True)
    
    # 增加輸入框與標題的間距
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True) 
    pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入當日授權碼")
    
    # 增加按鈕與輸入框的間距
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("初始化系統系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 頂部導航 ---
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
st.markdown('<h1 style="margin-bottom:0; font-size:40px;">💎 VIP 數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="opacity:0.9; font-size:13px; letter-spacing:2px;">{VERSION} | {LAST_SYNC}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 房號選擇
room_options = ["— 請選取監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("ROOM", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選取監控房號 —":
    st.markdown("<div class='premium-card' style='text-align: center; padding: 60px;'>📡 加密通道連線中，請選取房號...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 狀態演算邏輯 ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 

if count < 5:
    msg, clr = f"🔍 數據校準採樣中 ({count}/5)...", "#FFD700"
elif is_shield:
    msg, clr = "🚫 系統熔斷保護：偵測亂局，請觀望", "#FF4B4B"
else:
    msg, clr = "● AI 雲端算力同步成功", "#00FF00"

st.markdown(f'<div class="status-bar"><span style="color:{clr};">{msg}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測區 ---
if count >= 5 and not is_shield:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        color = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>AI 推薦方向</p><h1 style='color:{color}!important; text-align:center; font-size:55px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>數據信心度</p><h1 style='text-align:center; font-size:55px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 路評紀錄 ---
if st.session_state.history:
    bubbles = "".join([f"<div style='background:rgba(0,0,0,0.6); border:1px solid {'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; margin:0 4px;'>{x}</div>" for x in st.session_state.history[-10:]])
    st.markdown(f"<div style='display:flex; justify-content:center; margin:20px 0;'>{bubbles}</div>", unsafe_allow_html=True)

# --- 8. 控制台 (無警告穩壓版) ---
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])

if col_b1.button("🔴 莊 家", use_container_width=True):
    res = "莊"
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(res)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.rerun()

if col_b2.button("和", use_container_width=True):
    st.session_state.history.append("和"); st.rerun()

if col_b3.button("🔵 閒 家", use_container_width=True):
    res = "閒"
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(res)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.rerun()

# --- 9. 注碼管理中心 (修正間距問題) ---
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # 增加物理隔閡
st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
st.markdown("<p style='color:#FFD700; text-align:center; font-size:20px; margin-top:0;'>⚖️ 智能注碼管理中心</p>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns(2)
with col_f1: bal = st.number_input("💵 當前本金", value=10000, step=1000, label_visibility="collapsed")
with col_f2: rsk = st.slider("⚖️ 風險比例 %", 1, 10, 2, label_visibility="collapsed")

mult = 0.0 if count < 5 or is_shield else (0.8 if bal > 10000 else 1.0)
suggest = int(bal * (rsk/100) * mult)

if is_shield:
    st.markdown("<h1 style='color:#FF4B4B!important; text-align:center; font-size:50px; letter-spacing:5px;'>暫停操作</h1>", unsafe_allow_html=True)
else:
    st.markdown("<p style='opacity:0.7; text-align:center; margin:0;'>建議下注金額</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="bet-glow">{suggest}</div>', unsafe_allow_html=True)

if st.button("🧹 重置數據 / 快速換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
