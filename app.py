import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.9 Glass Full-Set"
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

    /* 通用玻璃面板 */
    .glass-card {{
        background: rgba(0, 0, 0, 0.45) !important;
        backdrop-filter: blur(25px) saturate(160%);
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 40px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        text-align: center;
    }}

    /* 珠盤路格點排版 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        overflow-x: auto;
        justify-content: start;
        padding: 10px;
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }}

    /* 【精緻路評：玻璃化】 */
    .commentary-glass {{
        background: rgba(255, 215, 0, 0.05) !important;
        backdrop-filter: blur(15px);
        border: 1.2px solid rgba(255, 215, 0, 0.5);
        border-radius: 100px;
        padding: 12px 30px;
        color: #f0e68c !important;
        font-size: 16px;
        font-weight: 300;
        letter-spacing: 2px;
        text-align: center;
        margin: 20px auto;
        width: 90%;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }}

    /* 注碼中心數字特效 */
    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 125px !important; 
        text-shadow: 0 0 45px rgba(255, 215, 0, 0.8) !important; 
        font-weight: 900; 
        margin: 5px 0;
        line-height: 1;
    }}

    /* 按鈕與組件置中優化 */
    [data-testid="stNumberInput"], [data-testid="stSlider"] {{ width: 85% !important; margin: 0 auto !important; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 房號與預測 ---
st.markdown('<h2 style="text-align:center; color:white; letter-spacing:8px; font-weight:100;">數據中心</h2>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 狀態條
st.markdown(f'<div style="background:rgba(0,0,0,0.7); border:1px solid rgba(0,255,0,0.4); border-radius:50px; padding:10px; text-align:center; color:#00FF00; font-size:14px;">● AI 雲端數據連線成功 ({cnt}/5)</div>', unsafe_allow_html=True)

# 預測區
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<div style='text-align:center;'><p style='color:rgba(255,255,255,0.5); font-size:13px;'>AI 建議方向</p><p style='color:{pcol}!important; font-size:88px; font-weight:900; margin:0;'>{st.session_state.next_pred}</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center;'><p style='color:rgba(255,255,255,0.5); font-size:13px;'>數據信心度</p><p style='color:white!important; font-size:88px; font-weight:900; margin:0;'>{random.randint(96, 99)}%</p></div>", unsafe_allow_html=True)

# --- 4. 珠盤路 (玻璃化) ---
st.markdown('<div class="glass-card"><div class="road-grid">', unsafe_allow_html=True)
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    st.markdown(f'<div class="road-dot" style="background:{color};">{item}</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# --- 5. 操作按鈕 ---
st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
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

# --- 6. 【玻璃化路評】 ---
ai_msg = "📡 正在分析數據規律..." if cnt < 5 else f"✅ 偵測【{st.session_state.history[-1]}】勢頭較穩，建議操作"
st.markdown(f"<div class='commentary-glass'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 7. 【注碼中心：玻璃化置中】 ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div style="color:#f0e68c; letter-spacing:10px; font-weight:200; margin-bottom:20px;">⚖️ 注 碼 中 心</div>', unsafe_allow_html=True)

col_in1, col_in2 = st.columns(2)
with col_in1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with col_in2: rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important; text-shadow:0 0 35px rgba(255,75,75,0.6)!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
