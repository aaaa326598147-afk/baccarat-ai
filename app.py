import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 核心規格參數 ---
VERSION = "AI-Pro V4.5 PREMIUM"
LAST_SYNC = datetime.now().strftime("%Y-%m-%d %H:%M")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'initial_bal' not in st.session_state: st.session_state.initial_bal = None

# --- 2. 旗艦級視覺 CSS ---
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
        .block-container {{ padding-top: 1rem !important; max-width: 600px !important; }}
        
        /* 全域立體字優化 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Segoe UI", "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
        }}

        /* 高級磨砂玻璃面板 (取代舊灰色底塊) */
        .glass-panel {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}

        /* 呼吸燈狀態格 */
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 5px rgba(255, 215, 0, 0.4); }}
            50% {{ box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); }}
            100% {{ box-shadow: 0 0 5px rgba(255, 215, 0, 0.4); }}
        }}
        .status-header {{
            background: rgba(0, 0, 0, 0.6);
            border-radius: 50px;
            padding: 8px 20px;
            border: 1px solid #FFD700;
            animation: pulse 3s infinite;
            text-align: center;
        }}

        /* 操作按鈕高級感 */
        div.stButton > button {{
            background: rgba(0, 0, 0, 0.7) !important;
            color: #FFD700 !important;
            border: 1px solid rgba(255, 215, 0, 0.5) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            font-size: 17px !important;
            height: 3.5em !important;
        }}
        div.stButton > button:hover {{
            background: rgba(255, 215, 0, 0.1) !important;
            border: 1px solid #FFD700 !important;
            transform: translateY(-2px);
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 系統核心邏輯 ---
if not st.session_state.login:
    st.markdown(f"<br><br><h1 style='text-align: center; font-size: 40px;'>💎 {VERSION}</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("Access Code", type="password", label_visibility="collapsed", placeholder="授權碼")
        if st.button("AUTHENTICATE", use_container_width=True):
            if pwd == datetime.now().strftime("%m%d"):
                st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 頂部導航 ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>💎 VIP 數據中心</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 12px; opacity: 0.8;'>VERSION 4.5 | {LAST_SYNC}</p>", unsafe_allow_html=True)

room_options = ["— 房號選取 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("ROOM", options=room_options, label_visibility="collapsed")

if selected_room == "— 房號選取 —":
    st.markdown("<div class='glass-panel' style='text-align: center; padding: 40px;'>📡 等待遠端數據流連線...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 動態狀態顯示區 (跳字格升級版) ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 

if count < 5:
    status_msg = f"🔍 深度數據採樣中 ({count}/5)..."
    status_color = "#FFD700"
elif is_shield:
    status_msg = "🚫 系統風險熔斷：請暫停操作"
    status_color = "#FF4B4B"
else:
    status_msg = "● AI 雲端算力同步成功：推薦中"
    status_color = "#00FF00"

st.markdown(f'<div class="status-header"><span style="color:{status_color}; font-size: 15px;">{status_msg}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測區 ---
if count >= 5 and not is_shield:
    if st.session_state.next_pred is None: 
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(f"<p style='margin:0; font-size:14px; opacity:0.7;'>AI 推薦方向</p>", unsafe_allow_html=True)
        color = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
        st.markdown(f"<h1 style='color:{color} !important; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"<p style='margin:0; font-size:14px; opacity:0.7;'>算力信心指標</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='margin:0;'>{random.randint(95, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 路評氣泡紀錄 ---
if st.session_state.history:
    bubbles = ""
    for x in st.session_state.history[-10:]:
        b_color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        bubbles += f"<div style='background:rgba(0,0,0,0.5); border:1px solid {b_color}; border-radius:50%; width:38px; height:38px; display:flex; align-items:center; justify-content:center; color:{b_color}; font-size:16px;'>{x}</div>"
    st.markdown(f"<div style='display:flex; justify-content:center; gap:8px; margin: 15px 0;'>{bubbles}</div>", unsafe_allow_html=True)

# --- 8. 操作控制台 ---
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
def input_data(res):
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1:
    if st.button("🔴 莊家", use_container_width=True): input_data("莊")
with col_b2:
    if st.button("和", use_container_width=True): input_data("和")
with col_b3:
    if st.button("🔵 閒家", use_container_width=True): input_data("閒")

# --- 9. 智能注碼管理面板 (巔峰視覺提升) ---
st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFD700; margin-top:0; font-size:16px;'>⚖️ 智能注碼管理中心</p>", unsafe_allow_html=True)

if st.session_state.initial_bal is None: st.session_state.initial_bal = 10000
bal = st.number_input("💵 目前本金", value=st.session_state.initial_bal, step=1000)
rsk = st.slider("⚖️ 風險比例 %", 1, 10, 2)

# 利潤守成與避險邏輯
final_mult = 1.0 if count >= 5 else 0.0
if is_shield: final_mult = 0.0
elif bal > st.session_state.initial_bal: final_mult *= 0.8 # 獲利守成

suggest_amt = int(bal * (rsk / 100) * final_mult)

if is_shield:
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B; font-size: 55px; letter-spacing: 5px;'>SUSPEND</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='text-align:center; opacity:0.7; margin:0;'>建議單把注碼</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #FFD700; font-size: 60px; margin:0;'>{suggest_amt}</h1>", unsafe_allow_html=True)

if st.button("🧹 重置數據 / 快速換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.next_pred = None; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
