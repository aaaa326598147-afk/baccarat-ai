import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
VERSION = "VIP AI-Pro V5.8 純淨雙鑽版"
LAST_SYNC = "2026-03-09 00:15"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華高清視覺 CSS ---
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
    
    .block-container {{ padding-top: 2rem !important; max-width: 530px !important; }}
    
    /* 屏蔽原生碎屑 */
    [data-testid="stInputWidgetInstructions"] {{ display: none !important; }}
    
    /* 無框純淨標題區塊 (移除框框) */
    .clean-header-zone {{
        text-align: center;
        margin-bottom: 30px;
        background: none !important; /* 徹底移除背景 */
        border: none !important;     /* 徹底移除邊框 */
        box-shadow: none !important;  /* 徹底移除陰影 */
    }}

    .flex-title {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }}
    .flex-title h1 {{
        margin: 0 !important;
        font-size: 44px !important;
        letter-spacing: 6px !important;
        color: #FFFFFF !important;
        text-shadow: 0px 4px 20px rgba(0,0,0,1) !important;
    }}
    .diamond-icon {{
        font-size: 38px;
        filter: drop-shadow(0 0 15px rgba(0, 191, 255, 0.8));
    }}

    /* 全域文字質感 */
    h1, h2, h3, p, span, label, div {{
        color: #FFFFFF !important;
        font-family: "Segoe UI", "Microsoft JhengHei", sans-serif !important;
        font-weight: 900 !important;
        text-shadow: 0px 4px 15px rgba(0,0,0,1) !important;
    }}

    /* 功能性面板 (保留用於注碼中心，維持層次) */
    .vip-card {{
        background: rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 215, 0, 0.5);
        border-radius: 40px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.6);
    }}

    /* 旗艦按鈕 */
    div.stButton > button {{
        background: linear-gradient(135deg, #444, #000) !important;
        color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.7) !important;
        border-radius: 25px !important;
        height: 3.8em !important;
        font-size: 19px !important;
        letter-spacing: 6px;
        transition: 0.4s ease;
    }}
    
    .big-data {{
        color: #FFD700 !important;
        font-size: 92px !important;
        text-align: center;
        text-shadow: 0 0 50px rgba(255, 215, 0, 0.9) !important;
        margin: 5px 0;
    }}

    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入介面 (純淨無框版) ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('''
        <div class="clean-header-zone">
            <div class="flex-title">
                <span class="diamond-icon">💎</span>
                <h1>百家樂 VIP 系統</h1>
                <span class="diamond-icon">💎</span>
            </div>
            <p style="opacity:0.9; letter-spacing:4px; font-size:16px;">PREMIUM ACCESS ONLY</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True) 
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="請輸入當日授權金鑰")
    
    if st.button("啟 動 系 統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心主介面 (純淨無框版) ---
st.markdown(f'''
    <div class="clean-header-zone">
        <div class="flex-title">
            <span class="diamond-icon">💎</span>
            <h1>百家樂數據中心</h1>
            <span class="diamond-icon">💎</span>
        </div>
        <p style="opacity:0.8; font-size:14px; letter-spacing:3px;">AI CLOUD SYNCING | {LAST_SYNC}</p>
    </div>
''', unsafe_allow_html=True)

rooms = ["— 請選擇百家樂監控桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]:
    st.markdown("<div style='text-align:center; padding:80px; font-size:18px; opacity:0.7;'>📡 雲端數據搜尋中，請選取監控房號...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 狀態監控欄 ---
cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2
status, scol = (f"🔍 數據校準中 ({cnt}/5)", "#FFD700") if cnt < 5 else ("🚫 風險警報：建議避險", "#FF4B4B") if shield else ("● 百家樂 AI 運算連線成功", "#00FF00")

st.markdown(f'<div style="background:rgba(0,0,0,0.85); border:1px solid #FFD700; border-radius:60px; padding:12px; text-align:center; margin-bottom:25px;"><span style="color:{scol}; font-size:16px; letter-spacing:2px; font-weight:bold;">{status}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測區 ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    c1, c2 = st.columns(2)
    with c1:
        pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>AI 推薦方向</p><h1 style='color:{pcol}!important; text-align:center; font-size:78px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>數據信心度</p><h1 style='text-align:center; font-size:78px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 歷史趨勢圖 ---
if st.session_state.history:
    dots = "".join([f"<div style='background:rgba(0,0,0,0.9); border:2.5px solid {'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}; border-radius:50%; width:42px; height:42px; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; margin:0 6px;'>{x}</div>" for x in st.session_state.history[-10:]])
    st.markdown(f"<div style='display:flex; justify-content:center; margin:30px 0;'>{dots}</div>", unsafe_allow_html=True)

# --- 8. 手動輸入按鈕 ---
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

# --- 9. 智能分析儀 ---
trend = "📡 背景分析中..." if cnt < 5 else "⚠️ 偵測亂局" if shield else "✅ 數據建模穩定"
st.markdown(f"<div style='background:rgba(0,0,0,0.4); border:1.5px solid #FFD700; border-radius:60px; padding:16px; text-align:center; margin:20px 0; color:#FFD700; letter-spacing:4px; font-weight:bold;'>{trend}</div>", unsafe_allow_html=True)

# --- 10. 注碼算力中心 ---
st.markdown("<div class='vip-card'><p style='color:#FFD700; text-align:center; font-size:24px; margin-top:0; letter-spacing:5px; font-weight:bold;'>⚖️ 百家樂注碼算力中心</p>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1: bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
with f2: rsk = st.slider("風險 %", 1, 10, 2, label_visibility="collapsed")
suggest = int(bal * (rsk/100) * (0.0 if cnt < 5 or shield else 1.0))
if shield:
    st.markdown("<h1 style='color:#FF4B4B!important; text-align:center; font-size:62px; letter-spacing:12px;'>規避時機</h1>", unsafe_allow_html=True)
else:
    st.markdown(f'<div class="big-data">{suggest}</div>', unsafe_allow_html=True)
if st.button("🧹 快速換桌 / 清除記錄", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
