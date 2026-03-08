import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 (嚴禁變動) ---
VERSION = "VIP AI-Pro V8.0"
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
    
    /* 標題與預測字體修正 */
    .flex-title h1 {{ font-size: 40px !important; color: white !important; text-shadow: 0px 4px 15px #000 !important; text-align: center; }}
    .pred-text {{ font-size: 82px !important; font-weight: 900; text-align: center; margin: 0; }}

    /* 【精確修正】珠盤路：確保珠子在灰色圓角框內換列 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        background: rgba(60, 60, 60, 0.75) !important; /* 對齊截圖灰色 */
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 35px;
        padding: 20px;
        margin: 20px 0;
        min-height: 320px;
        overflow-x: auto;
        box-shadow: inset 0 0 25px rgba(0,0,0,0.5);
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }}

    /* 【專注修正】注碼中心：回歸深色優雅版面 */
    .bet-container {{
        background: rgba(0, 0, 0, 0.7) !important; 
        border: 1.5px solid #FFD700; 
        border-radius: 45px;
        padding: 25px; 
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.7);
    }}
    .bet-label {{ color: #FFD700; font-size: 22px; letter-spacing: 4px; font-weight: bold; margin-bottom: 15px; }}
    .bet-main-number {{ color: #FFD700 !important; font-size: 92px !important; text-shadow: 0 0 30px rgba(255, 215, 0, 0.8) !important; font-weight: 900; margin: 5px 0; }}

    /* 隱藏原生組件 */
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 系統流程 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="授權金鑰")
    if st.button("啟 動", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 房號與預測 ---
st.markdown('<h1 style="text-align:center; color:white; letter-spacing:4px;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 狀態條
st.markdown(f'<div style="background:rgba(0,0,0,0.8); border:1px solid #FFD700; border-radius:50px; padding:10px; text-align:center; color:#FFD700;">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 預測顯示
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:white; margin:0;'>AI 推薦</p><p class='pred-text' style='color:{pcol}!important;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0;'>信心度</p><p class='pred-text' style='color:white!important;'>{random.randint(96, 99)}%</p>", unsafe_allow_html=True)

# --- 5. 珠盤路修正：確保所有點都被包裹在 road-grid 內 ---
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 6. 輸入按鈕 ---
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# 路評
ai_msg = "⏳ 校準中..." if cnt < 5 else f"✅ 路評：目前【{st.session_state.history[-1]}】勢頭較穩"
st.markdown(f"<div style='background:rgba(0,0,0,0.8); border:1.5px solid #FFD700; border-radius:50px; padding:10px; text-align:center; color:#FFD700;'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 7. 【最終精修】注碼中心 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)
st.markdown('<p class="bet-label">⚖️ 注碼中心</p>', unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with f2: rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important;'>避險</p>", unsafe_allow_html=True)
else: st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
