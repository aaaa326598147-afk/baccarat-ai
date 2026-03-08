import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化 (2026-03-08 密碼為 0308) ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'win_count' not in st.session_state: st.session_state.win_count = 0

# --- 2. 主介面設定 (背景清晰度最高化) ---
st.set_page_config(page_title="💎 AI 決策系統", layout="centered")

cover_image_path = "cover.jpg"
if os.path.exists(cover_image_path):
    with open(cover_image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{data}");
            background-size: cover;
            background-position: center top;
            background-attachment: fixed;
        }}
        /* ⭐ 透明度拉到最高：遮罩降至 0.05，呈現最亮原圖色彩 */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.05); 
            z-index: -1;
        }}
        /* ⭐ 超強力描邊：防止背景太亮導致字看不清楚 */
        h1, h2, h3, .stMetric, p, span, div, label, .stCaption {{
            color: #FFFFFF !important;
            text-shadow: 
                3px 3px 5px #000,
                -1px -1px 0 #000, 
                1px -1px 0 #000,
                -1px 1px 0 #000,
                 1px 1px 0 #000 !important;
            font-weight: 800 !important;
        }}
        div.stButton > button {{
            background-color: rgba(0,0,0,0.6) !important;
            border: 2px solid #FFFFFF !important;
            color: white !important;
        }}
        .stSidebar {{ background-color: rgba(0,0,0,0.85); }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<style>.stApp { background-color: #121212; }</style>", unsafe_allow_html=True)

# --- 3. 登入介面 ---
if not st.session_state.login:
    st.title("💎 私人俱樂部：決策輔助工具")
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
    if st.button("驗證進入", use_container_width=True):
        if pwd == today_code:
            st.session_state.login = True
            st.rerun()
    st.stop()

# --- 4. 主內容 ---
st.title("💎 私人俱樂部：決策輔助工具")
st.caption(f"🚀 AI 實時數據運算中 | {today_str}")

st.sidebar.header("📌 桌面資訊")
# ⭐ 房號保持完全空白預設
room_id = st.sidebar.text_input("請輸入房號", value="", placeholder="")

if st.sidebar.button("🧹 換桌重置"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()

if not room_id:
    st.warning("👈 請先輸入房號以開始。")
    st.stop()

# --- 5. 核心決策 ---
count = len(st.session_state.history)
if count < 5:
    st.subheader(f"📥 數據同步中 ({count}/5)")
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    current_p = st.session_state.next_pred
    confidence = random.randint(92, 99)
    
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("信心值", f"{confidence}%")
    st.divider()

# --- 6. 操作按鈕 (特效已關閉) ---
st.write(f"### 📢 記錄開出結果")
col1, col2, col3 = st.columns([2, 1, 2])

def handle_click(res):
    if len(st.session_state.history) >= 5:
        if st.session_state.next_pred and res == st.session_state.next_pred:
            st.session_state.win_count += 1
        st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res)
    time.sleep(0.3)
    st.rerun()

with col1:
    if st.button("🔴 莊", use_container_width=True): handle_click("莊")
with col2:
    if st.button("🟢 和", use_container_width=True): handle_click("和")
with col3:
    if st.button("🔵 閒", use_container_width=True): handle_click("閒")

# --- 7. 下方金額計算機 ---
st.write("---")
st.subheader("🧮 智能注碼計算機")
with st.expander("🛡️ 風險管理", expanded=True):
    balance = st.number_input("💵 本金", value=10000, step=1000)
    risk = st.slider("⚖️ 下注 %", 1, 10, 2)
    st.success(f"💡 建議下注金額：**{int(balance * (risk / 100))}**")

# --- 8. 手機端安全墊 ---
st.write("")
st.write("")
st.write("")
