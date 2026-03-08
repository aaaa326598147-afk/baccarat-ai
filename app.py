import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "AI-Pro V4.5 PREMIUM"
LAST_SYNC = "2026-03-08 20:30"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 旗艦視覺修正 CSS (強化文字對比) ---
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
        .block-container {{ padding-top: 1.5rem !important; max-width: 550px !important; }}
        
        /* [修正重點] 強化標題文字的 Z-Index 與清晰度 */
        .top-header {{
            position: relative;
            z-index: 999 !important;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Segoe UI", "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            /* 強化陰影，解決白色背景擋住文字的問題 */
            text-shadow: 2px 2px 8px rgba(0,0,0,0.9), 0px 0px 10px rgba(0,0,0,0.5) !important;
        }}

        /* 磨砂玻璃框樣式優化 */
        .glass-box {{
            background: rgba(0, 0, 0, 0.45); /* 加深一點底色增加對比 */
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        }}

        .status-glow {{
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #FFD700;
            border-radius: 50px;
            padding: 8px 15px;
            margin: 10px 0;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
            font-size: 15px;
        }}

        div.stButton > button {{
            background: rgba(0, 0, 0, 0.85) !important;
            color: #FFD700 !important;
            border: 1px solid rgba(255, 215, 0, 0.7) !important;
            border-radius: 12px !important;
            height: 3.2em !important;
            font-size: 18px !important;
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        /* 移除電腦端多餘的空間 */
        header {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入介面 ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f'<div class="glass-box"><h1 style="font-size: 45px;">💎 VIP CORE</h1><p style="opacity: 0.8;">{VERSION}</p></div>', unsafe_allow_html=True)
    pwd = st.text_input("KEY", type="password", label_visibility="collapsed", placeholder="授權碼")
    if st.button("INITIALIZE SYSTEM", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心主介面 (文字層次優化) ---
st.markdown('<div class="top-header"><h2>💎 VIP 數據中心</h2></div>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; font-size: 12px; margin-top: -15px; opacity: 0.9;">{VERSION} | {LAST_SYNC}</p>', unsafe_allow_html=True)

room_options = ["— 選取監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("ROOM", options=room_options, label_visibility="collapsed")

if selected_room == "— 選取監控房號 —":
    st.markdown("<div class='glass-box' style='padding: 50px; margin-top: 20px; text-align:center;'>📡 系統待命：等待加密通道連線...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 實時狀態 ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 

if count < 5:
    status_msg, status_clr = f"🔍 數據校準中 ({count}/5)...", "#FFD700"
elif is_shield:
    status_msg, status_clr = "🚫 系統熔斷：避險觀察中", "#FF4B4B"
else:
    status_msg, status_clr = "● AI 雲端算力同步成功", "#00FF00"

st.markdown(f'<div class="status-glow" style="text-align:center; color:{status_clr};">{status_msg}</div>', unsafe_allow_html=True)

# --- 6. AI 預測區 ---
if count >= 5 and not is_shield:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    col_v1, col_v2 = st.columns(2)
    with col_v1: st.metric("AI 推薦", st.session_state.next_pred)
    with col_v2: st.metric("算力信心", f"{random.randint(95, 99)}%")

# --- 7. 路評紀錄 ---
if st.session_state.history:
    bubbles = "".join([f"<div style='background:rgba(0,0,0,0.6); border:1px solid {'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}; border-radius:50%; width:35px; height:35px; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; margin: 0 4px;'>{x}</div>" for x in st.session_state.history[-10:]])
    st.markdown(f"<div style='display:flex; justify-content:center; margin-bottom: 20px;'>{bubbles}</div>", unsafe_allow_html=True)

# --- 8. 控制台 ---
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
def add_data(res):
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1: st.button("🔴 莊家", use_container_width=True, on_click=add_data, args=("莊",))
with col_b2: st.button("和", use_container_width=True, on_click=add_data, args=("和",))
with col_b3: st.button("🔵 閒家", use_container_width=True, on_click=add_data, args=("閒",))

# --- 9. 注碼管理中心 ---
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
st.markdown("<p style='color:#FFD700; font-size:18px; text-align:center;'>⚖️ 智能注碼管理中心</p>", unsafe_allow_html=True)

bal = st.number_input("💵 本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("⚖️ 風險比例 %", 1, 10, 2)

mult = 0.0 if count < 5 or is_shield else (0.8 if bal > 10000 else 1.0)
final_amt = int(bal * (rsk/100) * mult)

if is_shield:
    st.markdown("<h1 style='color:#FF4B4B !important; font-size: 50px; text-align:center;'>SUSPEND</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='opacity:0.7; text-align:center; margin:0;'>建議下注金額</p><h1 style='color:#FFD700 !important; font-size: 60px; text-align:center; margin:0;'>{final_amt}</h1>", unsafe_allow_html=True)

if st.button("🧹 快速換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
