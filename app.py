import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.5"
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

    /* 珠盤路樣式 (不變) */
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
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
    }}

    /* 【黑色圈起來的部分：調亮處理】 */
    .highlight-status {{
        background: rgba(80, 80, 80, 0.9) !important; /* 調亮背景色 */
        border: 1.5px solid #FFD700; 
        border-radius: 50px; 
        padding: 12px; 
        text-align: center; 
        color: #FFD700; 
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2); /* 增加微光感 */
    }}

    /* 【注碼中心：結構優化】 */
    .bet-container {{
        background: rgba(0, 0, 0, 0.85) !important; 
        border: 2px solid #FFD700; 
        border-radius: 45px;
        padding: 25px; 
        margin-top: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    
    /* 【文字放入框內修正】 */
    .bet-header-box {{
        background: rgba(50, 50, 50, 0.9);
        border: 1px solid #FFD700;
        border-radius: 30px;
        width: 90%;
        padding: 8px;
        margin-bottom: 20px;
        text-align: center;
    }}

    .bet-label {{ 
        color: #FFD700; 
        font-size: 22px; 
        letter-spacing: 4px; 
        font-weight: bold; 
        margin: 0;
    }}

    /* 【紅色圈圈修正：黑金色發光大數字】 */
    .bet-main-number {{ 
        color: #B29C5D !important; /* 暗金基色 */
        font-size: 110px !important; 
        /* 複合發光：黑色外框線 + 深金光暈 */
        text-shadow: 
            2px 2px 0px #000, 
            -2px -2px 0px #000, 
            0 0 40px rgba(178, 156, 93, 0.8),
            0 0 70px rgba(0, 0, 0, 0.9) !important; 
        font-weight: 900; 
        margin: 10px 0;
        text-align: center;
        width: 100%;
    }}

    [data-testid="stNumberInput"], [data-testid="stSlider"] {{
        width: 80% !important;
        margin: 0 auto !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入邏輯 (不變) ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="授權金鑰")
    if st.button("啟 動", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 房號與預測 ---
st.markdown('<h1 style="text-align:center; color:white; letter-spacing:4px;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 【黑色圈起來調亮：狀態條】
st.markdown(f'<div class="highlight-status">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 珠盤路顯示 (不變)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 輸入按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# 【黑色圈起來調亮：AI路評區】
ai_msg = "⏳ 校準中..." if cnt < 5 else f"✅ 目前【{st.session_state.history[-1]}】勢頭較穩"
st.markdown(f"<div class='highlight-status'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 5. 【注碼中心修正】 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)

# 【修正：將標題放入專屬黑框內，內容改為注碼建議分配】
st.markdown('<div class="bet-header-box"><p class="bet-label">⚖️ 注碼建議分配</p></div>', unsafe_allow_html=True)

bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))

# 【修正：黑金色發光大數字】
if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important; text-shadow: 0 0 20px #000 !important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
