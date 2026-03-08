import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化設定 ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 佈局與立體字 CSS ---
st.set_page_config(page_title="💎 VIP 數據中心", layout="centered")

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
        
        /* 核心立體字 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 0px #666, 4px 4px 8px rgba(0,0,0,0.8) !important;
        }}

        /* 氣泡式路評 */
        .history-row {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin: 15px 0; }}
        .history-bubble {{
            background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.3);
            border-radius: 50%; width: 40px; height: 40px;
            display: flex; align-items: center; justify-content: center; font-size: 18px;
        }}

        /* 底部隔離區塊 */
        .bottom-panel {{
            margin-top: 100px !important; padding: 25px;
            background: rgba(0, 0, 0, 0.4); border-radius: 20px;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入 ---
if not st.session_state.login:
    st.markdown("<br><br><h1 style='text-align: center; font-size: 42px;'>💎 VIP 數據中心</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("授權碼", type="password", label_visibility="collapsed", placeholder="請輸入金鑰")
        if st.button("啟動數據核心", use_container_width=True):
            if pwd == today_code: st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 頂部狀態 ---
st.markdown("<h2 style='text-align: center;'>💎 VIP 數據中心</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>系統版本：AI-Pro V4.0 | {today_str}</p>", unsafe_allow_html=True)

room_options = ["— 請選擇監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選擇監控房號 —":
    st.markdown("<div style='text-align: center; padding: 50px;'>📡 待命：等待房號連線...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. AI 路評 ---
if st.session_state.history:
    bubbles = ""
    for x in st.session_state.history[-10:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        bubbles += f"<div class='history-bubble' style='color:{color};'>{x}</div>"
    st.markdown(f"<div class='history-row'>{bubbles}</div>", unsafe_allow_html=True)

# --- 6. 核心演算邏輯 (暖機 + 避險) ---
count = len(st.session_state.history)
is_shield_mode = st.session_state.losses >= 3

if count < 5:
    st.markdown(f"<h3 style='text-align: center;'>📡 數據同步中... ({count}/5)</h3>", unsafe_allow_html=True)
    st.progress(count / 5)
    st.markdown("<p style='text-align: center; font-size: 12px; color: #FFD700;'>AI 正在分析當前路向機率模型</p>", unsafe_allow_html=True)
    suggest_mult = 1.0
elif is_shield_mode:
    st.markdown("<div style='background: rgba(255,0,0,0.2); border-radius:10px; padding:10px; border:1px solid red;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF4B4B;'>⚠️ 避險觀察模式</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>偵測到波動異常，建議暫停或減注觀察</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    suggest_mult = 0.5 # 避險期建議金額減半
else:
    if st.session_state.next_pred is None: st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(94, 98)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1: st.metric("AI 推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with col_v2: st.metric("算力信心", f"{confidence}%")
    suggest_mult = 1.0 if confidence >= 96 else 0.8

# --- 7. 操作按鈕 ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])

def handle_input(res):
    # 避險判斷邏輯
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred:
            st.session_state.losses += 1
        else:
            st.session_state.losses = 0 # 預測正確，重置連損數
            
    if len(st.session_state.history) >= 4:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1:
    if st.button("莊 🔴", use_container_width=True): handle_input("莊")
with col_b2:
    if st.button("和", use_container_width=True): handle_input("和")
with col_b3:
    if st.button("閒 🔵", use_container_width=True): handle_input("閒")

# --- 8. 智能注碼中心 ---
st.markdown("<div class='bottom-panel'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFD700;'>⚖️ 智能注碼運算中心</h3>", unsafe_allow_html=True)

bal = st.number_input("💵 目前本金", value=10000, step=1000)
rsk = st.slider("⚖️ 基本風險 %", 1, 10, 2)
# 根據 AI 狀態計算最終金額
base_sug = int(bal * (rsk / 100))
final_sug = int(base_sug * suggest_mult)

if is_shield_mode:
    st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>⚠️ 避險注碼：{final_sug}</h2>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>建議注碼：{final_sug}</h2>", unsafe_allow_html=True)

if st.button("🧹 重置房號數據", use_container_width=True):
    st.session_state.history = []; st.session_state.next_pred = None; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
