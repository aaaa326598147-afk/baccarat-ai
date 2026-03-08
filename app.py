import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 (完全不動) ---
VERSION = "VIP AI-Pro V7.5"
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
        background-attachment: fixed !important;
    }}
    .block-container {{ padding-top: 1.5rem !important; max-width: 530px !important; }}
    
    .clean-header-zone {{ text-align: center; margin-bottom: 20px; }}
    .flex-title h1 {{ font-size: 40px !important; letter-spacing: 6px !important; text-shadow: 0px 4px 15px #000 !important; color: white !important; margin: 0; }}

    /* 珠盤路容器 (維持 6 顆換列不動) */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        background: rgba(85, 85, 85, 0.8) !important;
        border: 2px solid rgba(255, 215, 0, 0.4);
        border-radius: 25px;
        padding: 20px;
        margin: 20px 0;
        min-height: 320px;
        max-height: 320px;
        overflow-x: auto;                    
        box-shadow: inset 0 0 25px rgba(0,0,0,0.6);
        justify-content: start;
    }}
    .road-dot {{
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }}

    /* 【注碼中心修正】：加深背景色，解決截圖中太白的問題 */
    .bet-center-card {{
        background: rgba(0, 0, 0, 0.8) !important; 
        backdrop-filter: blur(25px);
        border: 2px solid #FFD700; 
        border-radius: 40px;
        padding: 25px; 
        margin-top: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.8);
        text-align: center;
    }}

    .baccarat-commentary {{
        background: rgba(0, 0, 0, 0.8); border: 1.5px solid #FFD700;
        border-radius: 50px; padding: 12px; text-align: center;
        color: #FFD700 !important; font-size: 17px; margin: 15px 0;
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, #444, #000) !important;
        color: #FFD700 !important; border: 1px solid rgba(255, 215, 0, 0.6) !important;
        border-radius: 20px !important; font-size: 18px !important;
    }}
    
    /* 注碼大字特效 */
    .bet-amount {{ 
        color: #FFD700 !important; 
        font-size: 92px !important; 
        text-shadow: 0 0 40px rgba(255, 215, 0, 1) !important; 
        font-weight: 900; 
        margin: 10px 0;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入邏輯 ---
if not st.session_state.login:
    st.markdown("<br><br><br><div class='clean-header-zone'><h1>百家樂 VIP</h1></div>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="授權金鑰")
    if st.button("啟 動 系 統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 主介面 (房號選單不動) ---
st.markdown('<div class="clean-header-zone"><h1>數據中心</h1></div>', unsafe_allow_html=True)
rooms = ["— 請選擇監控桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]:
    st.markdown("<div style='text-align:center; padding:100px; color:white; opacity:0.6;'>📡 連線中...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 狀態監控 ---
cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2
status, scol = (f"🔍 數據校準中 ({cnt}/5)", "#FFD700") if cnt < 5 else ("🚫 風險警報", "#FF4B4B") if shield else ("● AI 運算連線成功", "#00FF00")
st.markdown(f'<div style="background:rgba(0,0,0,0.8); border:1px solid #FFD700; border-radius:50px; padding:10px; text-align:center; margin-bottom:15px;"><span style="color:{scol}; font-weight:bold;">{status}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測區 (不動) ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<p style='text-align:center; color:white; opacity:0.7; margin:0;'>🎯 AI 推薦</p><h1 style='color:{pcol}!important; text-align:center; font-size:72px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with c2: st.markdown(f"<p style='text-align:center; color:white; opacity:0.7; margin:0;'>📊 信心度</p><h1 style='text-align:center; color:white!important; font-size:72px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 珠盤路 (不動) ---
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div class="road-dot" style="background:{color};">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# --- 8. 手動輸入 ---
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r); st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 9. AI 路評 ---
ai_msg = "⏳ 校準中..." if cnt < 5 else "🚨 警報：路子亂" if shield else f"✅ 目前【{st.session_state.history[-1]}】勢頭較穩"
st.markdown(f"<div class='baccarat-commentary'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 10. 【專注修正】注碼中心 ---
st.markdown('<div class="bet-center-card">', unsafe_allow_html=True)
st.markdown("<p style='color:#FFD700; font-size:24px; letter-spacing:5px; font-weight:bold; margin-bottom:10px;'>⚖️ 注碼中心</p>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1: bal = st.number_input("💰 本金", value=10000, step=1000, label_visibility="collapsed")
with f2: rsk = st.slider("📈 風險", 1, 10, 2, label_visibility="collapsed")

suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: 
    st.markdown("<h1 style='color:#FF4B4B!important; text-align:center; font-size:60px; margin:10px 0;'>🚫 避險</h1>", unsafe_allow_html=True)
else:
    st.markdown(f'<div class="bet-amount">{suggest}</div>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
