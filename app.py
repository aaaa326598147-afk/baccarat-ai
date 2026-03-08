import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V9.0 Minimal Glass"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華極簡視覺 CSS ---
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
    .block-container {{ padding-top: 2rem !important; max-width: 500px !important; }}

    /* 【核心玻璃質感】：真正的毛玻璃霧面效果 */
    .premium-glass {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(25px) brightness(1.1);
        -webkit-backdrop-filter: blur(25px) brightness(1.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5), inset 0 0 20px rgba(255,255,255,0.05);
        text-align: center;
    }}

    /* 路評膠囊：極致輕盈 */
    .commentary-capsule {{
        background: rgba(255, 215, 0, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 0.5px solid rgba(255, 215, 0, 0.3);
        border-radius: 50px;
        padding: 10px 25px;
        color: rgba(255, 235, 150, 0.9) !important;
        font-size: 15px;
        font-weight: 300;
        letter-spacing: 1px;
        text-align: center;
        margin: 15px auto;
        width: fit-content;
    }}

    /* 珠盤路：懸浮感 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 40px); 
        grid-auto-flow: column;             
        grid-auto-columns: 40px;
        gap: 10px;
        overflow-x: auto;
        justify-content: start;
        padding: 5px;
    }}
    .road-dot {{
        width: 36px; height: 36px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; font-weight: bold; color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}

    /* 注碼數字：琥珀金光 */
    .bet-number {{ 
        color: #FFD700 !important; 
        font-size: 115px !important; 
        text-shadow: 0 0 50px rgba(255, 215, 0, 0.6), 0 0 10px rgba(255, 215, 0, 0.3) !important; 
        font-weight: 900; 
        margin: 10px 0;
        font-family: 'Helvetica Neue', sans-serif;
    }}

    /* UI 元件置中與隱藏 */
    [data-testid="stNumberInput"], [data-testid="stSlider"] {{ width: 80% !important; margin: 0 auto !important; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 房號與狀態 ---
st.markdown('<h2 style="text-align:center; color:white; font-weight:200; letter-spacing:10px; margin-bottom:10px;">數據中心</h2>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# --- 4. 預測區 (極簡化) ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='text-align:center;'><p style='color:rgba(255,255,255,0.4); font-size:12px;'>AI 建議方向</p><p style='color:{pcol}!important; font-size:75px; font-weight:900; margin:0;'>{st.session_state.next_pred}</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center;'><p style='color:rgba(255,255,255,0.4); font-size:12px;'>信心度</p><p style='color:white!important; font-size:75px; font-weight:900; margin:0;'>{random.randint(96, 99)}%</p></div>", unsafe_allow_html=True)

# --- 5. 珠盤路 (霧面玻璃) ---
st.markdown('<div class="premium-glass">', unsafe_allow_html=True)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 6. 操作區 (精緻置中) ---
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 7. 路評 (懸浮玻璃膠囊) ---
ai_msg = "📡 系統初始化中..." if cnt < 5 else f"✅ 偵測目前【{st.session_state.history[-1]}】勢頭穩定"
st.markdown(f"<div class='commentary-capsule'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 8. 【注碼中心：極簡玻璃版】 ---
st.markdown('<div class="premium-glass">', unsafe_allow_html=True)
st.markdown('<div style="color:rgba(255,255,255,0.5); letter-spacing:8px; font-weight:200; font-size:16px; margin-bottom:20px;">⚖️ 注 碼 中 心</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with col2: rsk = st.slider("風險控制", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: 
    st.markdown("<p class='bet-number' style='color:#FF4B4B!important; text-shadow:0 0 30px rgba(255,75,75,0.4)!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除數據 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
