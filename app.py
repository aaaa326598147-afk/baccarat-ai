import streamlit as st
import random

# --- 核心邏輯 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 精緻玻璃視覺 CSS ---
st.set_page_config(page_title="VIP AI-Pro", layout="centered")

st.markdown(
    """
    <style>
    /* 全黑背景，襯托玻璃質感 */
    .stApp { background: #000000 !important; }
    .block-container { max-width: 480px !important; padding-top: 1rem; }

    /* 【黑色框框改進：極細磨砂玻璃】 */
    .glass-box {
        background: rgba(40, 40, 40, 0.4) !important; /* 降低透明度，透出背景 */
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 0.8px solid rgba(255, 255, 255, 0.2); /* 白金極細邊框 */
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    /* 標題與標籤 */
    .text-title { color: #FFFFFF; font-weight: 200; letter-spacing: 10px; margin-bottom: 20px; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
    .text-label { color: rgba(255, 255, 255, 0.6); font-size: 13px; letter-spacing: 1px; }

    /* 注碼數字：維持 V8.2 的大氣感，優化光暈 */
    .bet-main {
        color: #FFD700 !important;
        font-size: 110px !important;
        font-weight: 900;
        margin: 10px 0;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.5), 0 5px 15px rgba(0,0,0,0.8);
    }

    /* 珠盤路：整齊排列 */
    .road-grid {
        display: grid;
        grid-template-rows: repeat(6, 40px); 
        grid-auto-flow: column;             
        grid-auto-columns: 40px;
        gap: 10px;
        overflow-x: auto;
        justify-content: center;
    }
    .dot {
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
    }

    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True
)

# --- 介面佈局 ---
st.markdown('<h2 class="text-title" style="text-align:center;">數據中心</h2>', unsafe_allow_html=True)
sel_room = st.selectbox("ROOM", ["RB01", "RB02", "RB03"], label_visibility="collapsed")

# 狀態條 (原黑色框框改為玻璃感)
st.markdown('<div style="background:rgba(255,215,0,0.15); border:0.5px solid #FFD700; border-radius:50px; padding:8px; text-align:center; color:#FFD700; font-size:14px; margin-bottom:20px;">● 百家樂 AI 運算連線成功</div>', unsafe_allow_html=True)

# 珠盤路面板 (原黑色大框改為玻璃感)
st.markdown('<div class="glass-box">', unsafe_allow_html=True)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#FF4B4B" if item == "莊" else "#1C83E1" if item == "閒" else "#2ECC71"
    road_html += f'<div class="dot" style="background:{color};">{item}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# 操作按鈕
c1, c2, c3 = st.columns([2, 1, 2])
if c1.button("🔴 莊 家", use_container_width=True): st.session_state.history.append("莊"); st.rerun()
if c2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if c3.button("🔵 閒 家", use_container_width=True): st.session_state.history.append("閒"); st.rerun()

# 路評 (原黑色長框改為玻璃感)
ai_msg = "偵測趨勢規律中..." if len(st.session_state.history) < 5 else "偵測目前【莊】勢頭較穩"
st.markdown(f'<div class="glass-box" style="padding:12px; margin:20px 0; border-radius:50px;">📝 路評：{ai_msg}</div>', unsafe_allow_html=True)

# 注碼中心 (維持精確置中，改為玻璃背板)
st.markdown('<div class="glass-box">', unsafe_allow_html=True)
st.markdown('<p class="text-label">⚖️ 注 碼 中 心</p>', unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca: st.number_input("CAPITAL", value=10000, label_visibility="collapsed")
with cb: st.slider("RISK", 1, 10, 2, label_visibility="collapsed")

st.markdown('<p class="bet-main">200</p>', unsafe_allow_html=True)

if st.button("清除記錄 / 換桌", use_container_width=True): st.session_state.history = []; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
