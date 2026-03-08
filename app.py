import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.6"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華視覺 CSS ---
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
    }}
    .block-container {{ padding-top: 1.5rem !important; max-width: 530px !important; }}

    /* 珠盤路 (不變) */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        background: rgba(60, 60, 60, 0.75) !important;
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 35px;
        padding: 20px;
        margin: 20px 0;
        min-height: 320px;
        overflow-x: auto;
    }}

    /* 【黑色圈起調亮：狀態條與路評】 */
    .highlight-status {{
        background: rgba(80, 80, 80, 0.9) !important; 
        border: 1.5px solid #FFD700; 
        border-radius: 50px; 
        padding: 12px; 
        text-align: center; 
        color: #FFD700; 
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        font-weight: bold;
    }}

    /* 【注碼中心：黑色外框】 */
    .bet-container {{
        background: rgba(40, 40, 40, 0.95) !important; 
        border: 2px solid #FFD700; 
        border-radius: 45px;
        padding: 25px; 
        margin-top: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}
    
    /* 【注碼中心標題：格內封閉】 */
    .bet-header-box {{
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #FFD700;
        border-radius: 30px;
        width: 85%;
        padding: 10px;
        margin-bottom: 20px;
        text-align: center;
    }}

    .bet-label {{ 
        color: #FFD700; 
        font-size: 24px; 
        letter-spacing: 5px; 
        font-weight: bold; 
        margin: 0;
    }}

    /* 【回歸經典：金色發光大數字】 */
    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 115px !important; 
        text-shadow: 0 0 35px rgba(255, 215, 0, 0.9), 0 5px 15px rgba(0,0,0,0.6) !important; 
        font-weight: 900; 
        margin: 15px 0;
        text-align: center;
        width: 100%;
    }}

    [data-testid="stNumberInput"], [data-testid="stSlider"] {{
        width: 85% !important;
        margin: 0 auto !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入與房號 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="授權金鑰")
    if st.button("啟 動", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

st.markdown('<h1 style="text-align:center; color:white; letter-spacing:4px;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 狀態條 (調亮版)
st.markdown(f'<div class="highlight-status">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 珠盤路 (不變)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 按鈕區
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# 路評區 (調亮版)
ai_msg = "⏳ 校準中..." if cnt < 5 else f"✅ 分析完成，長龍規律偵測中"
st.markdown(f"<div class='highlight-status'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 4. 【注碼中心：經典回歸修正】 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)

# 標題收進框內
st.markdown('<div class="bet-header-box"><p class="bet-label">⚖️ 注碼中心</p></div>', unsafe_allow_html=True)

bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))

# 回歸金色數字
if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important; text-shadow: 0 0 20px #FF0000 !important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
