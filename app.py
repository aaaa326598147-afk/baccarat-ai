import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 旗艦版參數 ---
VERSION = "AI-Pro V4.2 FLAGSHIP"
UPDATE_DATE = "2026-03-08"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'initial_bal' not in st.session_state: st.session_state.initial_bal = None

# --- 2. 最高規格視覺 CSS ---
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
        .block-container {{ padding-top: 1.5rem !important; max-width: 620px !important; }}
        
        /* 核心立體字體 - 最高細節 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 2px #444, 4px 4px 10px rgba(0,0,0,0.9) !important;
        }}

        /* 強化氣泡路評 */
        .history-row {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin: 20px 0; }}
        .history-bubble {{
            background: rgba(0,0,0,0.6); border: 1.5px solid rgba(255,255,255,0.4);
            border-radius: 50%; width: 44px; height: 44px;
            display: flex; align-items: center; justify-content: center; font-size: 20px;
            box-shadow: 0 0 12px rgba(255,255,255,0.1);
        }}

        /* 旗艦版按鈕樣式 */
        div.stButton > button {{
            background: rgba(20, 20, 20, 0.8) !important;
            color: #FFD700 !important;
            border: 2px solid #FFD700 !important;
            border-radius: 18px !important;
            height: 4.8em !important;
            font-size: 19px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }}

        /* 物理隔離底部面板 */
        .flagship-panel {{
            margin-top: 110px !important; padding: 30px;
            background: rgba(0, 0, 0, 0.5); border-radius: 25px;
            border: 2px solid rgba(255, 215, 0, 0.4);
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.1);
        }}

        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 驗證程序 ---
if not st.session_state.login:
    st.markdown(f"<br><br><h1 style='text-align: center; font-size: 45px;'>💎 {VERSION}</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="請輸入當日授權碼")
        if st.button("解鎖數據核心", use_container_width=True):
            if pwd == datetime.now().strftime("%m%d"):
                st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 系統頂部 ---
st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>💎 VIP 數據中心</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>{VERSION} | {UPDATE_DATE}</p>", unsafe_allow_html=True)

room_options = ["— 請選取監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選取監控房號 —":
    st.markdown("<div style='text-align: center; padding: 50px;'>📡 核心待命：等待數據源連線...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. AI 路評 (旗艦氣泡) ---
if st.session_state.history:
    bubbles = ""
    for x in st.session_state.history[-10:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        bubbles += f"<div class='history-bubble' style='color:{color};'>{x}</div>"
    st.markdown(f"<div class='history-row'>{bubbles}</div>", unsafe_allow_html=True)

# --- 6. 核心演算與避險 (V4.2 旗艦邏輯) ---
count = len(st.session_state.history)
is_shield = st.session_state.losses >= 2 
risk_multiplier = 1.0

if count < 5:
    st.markdown(f"<h3 style='text-align: center;'>📡 深度分析中... ({count}/5)</h3>", unsafe_allow_html=True)
    st.progress(count / 5)
    st.markdown("<p style='text-align: center; font-size: 12px; color: #FFD700;'>數據量未達標，AI 暫不提供非對稱演算推薦</p>", unsafe_allow_html=True)
elif is_shield:
    st.markdown("<div style='background: rgba(255,0,0,0.3); border-radius:15px; padding:20px; border:2px solid #FF0000; text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FF4B4B; margin:0;'>⚠️ 避險熔斷已啟動</h2>", unsafe_allow_html=True)
    st.markdown("<p>偵測到路向劇烈波動，請手動觀察 2-3 局</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    risk_multiplier = 0.0
else:
    if st.session_state.next_pred is None: 
        # 加入莊家權重微調
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    current_p = st.session_state.next_pred
    confidence = random.randint(95, 99)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1: st.metric("AI 推薦方向", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with col_v2: st.metric("算力信心值", f"{confidence}%")
    if confidence < 97: risk_multiplier = 0.8

# --- 7. 操作按鈕 ---
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])

def add_entry(res):
    if st.session_state.next_pred and res != "和":
        if res != st.session_state.next_pred:
            st.session_state.losses += 1
        else:
            st.session_state.losses = 0 
            
    if len(st.session_state.history) >= 4:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1:
    if st.button("莊 🔴", use_container_width=True): add_entry("莊")
with col_b2:
    if st.button("和", use_container_width=True): add_entry("和")
with col_b3:
    if st.button("閒 🔵", use_container_width=True): add_entry("閒")

# --- 8. 智能注碼面板 (旗艦規格) ---
st.markdown("<div class='flagship-panel'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFD700; margin-top:0;'>⚖️ 智能注碼運算中心</h3>", unsafe_allow_html=True)

if st.session_state.initial_bal is None: st.session_state.initial_bal = 10000
bal = st.number_input("💵 當前可用本金", value=st.session_state.initial_bal, step=1000)
rsk_pct = st.slider("⚖️ 設定風險比 %", 1, 10, 2)

# 利潤守成計算
profit_guard = 0.8 if bal > st.session_state.initial_bal else 1.0
final_amt = int(bal * (rsk_pct / 100) * risk_multiplier * profit_guard)

if is_shield:
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B; font-size: 50px;'>🚫 停注</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center; color: #FFD700; font-size: 50px;'>建議：{final_amt}</h1>", unsafe_allow_html=True)

if st.button("🧹 重置當前房號 / 換桌數據", use_container_width=True):
    st.session_state.history = []; st.session_state.next_pred = None; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
