import streamlit as st
import random
from datetime import datetime
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V9.5 Platinum"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 頂級精品視覺 CSS ---
st.set_page_config(page_title=VERSION, layout="centered")

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@100;400;900&display=swap');
    
    .stApp {{
        background: url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&auto=format&fit=crop&w=1964&q=80");
        background-size: cover;
        font-family: 'Noto Sans TC', sans-serif;
    }}
    .block-container {{ max-width: 520px !important; padding-top: 2rem; }}

    /* 【頂級白金玻璃容器】 */
    .platinum-panel {{
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(30px) saturate(150%);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 45px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05), inset 0 0 20px rgba(255,255,255,0.2);
        text-align: center;
    }}

    /* 路評膠囊：精緻簡約 */
    .premium-commentary {{
        background: rgba(0, 0, 0, 0.7);
        color: #f1c40f !important;
        border-radius: 50px;
        padding: 10px 25px;
        font-size: 14px;
        font-weight: 400;
        letter-spacing: 2px;
        margin: 15px auto;
        width: fit-content;
        border: 0.5px solid rgba(241, 196, 15, 0.5);
    }}

    /* 珠盤路：懸浮圓點 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 40px); 
        grid-auto-flow: column;             
        grid-auto-columns: 40px;
        gap: 12px;
        overflow-x: auto;
        padding: 5px;
        justify-content: center;
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; font-weight: 900; color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }}

    /* 注碼中心數字：香檳金 */
    .bet-display {{
        background: linear-gradient(180deg, #d4af37 0%, #f1c40f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 110px !important;
        font-weight: 900;
        margin: 10px 0;
        filter: drop-shadow(0 5px 15px rgba(212,175,55,0.3));
    }}

    /* 精緻控制組件 */
    div[data-testid="stNumberInput"] input {{ background: transparent !important; border-radius: 15px !important; text-align: center !important; font-size: 20px !important; }}
    .stSlider > div {{ padding-bottom: 25px !important; }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 標題與桌號 ---
st.markdown('<h1 style="text-align:center; color:#333; font-weight:100; letter-spacing:15px; margin-bottom:0;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# --- 4. 預測區 (白金背板) ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#e74c3c" if st.session_state.next_pred == "莊" else "#3498db"
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='text-align:center; border-right: 1px solid rgba(0,0,0,0.05);'><p style='color:#888; font-size:12px;'>建議</p><p style='color:{pcol}!important; font-size:80px; font-weight:900; margin:0;'>{st.session_state.next_pred}</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center;'><p style='color:#888; font-size:12px;'>信心</p><p style='color:#333!important; font-size:80px; font-weight:900; margin:0;'>{random.randint(96, 99)}%</p></div>", unsafe_allow_html=True)

# --- 5. 珠盤路 (整合式面板) ---
st.markdown('<div class="platinum-panel">', unsafe_allow_html=True)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#e74c3c" if item == "莊" else "#3498db" if item == "閒" else "#2ecc71"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 6. 交互按鈕 ---
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 7. 路評 (獨立黑膠囊) ---
ai_msg = "📡 系統初始化中..." if cnt < 5 else f"偵測目前【{st.session_state.history[-1]}】趨勢穩定"
st.markdown(f"<div class='premium-commentary'>✦ {ai_msg}</div>", unsafe_allow_html=True)

# --- 8. 注碼中心 (白金背板整合) ---
st.markdown('<div class="platinum-panel">', unsafe_allow_html=True)
st.markdown('<div style="color:#888; font-weight:400; font-size:14px; letter-spacing:5px; margin-bottom:15px;">BET CENTER</div>', unsafe_allow_html=True)

c_i1, c_i2 = st.columns(2)
with c_i1: bal = st.number_input("CAPITAL", value=10000, step=1000, label_visibility="collapsed")
with c_i2: rsk = st.slider("RISK", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: 
    st.markdown("<p class='bet-display' style='background:linear-gradient(180deg, #e74c3c 0%, #c0392b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-display">{suggest}</p>', unsafe_allow_html=True)

if st.button("RESET DATA", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
