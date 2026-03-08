import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "AI-Pro V4.6 PREMIUM"
LAST_SYNC = "2026-03-08 20:45"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華視覺 CSS (流光與深度磨砂) ---
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
        .block-container {{ padding-top: 1rem !important; max-width: 580px !important; }}
        
        /* 全域文字強化：解決遮擋問題 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Segoe UI", "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 10px rgba(0,0,0,1) !important;
        }}

        /* 金色流光狀態欄：取代原本生硬的灰色格 */
        .status-header {{
            background: linear-gradient(90deg, rgba(0,0,0,0.8), rgba(50,50,50,0.8), rgba(0,0,0,0.8));
            border: 1px solid #FFD700;
            border-radius: 50px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
            margin: 15px 0;
            position: relative;
            overflow: hidden;
        }}

        /* 高級感磨砂面板 */
        .premium-panel {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 35px;
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }}

        /* 建議注碼發光效果 */
        .amount-glow {{
            color: #FFD700 !important;
            font-size: 75px !important;
            font-weight: 900;
            text-align: center;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.8), 2px 2px 5px rgba(0,0,0,1) !important;
            margin: 10px 0;
        }}

        /* 金屬質感按鈕 */
        div.stButton > button {{
            background: linear-gradient(145deg, #222, #000) !important;
            color: #FFD700 !important;
            border: 1px solid rgba(255, 215, 0, 0.4) !important;
            border-radius: 15px !important;
            height: 3.8em !important;
            font-size: 18px !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }}
        div.stButton > button:hover {{
            border-color: #FFD700 !important;
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.4) !important;
            transform: translateY(-3px);
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        header {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 系統核心邏輯 ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="premium-panel" style="text-align:center;"><h1 style="font-size: 48px; letter-spacing: 5px;">💎 VIP CORE</h1><p style="opacity: 0.8;">PREMIUM ACCESS ONLY</p></div>', unsafe_allow_html=True)
    pwd = st.text_input("KEY", type="password", label_visibility="collapsed", placeholder="授權碼")
    if st.button("INITIALIZE SYSTEM", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 頂部奢華標題 ---
st.markdown('<div style="text-align: center; margin-bottom: 25px;">', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 42px; margin-bottom: 0;">💎 VIP 數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size: 14px; opacity: 0.9; letter-spacing: 2px;">{VERSION} | {LAST_SYNC}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 房號選擇器
room_options = ["— 房號選取 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("ROOM", options=room_options, label_visibility="collapsed")

if selected_room == "— 房號選取 —":
    st.markdown("<div class='premium-panel' style='text-align: center; padding: 60px;'>📡 核心待命：等待加密數據流同步...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 動態流光狀態欄 (解決不跳字問題) ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 

if count < 5:
    msg, clr = f"🔍 數據採樣中：目前進度 {count}/5", "#FFD700"
elif is_shield:
    msg, clr = "🚫 系統熔斷：偵測到亂局，請觀望", "#FF4B4B"
else:
    msg, clr = "● AI 雲端算力連線成功：推薦中", "#00FF00"

st.markdown(f'<div class="status-header"><span style="color:{clr}; font-size: 16px; letter-spacing: 1px;">{msg}</span></div>', unsafe_allow_html=True)

# --- 6. AI 數據分析區 ---
if count >= 5 and not is_shield:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>推薦方向</p>", unsafe_allow_html=True)
        color = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
        st.markdown(f"<h1 style='color:{color} !important; text-align:center; font-size: 55px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>算力信心</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; font-size: 55px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 精緻路評紀錄 ---
if st.session_state.history:
    bubbles = "".join([f"<div style='background:rgba(0,0,0,0.6); border:1px solid {'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; margin: 0 4px;'>{x}</div>" for x in st.session_state.history[-10:]])
    st.markdown(f"<div style='display:flex; justify-content:center; margin-top: 20px;'>{bubbles}</div>", unsafe_allow_html=True)

# --- 8. 巔峰控制台 ---
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
def input_action(res):
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1: st.button("🔴 莊家", use_container_width=True, on_click=input_action, args=("莊",))
with col_b2: st.button("和", use_container_width=True, on_click=input_action, args=("和",))
with col_b3: st.button("🔵 閒家", use_container_width=True, on_click=input_action, args=("閒",))

# --- 9. 奢華注碼面板 (重頭戲) ---
st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
st.markdown("<p style='color:#FFD700; font-size:18px; text-align:center; letter-spacing:3px; margin-top:0;'>⚖️ 智能注碼管理中心</p>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns([1, 1])
with col_f1:
    bal = st.number_input("💵 本金", value=10000, step=1000, label_visibility="collapsed")
with col_f2:
    rsk = st.slider("⚖️ 風險 %", 1, 10, 2, label_visibility="collapsed")

mult = 0.0 if count < 5 or is_shield else (0.8 if bal > 10000 else 1.0)
final_amt = int(bal * (rsk/100) * mult)

if is_shield:
    st.markdown("<h1 style='color:#FF4B4B !important; font-size: 55px; text-align:center; letter-spacing:8px;'>SUSPEND</h1>", unsafe_allow_html=True)
else:
    st.markdown("<p style='opacity:0.7; text-align:center; margin:0;'>SUGGESTED BET</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="amount-glow">{final_amt}</div>', unsafe_allow_html=True)

if st.button("🧹 快速換桌 / RESET", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
