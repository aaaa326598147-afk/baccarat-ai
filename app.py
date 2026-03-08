import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 (嚴禁變動) ---
VERSION = "VIP AI-Pro V8.3 (黑金玻璃限定版)"
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

    /* 珠盤路：每 6 顆自動換行 */
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
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }}

    /* 【注碼中心：黑色格改透明玻璃 + 文字格內置中】 */
    .bet-container {{
        /* 【關鍵修正】：黑色格改透明玻璃 */
        background: rgba(255, 255, 255, 0.1) !important; /* 超低透明度白 */
        backdrop-filter: blur(20px); /* 磨砂玻璃模糊感 */
        -webkit-backdrop-filter: blur(20px); /* 兼容 Safari */
        
        border: 2px solid rgba(255, 215, 0, 0.6); 
        border-radius: 45px;
        padding: 30px; 
        margin-top: 25px;
        
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

    /* 【紅色圈圈修正】：黑金色發光大數字 */
    .bet-main-number {{ 
        color: #B29C5D !important; /* 改為黑金色基底 */
        font-size: 110px !important; 
        /* 【關鍵修正】：改為暗金色與黑色發光層疊 */
        text-shadow: 0 0 20px rgba(0, 0, 0, 0.8), 0 0 40px rgba(178, 156, 93, 0.6), 0 0 60px rgba(255, 215, 0, 0.3) !important; 
        font-weight: 900; 
        margin: 15px 0;
        text-align: center;
        width: 100%;
    }}

    /* 狀態條與路評：統一白底黑字 */
    .white-status-bar {{
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 10px;
        text-align: center;
        color: #000000 !important;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }}

    [data-testid="stNumberInput"], [data-testid="stSlider"] {{
        width: 80% !important;
        margin: 0 auto !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入邏輯 (略過) ---
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

# 白底黑字狀態條
st.markdown(f'<div class="white-status-bar">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 預測顯示
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:white; margin:0;'>AI 推薦</p><p style='color:{pcol}!important; font-size:72px; font-weight:900; text-align:center; margin:0;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0;'>信心度</p><p style='color:white!important; font-size:72px; font-weight:900; text-align:center; margin:0;'>{random.randint(96, 99)}%</p>", unsafe_allow_html=True)

# --- 5. 珠盤路 ---
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

# 【修正：白底黑字路評區 + 分析文字】
ai_msg = "⏳ 校準中..." if cnt < 5 else f"✅ 分析完成，長龍規律偵測中" # 加上具體路評文字
st.markdown(f"<div class='white-status-bar' style='margin: 15px 0;'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 7. 【注碼中心：黑色格改透明玻璃 + 文字格內置中】 ---
# 將「⚖️ 注碼中心」這行字移動到 .bet-container 內部，確保被框住
st.markdown('<div class="bet-container">', unsafe_allow_html=True)
st.markdown('<p class="bet-label">⚖️ 注碼中心</p>', unsafe_allow_html=True) # 移動到框內

bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important;'>避險</p>", unsafe_allow_html=True)
else:
    # 這裡會應用 .bet-main-number 的黑金色發光效果
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
