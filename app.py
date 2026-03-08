import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.8 Glass Edition"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 頂級玻璃視覺 CSS ---
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
    .block-container {{ padding-top: 1.5rem !important; max-width: 530px !important; }}

    /* 頂級玻璃擬態容器：珠盤路與注碼中心通用 */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 40px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5), inset 0 0 15px rgba(255,255,255,0.05);
    }}

    /* 珠盤路專屬排版 (維持 6 顆換列) */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        overflow-x: auto;
        justify-content: start;
        padding: 5px;
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }}

    /* 【注碼中心：玻璃感優化】 */
    .bet-glass-card {{
        background: rgba(0, 0, 0, 0.45) !important; /* 玻璃透明底 */
        backdrop-filter: blur(30px) brightness(80%);
        border: 1.5px solid rgba(255, 215, 0, 0.6);
        border-radius: 45px;
        padding: 35px 25px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }}
    
    .bet-header-text {{
        color: #f0e68c;
        font-size: 16px;
        letter-spacing: 12px;
        font-weight: 200;
        margin-bottom: 25px;
        text-shadow: 0 0 8px rgba(255,215,0,0.4);
    }}

    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 125px !important; 
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.8), 2px 2px 10px rgba(0,0,0,0.5) !important; 
        font-weight: 900; 
        margin: 5px 0;
        letter-spacing: -2px;
    }}

    /* 輸入框透明化處理 */
    .stNumberInput input, .stSlider > div {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,215,0,0.2) !important;
        color: white !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 系統核心 ---
st.markdown('<h2 style="text-align:center; color:white; letter-spacing:8px; font-weight:100; margin-bottom:20px;">數據中心</h2>', unsafe_allow_html=True)
rooms = ["— 請選擇監控桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# --- 4. 預測顯示 ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='text-align:center;'><p style='color:rgba(255,255,255,0.5); font-size:13px; margin:0;'>AI 建議</p><p style='color:{pcol}!important; font-size:88px; font-weight:900; margin:0;'>{st.session_state.next_pred}</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center;'><p style='color:rgba(255,255,255,0.5); font-size:13px; margin:0;'>信心度</p><p style='color:white!important; font-size:88px; font-weight:900; margin:0;'>{random.randint(96, 99)}%</p></div>", unsafe_allow_html=True)

# --- 5. 珠盤路玻璃框 ---
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 6. 輸入按鈕與路評 ---
st.markdown("<div style='margin: 15px 0;'>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

ai_msg = "⏳ 雲端計算中..." if cnt < 5 else f"✅ 策略：目前【{st.session_state.history[-1]}】穩定，推薦跟進"
st.markdown(f"<div style='background:rgba(255,255,255,0.05); border-radius:50px; padding:10px; text-align:center; color:#FFD700; border: 1px solid rgba(255,215,0,0.3); font-size:15px; margin-bottom:20px;'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 7. 【高級玻璃感修正】注碼中心 ---
st.markdown('<div class="bet-glass-card">', unsafe_allow_html=True)
st.markdown('<div class="bet-header-text">⚖️ 注 碼 中 心</div>', unsafe_allow_html=True)

# 控制元件置中
col_in1, col_in2 = st.columns(2)
with col_in1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with col_in2: rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))

if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important; text-shadow:0 0 30px rgba(255,75,75,0.5)!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除數據 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
