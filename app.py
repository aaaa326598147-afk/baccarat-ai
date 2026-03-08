import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.4"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華玻璃視覺 CSS ---
st.set_page_config(page_title=VERSION, layout="centered")

st.markdown(
    f"""
    <style>
    /* 這裡建議您保留或更換成高品質背景圖，玻璃感才會強 */
    .stApp {{
        background: #000000;
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1964&q=80");
        background-size: cover !important;
    }}
    .block-container {{ padding-top: 1.5rem !important; max-width: 530px !important; }}

    /* 【關鍵修正：注碼中心黑色框變透明玻璃】 */
    .bet-container {{
        /* 徹底去除死黑，改用霧面半透明白 */
        background: rgba(255, 255, 255, 0.08) !important; 
        backdrop-filter: blur(25px); /* 磨砂玻璃的核心：高斯模糊 */
        -webkit-backdrop-filter: blur(25px);
        
        /* 極細白金線條邊框 */
        border: 1px solid rgba(255, 215, 0, 0.4); 
        border-radius: 45px;
        padding: 35px; 
        margin-top: 25px;
        
        /* 懸浮陰影，讓玻璃浮起來 */
        box-shadow: 0 25px 50px rgba(0,0,0,0.5), inset 0 0 20px rgba(255,255,255,0.05);
        
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: center;
    }}
    
    .bet-label {{ 
        color: #FFD700; 
        font-size: 26px; 
        letter-spacing: 6px; 
        font-weight: bold; 
        margin-bottom: 20px;
        text-align: center;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}

    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 115px !important; 
        /* 增強數字光暈，在玻璃上更立體 */
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.8), 0 5px 15px rgba(0,0,0,0.5) !important; 
        font-weight: 900; 
        margin: 10px 0;
        text-align: center;
        width: 100%;
    }}

    /* 珠盤路也同步改為磨砂感，才不會顯得突兀 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        background: rgba(40, 40, 40, 0.5) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
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

    /* 控制項置中 */
    [data-testid="stNumberInput"], [data-testid="stSlider"] {{
        width: 85% !important;
        margin: 0 auto !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 系統介面 ---
st.markdown('<h1 style="text-align:center; color:white; letter-spacing:4px; font-weight:100;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 狀態條 (玻璃感)
st.markdown(f'<div style="background:rgba(255,215,0,0.1); border:1px solid rgba(255,215,0,0.4); border-radius:50px; padding:10px; text-align:center; color:#FFD700; font-size:14px;">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 珠盤路
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

# --- 4. 【透明玻璃＋精確置中】注碼中心 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)
st.markdown('<p class="bet-label">⚖️ 注碼中心</p>', unsafe_allow_html=True)

# 內部控制元件
bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100))
if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): 
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
