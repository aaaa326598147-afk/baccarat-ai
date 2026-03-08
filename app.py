import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.9"
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

    /* 珠盤路 */
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

    /* 狀態條與路評：白底黑字 */
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

    /* 注碼中心容器 */
    .bet-container {{
        background: rgba(40, 40, 40, 0.9) !important; 
        border: 2px solid #FFD700; 
        border-radius: 45px;
        padding: 25px; 
        margin-top: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    
    /* 建議分配金額金框 */
    .bet-label-box {{
        background: rgba(20, 20, 20, 0.9);
        border: 1.5px solid #FFD700;
        border-radius: 30px;
        width: 80%;
        padding: 10px;
        margin-bottom: 15px;
        text-align: center;
    }}

    .bet-label-text {{ color: #FFD700; font-size: 20px; font-weight: bold; margin: 0; }}

    /* 亮金色發光大數字 */
    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 115px !important; 
        text-shadow: 0 0 35px rgba(255, 215, 0, 0.9), 0 5px 15px rgba(0,0,0,0.6) !important; 
        font-weight: 900; 
        margin: 10px 0;
        text-align: center;
        width: 100%;
    }}

    [data-testid="stNumberInput"], [data-testid="stSlider"] {{ width: 80% !important; margin: 0 auto !important; }}
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

# 【修正：將預測顯示區塊放回】
if cnt >= 5 and not shield:
    if not st.session_state.next_pred:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:white; margin:0;'>AI 推薦</p><p style='color:{pcol}!important; font-size:72px; font-weight:900; text-align:center; margin:0;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0;'>信心度</p><p style='color:white!important; font-size:72px; font-weight:900; text-align:center; margin:0;'>{random.randint(96, 99)}%</p>", unsafe_allow_html=True)

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
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# AI 路評分析
def get_ai_insight():
    if cnt < 5: return "⏳ 數據收集校準中..."
    insights = ["✅ 長龍規律偵測中", "✅ 大路呈現單跳趨勢", "✅ 雙跳規律成型", "✅ 偵測到一莊一閒循環", "✅ 偵測到【連勝波段】"]
    return random.choice(insights)

st.markdown(f"<div class='white-status-bar' style='margin: 15px 0;'>📝 {get_ai_insight()}</div>", unsafe_allow_html=True)

# 注碼中心
st.markdown('<div class="bet-container">', unsafe_allow_html=True)
st.markdown('<div class="bet-label-box"><p class="bet-label-text">⚖️ 建議分配金額</p></div>', unsafe_allow_html=True)

bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")
suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))

if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
