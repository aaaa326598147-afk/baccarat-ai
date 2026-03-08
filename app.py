import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V9.2 Clear Glass"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 高對比玻璃視覺 CSS ---
st.set_page_config(page_title=VERSION, layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg}");
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
    }}
    .block-container {{ padding-top: 1.5rem !important; max-width: 500px !important; }}

    /* 【強化對比玻璃面板】 */
    .premium-glass {{
        background: rgba(0, 0, 0, 0.5) !important; /* 加深底色提升文字對比 */
        backdrop-filter: blur(25px) brightness(0.8);
        border: 1.5px solid rgba(255, 215, 0, 0.4);
        border-radius: 40px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8), inset 0 0 20px rgba(255,255,255,0.05);
        text-align: center;
    }}

    /* 路評膠囊：強化深色底 */
    .commentary-capsule {{
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #FFD700;
        border-radius: 50px;
        padding: 12px 30px;
        color: #FFD700 !important; /* 純金黃色文字，確保清晰度 */
        font-size: 16px;
        font-weight: 600;
        letter-spacing: 2px;
        text-shadow: 0 2px 4px rgba(0,0,0,1); /* 文字黑色投影 */
        text-align: center;
        margin: 15px auto;
        width: 85%;
        display: flex; align-items: center; justify-content: center;
    }}

    /* 珠盤路：每 6 顆換列 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 10px;
        overflow-x: auto;
        justify-content: start;
        padding: 5px;
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}

    /* 注碼數字：強化發光與陰影 */
    .bet-number {{ 
        color: #FFD700 !important; 
        font-size: 120px !important; 
        text-shadow: 0 0 40px rgba(0, 0, 0, 1), 0 0 20px rgba(255, 215, 0, 0.8) !important; 
        font-weight: 900; 
        margin: 10px 0;
        letter-spacing: -2px;
    }}

    /* 下拉選單與輸入框：文字變粗 */
    .stNumberInput input {{ font-weight: bold !important; font-size: 18px !important; }}
    
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 房號與預測 ---
st.markdown('<h2 style="text-align:center; color:white; font-weight:900; letter-spacing:8px; text-shadow:0 4px 10px #000;">數據中心</h2>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 預測顯示 (字體加粗，增加對比)
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='text-align:center;'><p style='color:white; font-weight:bold; margin:0; text-shadow:0 2px 5px #000;'>AI 建議</p><p style='color:{pcol}!important; font-size:82px; font-weight:900; margin:0; text-shadow:0 5px 15px #000;'>{st.session_state.next_pred}</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center;'><p style='color:white; font-weight:bold; margin:0; text-shadow:0 2px 5px #000;'>信心度</p><p style='color:white!important; font-size:82px; font-weight:900; margin:0; text-shadow:0 5px 15px #000;'>{random.randint(96, 99)}%</p></div>", unsafe_allow_html=True)

# --- 4. 珠盤路 (加深玻璃感) ---
st.markdown('<div class="premium-glass">', unsafe_allow_html=True)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 5. 操作按鈕 ---
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 6. 路評 (強化對比膠囊) ---
ai_msg = "⏳ 雲端運算中..." if cnt < 5 else f"✅ 偵測目前【{st.session_state.history[-1]}】勢頭穩定"
st.markdown(f"<div class='commentary-capsule'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 7. 【注碼中心：清晰版】 ---
st.markdown('<div class="premium-glass">', unsafe_allow_html=True)
st.markdown('<div style="color:#FFD700; letter-spacing:10px; font-weight:bold; font-size:20px; margin-bottom:20px; text-shadow:0 2px 5px #000;">⚖️ 注 碼 中 心</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with col2: rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: 
    st.markdown("<p class='bet-number' style='color:#FF4B4B!important; text-shadow:0 0 30px #000!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除數據 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
