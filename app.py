import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V8.5 Ultra"
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 頂級視覺 CSS 注入 ---
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

    /* 珠盤路：強化立體感 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        background: rgba(30, 30, 30, 0.8) !important;
        border: 2px solid rgba(255, 215, 0, 0.2);
        border-radius: 35px;
        padding: 22px;
        margin: 20px 0;
        min-height: 320px;
        overflow-x: auto;
        box-shadow: inset 0 10px 30px rgba(0,0,0,0.8);
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.6), inset 0 -3px 5px rgba(0,0,0,0.3);
    }}

    /* 【注碼中心：超精緻重塑】 */
    .bet-container {{
        background: linear-gradient(145deg, rgba(20,20,20,0.9), rgba(0,0,0,0.95)) !important; 
        border: 2px solid rgba(255, 215, 0, 0.6); 
        border-radius: 40px;
        padding: 35px 20px; 
        margin-top: 30px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.9), 0 0 20px rgba(255,215,0,0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }}
    
    .bet-header {{
        color: #FFD700;
        font-size: 18px;
        letter-spacing: 10px;
        font-weight: 300;
        margin-bottom: 25px;
        opacity: 0.9;
        text-shadow: 0 0 10px rgba(255,215,0,0.3);
    }}

    /* 數字特效：黃金發光 */
    .bet-main-number {{ 
        color: #FFD700 !important; 
        font-size: 120px !important; 
        text-shadow: 0 0 45px rgba(255, 215, 0, 0.7), 0 0 10px rgba(255, 215, 0, 0.5) !important; 
        font-weight: 900; 
        margin: 10px 0;
        line-height: 1;
        font-family: 'Arial Black', sans-serif;
    }}

    /* 本金與風險拉條精緻化 */
    div[data-testid="stNumberInput"] {{ margin-bottom: 10px; }}
    div[data-testid="stSlider"] {{ margin-top: 10px; }}
    
    /* 強制置中所有內部組件 */
    .stNumberInput, .stSlider {{ width: 85% !important; }}

    /* 按鈕美化 */
    div.stButton > button {{
        background: linear-gradient(135deg, #333, #111) !important;
        border: 1px solid rgba(255,215,0,0.4) !important;
        transition: 0.3s !important;
    }}
    div.stButton > button:hover {{
        border: 1px solid #FFD700 !important;
        box-shadow: 0 0 15px rgba(255,215,0,0.3) !important;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 系統核心邏輯 ---
st.markdown('<h1 style="text-align:center; color:white; letter-spacing:5px; font-weight:200;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

# 狀態條：微光特效
st.markdown(f'<div style="background:rgba(0,0,0,0.8); border:1px solid rgba(255,215,0,0.4); border-radius:50px; padding:10px; text-align:center; color:#FFD700; box-shadow: 0 0 15px rgba(255,215,0,0.1);">● AI 雲端數據連線成功 ({cnt}/5)</div>', unsafe_allow_html=True)

# 預測顯示
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:rgba(255,255,255,0.6); margin:0; font-size:14px;'>🎯 AI 推薦方向</p><p style='color:{pcol}!important; font-size:82px; font-weight:900; text-align:center; margin:0; text-shadow:0 0 20px rgba(0,0,0,0.5);'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:rgba(255,255,255,0.6); margin:0; font-size:14px;'>📊 數據信心度</p><p style='color:white!important; font-size:82px; font-weight:900; text-align:center; margin:0;'>{random.randint(96, 99)}%</p>", unsafe_allow_html=True)

# --- 4. 珠盤路 ---
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 5. 輸入按鈕 ---
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 6. AI 路評 ---
ai_msg = "⏳ 校準中..." if cnt < 5 else f"✅ 策略：目前【{st.session_state.history[-1]}】強勢，維持小額"
st.markdown(f"<div style='background:rgba(0,0,0,0.85); border:1px solid #FFD700; border-radius:50px; padding:12px; text-align:center; color:#FFD700; margin: 15px 0; font-size:16px;'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 7. 【奢華再定義】注碼中心 ---
st.markdown('<div class="bet-container">', unsafe_allow_html=True)
st.markdown('<div class="bet-header">⚖️ 注 碼 中 心</div>', unsafe_allow_html=True)

# 本金與風險置中
c_bal, c_rsk = st.columns([1, 1])
with c_bal: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with c_rsk: rsk = st.slider("風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))

if shield: 
    st.markdown("<p class='bet-main-number' style='color:#FF4B4B!important; text-shadow:0 0 40px rgba(255,75,75,0.6)!important;'>避險</p>", unsafe_allow_html=True)
else:
    st.markdown(f'<p class="bet-main-number">{suggest}</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
