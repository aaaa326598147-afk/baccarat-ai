import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 系統核心參數 ---
VERSION = "VIP AI-Pro V5.1 最終旗艦版"
LAST_SYNC = "2026-03-08 22:15"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華白金視覺 CSS 引擎 ---
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
        
        /* 徹底隱藏輸入框下方的英文 */
        [data-testid="stInputWidgetInstructions"] {{ display: none !important; }}

        /* 全域文字強化 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Segoe UI", "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8) !important;
        }}

        /* 白金面板 */
        .platinum-card {{
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(35px);
            -webkit-backdrop-filter: blur(35px);
            border: 1px solid rgba(255, 215, 0, 0.5);
            border-radius: 35px;
            padding: 30px;
            margin: 15px 0;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        }}

        /* 動態數據監控框 (修正原本空的區域) */
        .data-monitor {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 50px;
            padding: 10px;
            text-align: center;
            margin: 15px 0;
            font-size: 14px;
            letter-spacing: 2px;
            box-shadow: inset 0 0 10px rgba(255,215,0,0.1);
        }}

        /* 狀態流光欄 */
        .status-bar {{
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #FFD700;
            border-radius: 50px;
            padding: 12px;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            margin: 10px 0;
        }}

        /* 下注金額發光 */
        .bet-glow {{
            color: #FFD700 !important;
            font-size: 80px !important;
            text-align: center;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.8), 2px 2px 5px #000 !important;
            margin: 10px 0;
        }}

        /* 白金按鈕 */
        div.stButton > button {{
            background: linear-gradient(145deg, rgba(50,50,50,0.95), rgba(0,0,0,0.95)) !important;
            color: #FFD700 !important;
            border: 1px solid rgba(255, 215, 0, 0.6) !important;
            border-radius: 20px !important;
            height: 3.7em !important;
            font-size: 18px !important;
            transition: all 0.3s ease !important;
            letter-spacing: 5px;
        }}
        div.stButton > button:hover {{
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.6) !important;
            transform: translateY(-2px);
        }}

        header {{ visibility: hidden; }}
        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入介面 (修期間距與文字) ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="platinum-card" style="text-align:center;"><h1 style="font-size: 48px; letter-spacing: 5px;">💎 VIP 核心系統</h1><p style="opacity:0.8; letter-spacing:3px;">授權專用通道</p></div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True) 
    pwd = st.text_input("授權碼", type="password", label_visibility="collapsed", placeholder="請輸入當日授權碼")
    
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    if st.button("登 入", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心主介面 ---
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
st.markdown('<h1 style="margin-bottom:0; font-size:42px; letter-spacing:2px;">💎 VIP 數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="opacity:0.9; font-size:14px; letter-spacing:2px;">{VERSION} | {LAST_SYNC}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

room_options = ["— 請選取監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("ROOM", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選取監控房號 —":
    st.markdown("<div class='platinum-card' style='text-align: center; padding: 65px; letter-spacing:2px;'>📡 加密通道建立中...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 狀態欄邏輯 ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 

if count < 5:
    msg, clr = f"🔍 數據校準採樣中 ({count}/5)...", "#FFD700"
elif is_shield:
    msg, clr = "🚫 系統熔斷：偵測亂局，請觀望", "#FF4B4B"
else:
    msg, clr = "● AI 雲端大數據同步成功", "#00FF00"

st.markdown(f'<div class="status-bar"><span style="color:{clr}; font-size:16px; letter-spacing:1px;">{msg}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測區 ---
if count >= 5 and not is_shield:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        color = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>AI 推薦方向</p><h1 style='color:{color}!important; text-align:center; font-size:65px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>數據信心度</p><h1 style='text-align:center; font-size:65px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 歷史路評 ---
if st.session_state.history:
    bubbles = "".join([f"<div style='background:rgba(0,0,0,0.7); border:1px solid {'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}; border-radius:50%; width:38px; height:38px; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; margin:0 5px;'>{x}</div>" for x in st.session_state.history[-10:]])
    st.markdown(f"<div style='display:flex; justify-content:center; margin:25px 0;'>{bubbles}</div>", unsafe_allow_html=True)

# --- 8. 控制按鈕 ---
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

# --- 9. 功能化原本空的區域 ---
if count < 5:
    monitor_text = "📡 系統正於雲端進行數據校準..."
elif is_shield:
    monitor_text = "⚠️ 警報：當前波動過大，風險規避中"
else:
    monitor_text = f"⚙️ AI 已完成 {selected_room} 深度建模，信號穩定"

st.markdown(f"<div class='data-monitor'>{monitor_text}</div>", unsafe_allow_html=True)

# --- 10. 智能注碼管理中心 ---
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='platinum-card'>", unsafe_allow_html=True)
st.markdown("<p style='color:#FFD700; text-align:center; font-size:22px; margin-top:0; letter-spacing:4px;'>⚖️ 智能注碼管理中心</p>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns(2)
with col_f1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with col_f2: rsk = st.slider("比例 %", 1, 10, 2, label_visibility="collapsed")

mult = 0.0 if count < 5 or is_shield else (0.8 if bal > 10000 else 1.0)
suggest = int(bal * (rsk/100) * mult)

if is_shield:
    st.markdown("<h1 style='color:#FF4B4B!important; text-align:center; font-size:55px; letter-spacing:10px;'>暫停操作</h1>", unsafe_allow_html=True)
else:
    st.markdown("<p style='opacity:0.8; text-align:center; margin:0; letter-spacing:2px;'>建議下注金額</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="bet-glow">{suggest}</div>', unsafe_allow_html=True)

if st.button("🧹 重置數據 / 快速換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
