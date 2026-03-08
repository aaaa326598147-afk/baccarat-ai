import streamlit as st
import random

# --- 1. 核心參數 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 絕對精緻：深邃磨砂 CSS ---
st.set_page_config(page_title="VIP AI-Pro", layout="centered")

st.markdown(
    """
    <style>
    /* 全局背景：純粹黑 */
    .stApp { background: #050505 !important; }
    .block-container { max-width: 480px !important; padding-top: 2rem; }

    /* 【頂級磨砂面板】 */
    .vip-glass {
        background: rgba(25, 25, 25, 0.7) !important;
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 35px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        text-align: center;
    }

    /* 文字：極致清晰度 */
    .title-text { color: #FFF; font-weight: 200; letter-spacing: 12px; margin-bottom: 25px; }
    
    /* 注碼數字：黃金漸層 + 立體投影 */
    .gold-number {
        background: linear-gradient(180deg, #FFE082 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 110px !important;
        font-weight: 900;
        margin: 5px 0;
        filter: drop-shadow(0 10px 15px rgba(212,175,55,0.4));
    }

    /* 珠盤路：整齊排列 */
    .road-grid {
        display: grid;
        grid-template-rows: repeat(6, 42px); 
        grid-auto-flow: column;             
        grid-auto-columns: 42px;
        gap: 12px;
        overflow-x: auto;
        justify-content: center;
        padding: 5px;
    }
    .dot {
        width: 40px; height: 40px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; font-weight: bold; color: white;
        box-shadow: inset 0 -3px 6px rgba(0,0,0,0.3);
    }

    /* 推薦區：呼吸感 */
    .predict-box { display: flex; justify-content: space-around; margin-bottom: 20px; }
    .predict-label { color: rgba(255,255,255,0.4); font-size: 13px; margin-bottom: 5px; }
    .predict-value { color: #FFF; font-size: 75px; font-weight: 900; line-height: 1; }

    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 介面內容 ---
st.markdown('<h2 class="title-text" style="text-align:center;">數據中心</h2>', unsafe_allow_html=True)
sel_room = st.selectbox("ROOM", options=["— 選擇桌號 —", "RB01", "RB02"], label_visibility="collapsed")

if sel_room == "— 選擇桌號 —": st.stop()

# 模擬連線成功
st.markdown('<div style="color:#00FF00; font-size:13px; text-align:center; margin-bottom:15px; opacity:0.8;">● AI 核心計算連線中...</div>', unsafe_allow_html=True)

# 推薦方向
if len(st.session_state.history) >= 5:
    st.markdown('<div class="predict-box">'
                '<div><div class="predict-label">推薦方向</div><div class="predict-value" style="color:#FF4B4B;">莊</div></div>'
                '<div><div class="predict-label">信心度</div><div class="predict-value">97%</div></div>'
                '</div>', unsafe_allow_html=True)

# 珠盤路面板
st.markdown('<div class="vip-glass">', unsafe_allow_html=True)
road_html = '<div class="road-grid">'
for item in st.session_state.history:
    color = "#FF4B4B" if item == "莊" else "#1C83E1" if item == "閒" else "#2ECC71"
    road_html += f'<div class="dot" style="background:{color};">{item}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# 輸入按鈕
c1, c2, c3 = st.columns([2,1,2])
if c1.button("🔴 莊 家", use_container_width=True): st.session_state.history.append("莊"); st.rerun()
if c2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if c3.button("🔵 閒 家", use_container_width=True): st.session_state.history.append("閒"); st.rerun()

# 路評膠囊
st.markdown(f'<div style="background:rgba(255,215,0,0.1); border:1px solid rgba(255,215,0,0.3); border-radius:50px; padding:10px; color:#FFD700; text-align:center; margin:20px 0; font-size:15px;">⚖️ 目前偵測到長龍規律，建議輕倉跟隨</div>', unsafe_allow_html=True)

# 注碼中心
st.markdown('<div class="vip-glass">', unsafe_allow_html=True)
st.markdown('<div style="color:rgba(255,255,255,0.4); font-size:13px; letter-spacing:4px;">BET CENTER</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a: st.number_input("CAPITAL", value=10000, label_visibility="collapsed")
with col_b: st.slider("RISK", 1, 10, 2, label_visibility="collapsed")

st.markdown('<p class="gold-number">200</p>', unsafe_allow_html=True)

if st.button("RESET DATA", use_container_width=True): st.session_state.history = []; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
