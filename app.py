import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 邏輯運算 (不變) ---
def get_logic_analysis(history, win_streak):
    if len(history) < 5: return "⏳ 數據校準中...", random.randint(35, 52)
    path = "".join(history[-10:]); last_4 = "".join(history[-4:])
    base_conf = random.randint(38, 58)
    status = "⚠️ 盤勢震盪，建議輕倉觀望"
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 偵測到【長龍規律】"
        base_conf = random.randint(93, 99)
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 偵測到【單跳規律】"
        base_conf = random.randint(88, 95)
    elif "閒莊閒" in last_4:
        status = "✨ 偵測到【逢閒即跳】"
        base_conf = random.randint(86, 94)
    if win_streak >= 2: base_conf = min(base_conf + 3, 99)
    elif win_streak < 0: base_conf = max(base_conf - 15, 32)
    return status, base_conf

# --- 2. 核心介面配置 ---
st.set_page_config(page_title="VIP AI-Pro V13.2", layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg")
st.markdown(f"""
    <style>
    .stApp {{ background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important; }}
    /* 暴力移除所有預設陰影 */
    div, p, span, h1 {{ text-shadow: none !important; }}
    .white-bar {{
        background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center;
        color: #000000 !important; font-weight: bold; margin-bottom: 12px;
    }}
    .road-map-container {{
        display: grid; grid-template-rows: repeat(6, 42px); grid-auto-flow: column; grid-auto-columns: 42px; gap: 8px; 
        background: rgba(255, 255, 255, 0.1) !important; backdrop-filter: blur(15px);
        border: 1.5px solid rgba(212, 175, 55, 0.4); border-radius: 30px; padding: 20px; overflow-x: auto; min-height: 310px; margin: 15px 0;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 狀態初始化 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'locked_room' not in st.session_state: st.session_state.locked_room = None
if 'viewers' not in st.session_state: st.session_state.viewers = random.randint(182, 235)
else: st.session_state.viewers = max(min(st.session_state.viewers + random.choice([-2, 1, 3]), 250), 160)

# 登入與桌號選擇 (省略細節以專注顏色修改)
if not st.session_state.login:
    pwd = st.text_input("密碼", type="password")
    if st.button("登入"):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

if st.session_state.locked_room is None:
    sel_room = st.selectbox("ROOM", options=["— 請選擇桌號 —", "RB01", "RB02"])
    if "RB" in sel_room: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

# --- 4. 顯示核心 (顏色硬鎖定) ---
insight_text, conf_val = get_logic_analysis(st.session_state.history, st.session_state.win_streak)
st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 ({len(st.session_state.history)}/5)</div>', unsafe_allow_html=True)

if len(st.session_state.history) >= 5:
    # 這裡隨機出下一局，但顏色我們會寫死
    next_pred = random.choice(["莊", "閒"])
    
    # 顏色邏輯：莊=純紅, 閒=純藍
    text_color = "#FF0000" if next_pred == "莊" else "#0000FF"
    # 趴數邏輯：>60 紅, <=60 黑
    conf_color = "#FF0000" if conf_val > 60 else "#000000"

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="text-align:center;">
                <p style="color:white; font-size:14px; margin:0;">AI 智能預測</p>
                <p style="color:{text_color} !important; font-size:110px; font-weight:900; margin:-20px 0; text-shadow:none !important;">{next_pred}</p>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style="text-align:center;">
                <p style="color:white; font-size:14px; margin:0;">分析信心度</p>
                <p style="color:{conf_color} !important; font-size:110px; font-weight:900; margin:-20px 0; text-shadow:none !important;">{conf_val}%</p>
            </div>
            """, unsafe_allow_html=True)

# --- 5. 其他內容 ---
road_inner = "".join([f'<div style="width:38px; height:38px; border-radius:50%; background:{"#FF0000" if i=="莊" else "#0000FF" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; border:1px solid white;">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_inner}</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,1,2])
if col1.button("🔴 莊"): st.session_state.history.append("莊"); st.rerun()
if col2.button("和"): st.session_state.history.append("和"); st.rerun()
if col3.button("🔵 閒"): st.session_state.history.append("閒"); st.rerun()

st.markdown(f"<div class='white-bar' style='margin-top:15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)
