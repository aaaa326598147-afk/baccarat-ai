import streamlit as st
from datetime import datetime
import os
import base64

# --- 1. 核心設定 ---
VERSION = "VIP AI-Pro V6.8 修正版"
LAST_SYNC = "2026-03-09 03:30"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. 視覺 CSS (保持你原本喜歡的樣式，僅加入 6 顆換行邏輯) ---
st.set_page_config(page_title=VERSION, layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{ background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover; }}
    .block-container {{ max-width: 500px !important; padding-top: 10px !important; }}
    
    /* 房號選單與標題樣式 */
    .vip-main-title {{ font-size: 42px !important; font-weight: 800; text-align: center; color: white; text-shadow: 0 4px 10px #000; }}

    /* 關鍵修改：珠盤路 6 顆垂直換行網格 */
    .road-grid-wrapper {{
        background: rgba(0, 0, 0, 0.6); border: 1.5px solid #FFD700;
        border-radius: 15px; padding: 10px; margin: 15px 0;
        overflow-x: auto; display: flex;
    }}
    .bead-grid-core {{
        display: grid; 
        grid-template-rows: repeat(6, 40px); /* 固定 6 顆垂直高度 */
        grid-auto-flow: column; /* 滿 6 顆自動往右排 */
        grid-auto-columns: 40px; gap: 5px;
    }}
    .bead-dot {{ width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }}

    /* 還原截圖中的大字預測與按鈕 */
    .ai-hero-val {{ font-size: 60px; font-weight: 900; color: white; text-shadow: 0 0 20px rgba(255,255,255,0.5); text-align: center; }}
    div.stButton > button {{ background: linear-gradient(180deg, #333 0%, #000 100%) !important; color: #FFD700 !important; border: 1px solid #FFD700 !important; border-radius: 12px !important; height: 3.5em !important; font-weight: bold !important; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入區 ---
if not st.session_state.login:
    st.markdown('<h1 class="vip-main-title">💎 VIP 核心系統</h1>', unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", label_visibility="collapsed", placeholder="請輸入授權碼")
    if st.button("登 入", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心 (房號與預測) ---
st.markdown(f'<h1 class="vip-main-title">💎 VIP 數據中心</h1>', unsafe_allow_html=True)

# 房號選擇
rooms = [f"房號 VIP-{i:02d}" for i in range(1, 11)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

# AI 預測區 (還原大字)
st.markdown('<div style="background:rgba(0,0,0,0.7); border-radius:20px; padding:15px; margin:10px 0; border:1px solid #FFD700; text-align:center; color:white;">● 百家樂 AI 運算連線成功</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("<p style='text-align:center; color:silver;'>AI 推薦方向</p>", unsafe_allow_html=True)
    st.markdown("<div class='ai-hero-val'>閒</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<p style='text-align:center; color:silver;'>數據信心度</p>", unsafe_allow_html=True)
    st.markdown("<div class='ai-hero-val'>99%</div>", unsafe_allow_html=True)

# --- 5. 珠盤路 (只改這裡：6 顆垂直換行) ---
st.markdown('<div class="road-grid-wrapper"><div class="bead-grid-core">', unsafe_allow_html=True)
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    st.markdown(f'<div class="bead-dot" style="background:{color};">{item}</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# --- 6. 操作與注碼區 (還原原本配置) ---
b1, b2, b3 = st.columns([2, 1, 2])
def add_rec(r): st.session_state.history.append(r); st.rerun()
if b1.button("🔴 莊 家", use_container_width=True): add_rec("莊")
if b2.button("和", use_container_width=True): add_rec("和")
if b3.button("🔵 閒 家", use_container_width=True): add_rec("閒")

st.markdown("<hr style='border:0.5px solid rgba(255,215,0,0.3);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white;'>⚖️ 百家樂注碼算力中心</p>", unsafe_allow_html=True)
bal = st.number_input("本金", value=10000, step=1000, label_visibility="collapsed")
st.markdown(f'<div style="text-align:center;"><p style="color:silver; font-size:12px;">建議下注金額</p><h1 style="color:#FFD700; font-size:60px;">{(bal//100)*2 if st.session_state.history else 0}</h1></div>', unsafe_allow_html=True)

if st.button("🧹 重置數據 / 快速換房", use_container_width=True):
    st.session_state.history = []
    st.rerun()
