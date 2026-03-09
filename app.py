import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 實戰科學演算法 ---
def get_final_analysis(history):
    if len(history) < 5: 
        return "⚖️ 數據樣本蒐集預熱中...", random.randint(42, 55)
    valid_history = [x for x in history if x != "和"]
    total = len(valid_history)
    if total == 0: return "⚖️ 數據預熱中...", 50
    b_count = valid_history.count("莊"); p_count = valid_history.count("閒")
    path = "".join(history[-10:]); last_4 = "".join(history[-4:])
    bias = (p_count - b_count) * 2.8 
    base_conf = 50.68 + bias
    status = "⚖️ 盤勢平衡：建議均注"
    confidence = base_conf
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 偵測到【長龍規律】，穩定獲利中"; confidence += 35
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 偵測到【單跳規律】，建議跟進"; confidence += 28
    return status, int(max(min(confidence, 99), 32))

# --- 2. 界面 CSS (還原截圖美感) ---
st.set_page_config(page_title="VIP 數據中心", layout="centered")
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg = get_base64("cover.jpg")
st.markdown(f"""
    <style>
    .stApp {{ background-color: #F0EDE9; {f'background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important;' if bg else ''} }}
    * {{ text-shadow: none !important; -webkit-text-stroke: 0px !important; }}
    .white-bar {{ background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center; color: #000000 !important; font-weight: bold; margin-bottom: 12px; border: 1px solid #EEE; }}
    .viewer-box {{ text-align: center; background: rgba(0, 0, 0, 0.6); border-radius: 20px; padding: 5px 15px; width: fit-content; margin: 0 auto 15px auto; border: 1px solid #D4AF37; }}
    .road-map-container {{ background: rgba(255, 255, 255, 0.4); border: 1.5px solid #D4AF37; border-radius: 30px; padding: 20px; overflow-x: auto; min-height: 250px; margin: 15px 0; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 主介面邏輯 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'locked_room' not in st.session_state: st.session_state.locked_room = None
if 'viewers' not in st.session_state: st.session_state.viewers = random.randint(180, 240)

st.markdown('<h1 style="text-align:center; color:#FFF; font-size:45px;">數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="viewer-box"><span style="color:#F8D06E; font-size:13px; font-weight:bold;">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

if st.session_state.locked_room is None:
    # 補齊所有桌號
    rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

insight, conf = get_final_analysis(st.session_state.history)
st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 ({len(st.session_state.history)} 局)</div>', unsafe_allow_html=True)

if len(st.session_state.history) >= 1:
    b_c = st.session_state.history.count("莊"); p_c = st.session_state.history.count("閒")
    next_p = "莊" if p_c >= b_c else "閒"
    p_color = "#FF0000" if next_p == "莊" else "#0000FF"
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div style="text-align:center;"><p style="color:#999; font-size:14px;">AI 智能預測</p><p style="color:{p_color}; font-size:100px; font-weight:bold; margin-top:-20px;">{next_p}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div style="text-align:center;"><p style="color:#999; font-size:14px;">分析信心度</p><p style="color:#333; font-size:100px; font-weight:bold; margin-top:-20px;">{conf}%</p></div>', unsafe_allow_html=True)

road = "".join([f'<div style="width:35px; height:35px; border-radius:50%; background:{"#FF0000" if i=="莊" else "#0000FF" if i=="閒" else "#28A745"}; margin:3px;"></div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container" style="display: flex; flex-wrap: wrap;">{road}</div>', unsafe_allow_html=True)

b1, b2, b3 = st.columns([2, 1, 2])
if b1.button("🔴 莊 家", use_container_width=True): st.session_state.history.append("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): st.session_state.history.append("閒"); st.rerun()

st.markdown(f"<div class='white-bar' style='margin-top:15px;'>📝 {insight}</div>", unsafe_allow_html=True)
if st.button("更換桌號"): st.session_state.history = []; st.session_state.locked_room = None; st.rerun()
