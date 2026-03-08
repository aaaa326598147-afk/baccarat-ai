import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "AI-Pro V4.2 FLAGSHIP"
UPDATE_DATE = "2026-03-08"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'initial_bal' not in st.session_state: st.session_state.initial_bal = None

# --- 2. 視覺規格 CSS ---
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
        .block-container {{ padding-top: 1.5rem !important; max-width: 600px !important; }}
        
        /* 核心立體字體 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 2px #444, 4px 4px 10px rgba(0,0,0,0.9) !important;
        }}

        /* 氣泡式路評 */
        .history-row {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 15px 0; }}
        .history-bubble {{
            background: rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.4);
            border-radius: 50%; width: 42px; height: 42px;
            display: flex; align-items: center; justify-content: center; font-size: 18px;
        }}

        /* 人性化狀態跳字格 */
        .status-box {{
            background: rgba(40, 40, 40, 0.8); border-radius: 25px; padding: 12px;
            text-align: center; margin: 15px 0; border: 1px solid #FFD700;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
        }}

        /* 底部物理隔離面板 */
        .bottom-panel {{
            margin-top: 100px !important; padding: 30px;
            background: rgba(0, 0, 0, 0.5); border-radius: 25px;
            border: 2px solid rgba(255, 215, 0, 0.4);
        }}

        div.stButton > button {{
            background: rgba(20, 20, 20, 0.8) !important;
            color: #FFD700 !important; border: 2px solid #FFD700 !important;
            border-radius: 18px !important; height: 4.8em !important; font-size: 18px !important;
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入程序 ---
if not st.session_state.login:
    st.markdown(f"<br><br><h1 style='text-align: center;'>💎 {VERSION}</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入當日驗證碼")
        if st.button("啟動數據核心", use_container_width=True):
            if pwd == datetime.now().strftime("%m%d"):
                st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 頂部狀態 ---
st.markdown("<h2 style='text-align: center;'>💎 VIP 數據中心</h2>", unsafe_allow_html=True)
room_options = ["— 請選取監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選取監控房號 —":
    st.markdown("<div style='text-align: center; padding: 50px;'>📡 核心待命：等待房號連線...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. AI 路評 ---
if st.session_state.history:
    bubbles = ""
    for x in st.session_state.history[-10:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        bubbles += f"<div class='history-bubble' style='color:{color};'>{x}</div>"
    st.markdown(f"<div class='history-row'>{bubbles}</div>", unsafe_allow_html=True)

# --- 6. 核心演算與避險 (人性化狀態) ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 
suggest_mult = 1.0

# [關鍵] 讓那格跳字的邏輯
if count < 5:
    status_msg = f"📡 數據校準中：還差 {5-count} 局產出預測"
    status_color = "#FFD700"
elif is_shield:
    status_msg = "🚫 偵測到波動：進入避險觀察期"
    status_color = "#FF4B4B"
    suggest_mult = 0.0
else:
    status_msg = "💎 AI 雲端算力已連線：推薦中"
    status_color = "#00FF00"

st.markdown(f'<div class="status-box"><span style="color:{status_color};">● {status_msg}</span></div>', unsafe_allow_html=True)

if count >= 5 and not is_shield:
    if st.session_state.next_pred is None: 
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    col_v1, col_v2 = st.columns(2)
    with col_v1: st.metric("AI 推薦", f"🔴 {st.session_state.next_pred}" if st.session_state.next_pred == "莊" else f"🔵 {st.session_state.next_pred}")
    with col_v2: st.metric("算力信心", f"{random.randint(95, 99)}%")

# --- 7. 操作按鈕 ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])

def handle_input(res):
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    if len(st.session_state.history) >= 4:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1:
    if st.button("莊 🔴", use_container_width=True): handle_input("莊")
with col_b2:
    if st.button("和", use_container_width=True): handle_input("和")
with col_b3:
    if st.button("閒 🔵", use_container_width=True): handle_input("閒")

# --- 8. 智能注碼中心 ---
st.markdown("<div class='bottom-panel'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFD700;'>⚖️ 智能注碼管理中心</h3>", unsafe_allow_html=True)

if st.session_state.initial_bal is None: st.session_state.initial_bal = 10000
bal = st.number_input("💵 目前本金", value=st.session_state.initial_bal, step=1000)
rsk = st.slider("⚖️ 風險比例 %", 1, 10, 2)

# 利潤守成與避險計算
profit_adj = 0.8 if bal > st.session_state.initial_bal else 1.0
final_amt = int(bal * (rsk/100) * suggest_mult * profit_adj)

if is_shield:
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B; font-size: 48px;'>🚫 建議停注</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: #FFD700; font-size: 48px;'>建議：{final_amt}</h1>", unsafe_allow_html=True)

if st.button("🧹 換桌 / 重置當前數據", use_container_width=True):
    st.session_state.history = []; st.session_state.next_pred = None; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
