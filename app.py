import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V6.1 旗艦登入版"
LAST_SYNC = "2026-03-09 01:00"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華至中視覺 CSS ---
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
        image-rendering: -webkit-optimize-contrast;
    }}
    
    /* 置中核心佈局控制 */
    .block-container {{ 
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 90vh !important;
        max-width: 500px !important; 
        padding-top: 0 !important;
    }}
    
    [data-testid="stInputWidgetInstructions"] {{ display: none !important; }}
    
    /* 旗艦標題樣式 (移除系統二字) */
    .clean-header-zone {{ 
        text-align: center; 
        margin-bottom: 40px; 
        background: none !important; 
    }}
    .flex-title {{ 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        gap: 20px; 
    }}
    .flex-title h1 {{ 
        margin: 0 !important; 
        font-size: 52px !important; 
        letter-spacing: 12px !important; 
        text-shadow: 0px 0px 30px rgba(255,255,255,0.4), 0px 4px 20px rgba(0,0,0,1) !important;
        color: #FFFFFF !important;
    }}
    .diamond-icon {{ 
        font-size: 42px; 
        filter: drop-shadow(0 0 20px rgba(0, 191, 255, 0.9)); 
    }}

    /* 輸入框高級感 */
    .stTextInput input {{
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 215, 0, 0.6) !important;
        border-radius: 15px !important;
        height: 55px !important;
        font-size: 18px !important;
        text-align: center !important;
        color: #333 !important;
        text-shadow: none !important;
    }}

    /* 登入按鈕強化 */
    div.stButton > button {{
        background: linear-gradient(180deg, #333 0%, #000 100%) !important;
        color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.8) !important;
        border-radius: 20px !important;
        height: 3.5em !important;
        font-size: 22px !important;
        font-weight: bold !important;
        letter-spacing: 15px !important;
        text-indent: 15px; /* 修正間距導致的文字偏移 */
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        transition: 0.3s all;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.3) !important;
    }}

    /* 專業術語與數據卡片樣式 */
    .vip-card {{
        background: rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 215, 0, 0.5);
        border-radius: 40px;
        padding: 30px;
    }}
    
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入介面 (至中旗艦版) ---
if not st.session_state.login:
    # 標題區
    st.markdown('''
        <div class="clean-header-zone">
            <div class="flex-title">
                <span class="diamond-icon">💎</span>
                <h1>百家樂 VIP</h1>
                <span class="diamond-icon">💎</span>
            </div>
            <p style="opacity:0.9; letter-spacing:6px; font-size:16px; margin-top:10px; color:#FFFFFF; text-shadow: 0 2px 10px #000;">PREMIUM ACCESS ONLY</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # 輸入區
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="請輸入當日授權金鑰")
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) 
    
    # 登入按鈕
    if st.button("登 入", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心主介面 (登入後) ---
st.markdown(f'''
    <div class="clean-header-zone">
        <div class="flex-title">
            <span class="diamond-icon">💎</span>
            <h1 style="font-size:38px !important;">數據中心</h1>
            <span class="diamond-icon">💎</span>
        </div>
        <p style="opacity:0.8; font-size:14px; letter-spacing:3px; color:#FFFFFF;">AI CLOUD SYNCING | {LAST_SYNC}</p>
    </div>
''', unsafe_allow_html=True)

# (其餘數據邏輯與階梯路圖保持 V6.0 高規格配置)
rooms = ["— 請選擇監控桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]:
    st.markdown("<div style='text-align:center; padding:80px; color:#FFFFFF; opacity:0.7;'>📡 雲端連線中...</div>", unsafe_allow_html=True)
    st.stop()

# 數據監控欄
cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2
status, scol = (f"🔍 校準中 ({cnt}/5)", "#FFD700") if cnt < 5 else ("🚫 風險避險", "#FF4B4B") if shield else ("● AI 連線成功", "#00FF00")
st.markdown(f'<div style="background:rgba(0,0,0,0.85); border:1px solid #FFD700; border-radius:60px; padding:12px; text-align:center; margin-bottom:20px;"><span style="color:{scol}; font-weight:bold;">{status}</span></div>', unsafe_allow_html=True)

# 階梯路單 (Road Grid)
if st.session_state.history:
    st.markdown('<div style="display:grid; grid-template-columns:repeat(6, 1fr); gap:8px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,215,0,0.3); border-radius:20px; padding:15px; margin-bottom:20px;">', unsafe_allow_html=True)
    for item in st.session_state.history[-18:]:
        c = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
        st.markdown(f'<div style="background:{c}; width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; color:white; box-shadow:0 4px 10px rgba(0,0,0,0.3);">{item}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 操作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update(r):
    st.session_state.history.append(r); st.rerun()
if b1.button("🔴 莊", use_container_width=True): update("莊")
if b2.button("和", use_container_width=True): update("和")
if b3.button("🔵 閒", use_container_width=True): update("閒")
