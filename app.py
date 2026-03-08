import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V6.2 標準路圖版"
LAST_SYNC = "2026-03-09 01:20"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華置中視覺 CSS ---
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
    
    .block-container {{ 
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 90vh !important;
        max-width: 500px !important; 
        padding-top: 1rem !important;
    }}
    
    [data-testid="stInputWidgetInstructions"] {{ display: none !important; }}
    
    /* 標題與登入區 */
    .clean-header-zone {{ text-align: center; margin-bottom: 30px; }}
    .flex-title h1 {{ 
        font-size: 48px !important; 
        letter-spacing: 10px !important; 
        text-shadow: 0px 4px 20px rgba(0,0,0,1) !important;
        margin: 0 !important;
    }}

    /* 珠盤路核心：6顆一列換行 */
    .bead-plate-container {{
        display: flex;
        flex-wrap: wrap; /* 允許換列 */
        gap: 10px;
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 25px;
        padding: 20px;
        justify-content: flex-start;
        margin-bottom: 25px;
    }}
    .bead-column {{
        display: flex;
        flex-direction: column; /* 垂直排列 6 顆 */
        gap: 8px;
    }}
    .bead-dot {{
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: bold;
        color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }}

    /* 按鈕與卡片 */
    div.stButton > button {{
        background: linear-gradient(180deg, #333 0%, #000 100%) !important;
        color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.7) !important;
        border-radius: 20px !important;
        height: 3.5em !important;
        font-size: 20px !important;
        font-weight: bold !important;
        letter-spacing: 8px !important;
    }}
    
    .baccarat-commentary {{
        background: rgba(0, 0, 0, 0.7);
        border: 1.5px solid #FFD700;
        border-radius: 50px;
        padding: 12px;
        text-align: center;
        margin-bottom: 20px;
        color: #FFD700 !important;
        font-size: 16px;
    }}
    
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入介面 ---
if not st.session_state.login:
    st.markdown('<div class="clean-header-zone"><div class="flex-title"><h1>百家樂 VIP</h1></div><p style="letter-spacing:4px; font-size:14px; color:#EEE;">PREMIUM ACCESS ONLY</p></div>', unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="請輸入當日授權金鑰")
    if st.button("登 入", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心主介面 ---
st.markdown(f'<div class="clean-header-zone"><h1 style="font-size:32px !important; letter-spacing:5px !important;">數據中心</h1><p style="opacity:0.7; font-size:12px;">AI CLOUD SYNCING | {LAST_SYNC}</p></div>', unsafe_allow_html=True)

rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]: st.stop()

# --- 5. 珠盤路階梯顯示邏輯 ---
if st.session_state.history:
    st.markdown('<div class="bead-plate-container">', unsafe_allow_html=True)
    
    # 將歷史紀錄每 6 顆切分為一個「列 (Column)」
    history_data = st.session_state.history
    columns = [history_data[i:i + 6] for i in range(0, len(history_data), 6)]
    
    for col in columns:
        st.markdown('<div class="bead-column">', unsafe_allow_html=True)
        for item in col:
            c = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
            st.markdown(f'<div class="bead-dot" style="background:{c};">{item}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 操作按鈕 ---
b1, b2, b3 = st.columns([2, 1, 2])
def update(r):
    st.session_state.history.append(r)
    st.rerun()

if b1.button("🔴 莊", use_container_width=True): update("莊")
if b2.button("和", use_container_width=True): update("和")
if b3.button("🔵 閒", use_container_width=True): update("閒")

# --- 7. AI 路評 ---
cnt = len(st.session_state.history)
if cnt >= 5:
    h = st.session_state.history
    if h[-3:] == ["莊"]*3: ai_msg = "🔥 偵測【莊家長龍】，建議順勢"
    elif h[-3:] == ["閒"]*3: ai_msg = "🔥 偵測【閒家長龍】，建議順勢"
    elif h[-2:] == ["莊", "閒"]: ai_msg = "⚡ 走勢呈現【逢莊即跳】"
    else: ai_msg = f"✅ 路評：【{h[-1]}】勢頭較穩"
    st.markdown(f"<div class='baccarat-commentary'>📝 {ai_msg}</div>", unsafe_allow_html=True)

if st.button("🧹 清除 / 換桌", use_container_width=True):
    st.session_state.history = []
    st.rerun()
