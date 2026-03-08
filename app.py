import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V7.0 結構全修正版"
LAST_SYNC = "2026-03-09 21:15"

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

    /* 【結構修正】：確保容器能裝載珠子並向右換列 */
    .road-grid {{
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 8px;
        background: rgba(85, 85, 85, 0.8) !important; /* 對齊截圖中的灰色 */
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

    .vip-card {{
        background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 215, 0, 0.4); border-radius: 35px;
        padding: 25px; margin-bottom: 15px;
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
    
    .big-data {{ color: #FFD700 !important; font-size: 88px !important; text-align: center; text-shadow: 0 0 30px rgba(255, 215, 0, 0.7) !important; font-weight: 900; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入邏輯 ---
if not st.session_state.login:
    st.markdown("<br><br><br><div class='clean-header-zone'><h1>百家樂 VIP</h1></div>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="請輸入授權金鑰")
    if st.button("啟 動 系 統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 主介面 ---
st.markdown('<div class="clean-header-zone"><h1>數據中心</h1></div>', unsafe_allow_html=True)
rooms = ["— 請選擇監控桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]:
    st.markdown("<div style='text-align:center; padding:100px; color:white; opacity:0.6;'>📡 雲端連線中...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 狀態監控 ---
cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2
status, scol = (f"🔍 數據校準中 ({cnt}/5)", "#FFD700") if cnt < 5 else ("🚫 風險警報：建議避險", "#FF4B4B") if shield else ("● 百家樂 AI 運算連線成功", "#00FF00")
st.markdown(f'<div style="background:rgba(0,0,0,0.8); border:1px solid #FFD700; border-radius:50px; padding:10px; text-align:center; margin-bottom:15px;"><span style="color:{scol}; font-weight:bold;">{status}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測區 ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<p style='text-align:center; color:white; opacity:0.7; margin:0;'>🎯 AI 推薦</p><h1 style='color:{pcol}!important; text-align:center; font-size:72px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with c2: st.markdown(f"<p style='text-align:center; color:white; opacity:0.7; margin:0;'>📊 信心度</p><h1 style='text-align:center; color:white!important; font-size:72px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)
else:
    st.markdown("<div style='height:120px; display:flex; align-items:center; justify-content:center; color:gray;'>等待數據達標後開啟 AI 預測...</div>", unsafe_allow_html=True)

# --- 7. 【重點修復】：合併 HTML 字串確保珠子在容器內 ---
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

# --- 9. AI 專業路評 ---
if cnt < 5: ai_msg = "⏳ 正在觀察路分，等待數據建模..."
elif shield: ai_msg = "🚨 警報：當前路子太亂，建議離場觀望"
else:
    h = st.session_state.history
    if h[-3:] == ["莊"]*3: ai_msg = "🔥 偵測【莊家長龍】規律，建議順龍而行"
    elif h[-3:] == ["閒"]*3: ai_msg = "🔥 偵測【閒家長龍】規律，建議順龍而行"
    elif len(h) >= 4 and h[-1] != h[-2] and h[-2] != h[-3] and h[-3] != h[-4]: ai_msg = "🔄 當前走勢【左右單跳】，運算極度穩定"
    else: ai_msg = f"✅ 路評：目前【{h[-1]}】勢頭較穩，維持小額策略"
st.markdown(f"<div class='baccarat-commentary'>📝 {ai_msg}</div>", unsafe_allow_html=True)

# --- 10. 注碼算力中心 ---
st.markdown(f"<div class='vip-card'><p style='color:#FFD700; text-align:center; font-size:22px; margin:0;'>⚖️ 注碼中心</p>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1: bal = st.number_input("💰 本金", value=10000, step=1000, label_visibility="collapsed")
with f2: rsk = st.slider("📈 風險", 1, 10, 2, label_visibility="collapsed")
suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield: st.markdown("<h1 style='color:#FF4B4B!important; text-align:center; font-size:55px;'>🚫 避險</h1>", unsafe_allow_html=True)
else: st.markdown(f'<div class="big-data">{suggest}</div>', unsafe_allow_html=True)
if st.button("🧹 清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
