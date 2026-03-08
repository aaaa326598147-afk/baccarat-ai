import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.3"
# 登入與數據狀態（略過）
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華玻璃視覺 CSS ---
st.set_page_config(page_title=VERSION, layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg") # 如果您有背景圖，請放置於同目錄下
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg}");
        background-size: cover !important;
        background-position: center center !important;
    }}
    .block-container {{ padding-top: 1.5rem !important; max-width: 530px !important; }}

    /* 珠盤路格點排版（略過） */
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
        box-shadow: inset 0 0 25px rgba(0,0,0,0.5);
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
    }}

    /* 【注碼中心：黑色格改透明玻璃】 */
    .bet-container {{
        /* 【關鍵修正】：玻璃擬態效果 */
        background: rgba(255, 255, 255, 0.1) !important; /* 超低透明度白 */
        backdrop-filter: blur(20px); /* 磨砂玻璃模糊感 */
        -webkit-backdrop-filter: blur(20px); /* 兼容 Safari */
        
        /* 保留金色邊框與圓角 */
        border: 2px solid rgba(255, 215, 0, 0.6); 
        border-radius: 45px;
        padding: 30px; 
        margin-top: 25px;
        
        /* 增強陰影層次感 */
        box-shadow: 0 15px 35px rgba(0,0,0,0.4), inset 0 0 15px rgba(255,255,255,0.05);
        
        display: flex;
        flex-direction: column;
        align-items: center; /* 水平置中 */
        justify-content: center; /* 垂直置中 */
    }}
    
    .bet-label {{ 
        color: #FFD700; 
        font-size: 26px; 
        letter-spacing: 6px; 
        font-weight: bold; 
        margin-bottom: 20px;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}

    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 110px !important; 
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.9) !important; 
        font-weight: 900; 
        margin: 15px 0;
        text-align: center;
        width: 100%;
    }}

    /* 調整輸入框寬度與顏色以適應玻璃背景 */
    [data-testid="stNumberInput"] input, [data-testid="stSlider"] {{
        width: 80% !important;
        margin: 0 auto !important;
        background-color: rgba(0, 0, 0, 0.3) !important; /* 輸入框內也微透 */
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 系統流程（略過） ---
# 主介面標題與桌號（略過）
st.markdown('<h1 style="text-align:center; color:white; letter-spacing:4px;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2# 狀態條與預測顯示（略過）
st.markdown(f'<div style="background:rgba(0,0,0,0.8); border:1px solid #FFD700; border-radius:50px; padding:10px; text-align:center; color:#FFD700;">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)# --- 珠盤路與輸入按鈕（略過） ---
road_html = '<div class="road-grid">'for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

b1, b2, b3 = st.columns([2, 1, 2])def update_data(r):
    # 數據更新邏輯（略過）
    st.session_state.history.append(r)if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()# --- 【精確置中＋透明玻璃修正】注碼中心 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)
st.markdown('<p class="bet-label">⚖️ 注碼中心</p>', unsafe_allow_html=True)# 內部控制元件置中排版
bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100)) # 簡化計算邏輯用於範例st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
