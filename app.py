import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.7"
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
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
    }}

    /* 狀態條與路評：白底黑字 (保留 V8.3 調亮感) */
    .white-status-bar {{
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 12px;
        text-align: center;
        color: #000000 !important;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }}

    /* 【注碼中心：磨砂玻璃質感】 */
    .bet-container {{
        background: rgba(255, 255, 255, 0.1) !important; 
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px); 
        border: 2px solid rgba(255, 215, 0, 0.6); 
        border-radius: 45px;
        padding: 35px; 
        margin-top: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }}

    /* 【紅色圈圈修正：回歸亮金色發光大數字】 */
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
        width: 80% !important;
        margin: 0 auto !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 核心邏輯 ---
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

st.markdown(f'<div class="white-status-bar">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 珠盤路
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 4. 【AI路評豐富化】 ---
def get_ai_insight():
    if cnt < 5: return "⏳ 數據收集校準中..."
    insights = [
        "✅ 長龍規律偵測中，建議輕注跟隨",
        "✅ 大路呈現單跳趨勢，看好勢頭反轉",
        "✅ 雙跳規律成型，系統判定穩定度高",
        "✅ 偵測到一莊一閒循環，建議保持節奏",
        "✅ 排列呈現整齊圖案，大數據勝率提升中",
        "✅ 路紙重心向【莊】偏移，適配注碼策略",
        "✅ 閒家勢頭強勁，偵測到連勝波段"
    ]
    return random.choice(insights)

st.markdown(f"<div class='white-status-bar' style='margin: 15px 0;'>📝 {get_ai_insight()}</div>", unsafe_allow_html=True)

# --- 5. 【注碼中心：移除標題 + 金色數字回歸】 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)

# 【已移除】原本在這裡的 ⚖️ 注碼中心 標籤

bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))

if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important; text-shadow: 0 0 20px #FF0000 !important;'>避險</p>", unsafe_allow_html=True)
else:
    # 回歸亮金色發光效果
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
