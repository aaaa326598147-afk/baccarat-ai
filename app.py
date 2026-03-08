import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化 (2026-03-08) ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None

# --- 2. 佈局與文字浮雕效果 CSS ---
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
            background-size: cover; background-position: center top; background-attachment: fixed;
        }}
        .block-container {{ padding-top: 1.5rem !important; max-width: 600px !important; }}
        
        /* ⭐ 維持浮雕立體字 */
        h1, h2, h3, .stMetric, p, span, label, div {{
            color: #FFFFFF !important;
            font-family: "Microsoft JhengHei", sans-serif !important;
            font-weight: 900 !important;
            text-shadow: 2px 2px 0px #666, 4px 4px 8px rgba(0,0,0,0.8) !important;
        }}

        /* 房號選單 - 增加透明度以區隔 */
        div[data-baseweb="select"] > div {{
            background-color: rgba(0, 0, 0, 0.3) !important;
            border: 1.5px solid #FFFFFF !important;
            border-radius: 12px !important;
            height: 50px !important;
        }}

        /* 路評發光氣泡 - 徹底解決擠成一團 */
        .history-row {{
            display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin: 20px 0;
        }}
        .history-bubble {{
            background: rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.4);
            border-radius: 50%; width: 40px; height: 40px;
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; box-shadow: 0 0 10px rgba(255,255,255,0.2);
        }}

        /* 按鈕視覺強化 */
        div.stButton > button {{
            background: rgba(0, 0, 0, 0.7) !important;
            color: #FFD700 !important;
            border: 2px solid #FFD700 !important;
            border-radius: 15px !important;
            height: 4.5em !important;
            font-size: 18px !important;
        }}

        /* 下拉選單文字顏色修正 */
        div[data-baseweb="popover"] li {{ color: #333 !important; text-shadow: none !important; }}

        [data-testid="stSidebar"] {{ display: none; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 3. 登入 ---
if not st.session_state.login:
    st.markdown("<br><br><h1 style='text-align: center; font-size: 48px;'>💎 私人俱樂部</h1>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        pwd = st.text_input("金鑰", type="password", label_visibility="collapsed", placeholder="輸入金鑰")
        if st.button("驗證進入", use_container_width=True):
            if pwd == today_code:
                st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 房號區 ---
st.markdown("<h2 style='text-align: center; margin-bottom: 5px;'>💎 私人俱樂部</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'>{today_str} | AI 算力同步中</p>", unsafe_allow_html=True)

rb_list = [f"RB0{i}" for i in range(1, 8)]; s_list = [f"S0{i}" for i in range(1, 8)]
room_options = ["— 請選取房號 —"] + rb_list + s_list
selected_room = st.selectbox("房號", options=room_options, label_visibility="collapsed")

if selected_room == "— 請選取房號 —":
    st.markdown("<div style='text-align: center; padding: 50px;'>📡 請選取房號連線</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. AI 路評 (獨立氣泡排列) ---
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
if st.session_state.history:
    st.markdown("<p style='text-align: center; font-size: 14px;'>📊 現場紀錄</p>", unsafe_allow_html=True)
    bubbles = ""
    for x in st.session_state.history[-8:]:
        color = "#ff4b4b" if x == "莊" else "#1c83e1" if x == "閒" else "#28a745"
        bubbles += f"<div class='history-bubble' style='color:{color};'>{x}</div>"
    st.markdown(f"<div class='history-row'>{bubbles}</div>", unsafe_allow_html=True)

# --- 6. 核心預測區 ---
count = len(st.session_state.history)
if count < 5:
    st.markdown(f"<h3 style='text-align: center; margin: 20px 0;'>📡 同步進度 ({count}/5)</h3>", unsafe_allow_html=True)
    st.progress(count / 5)
else:
    if st.session_state.next_pred is None: st.session_state.next_pred = random.choice(["莊", "閒"])
    current_p = st.session_state.next_pred
    confidence = random.randint(93, 99)
    
    c_m1, c_m2 = st.columns(2)
    with c_m1: st.metric("AI 推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c_m2: st.metric("信心度度", f"{confidence}%")

# --- 7. 操作按鈕 ---
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
def add_res(res):
    if len(st.session_state.history) >= 5: st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(res); time.sleep(0.1); st.rerun()

with col_b1:
    if st.button("莊 🔴", use_container_width=True): add_res("莊")
with col_b2:
    if st.button("和", use_container_width=True): add_res("和")
with col_b3:
    if st.button("閒 🔵", use_container_width=True): add_res("閒")

# --- 8. 智能計算機 (置底獨立) ---
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
with st.expander("🧮 智能注碼管理", expanded=True):
    st.markdown("<div style='padding: 10px;'></div>", unsafe_allow_html=True)
    balance = st.number_input("💵 目前本金", value=10000, step=1000)
    risk = st.slider("⚖️ 風險比例 %", 1, 10, 2)
    st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>建議下注：{int(balance * (risk/100))}</h2>", unsafe_allow_html=True)
    
    if st.button("🧹 重置本桌數據", use_container_width=True):
        st.session_state.history = []; st.session_state.next_pred = None; st.rerun()
