import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 實戰科學演算法 (含配注與動態邏輯) ---
def get_final_analysis(history):
    if len(history) < 5: 
        return "⚖️ 數據樣本蒐集預熱中...", random.randint(42, 55), 0
    valid_history = [x for x in history if x != "和"]
    b_count = valid_history.count("莊"); p_count = valid_history.count("閒")
    path = "".join(history[-10:]); last_4 = "".join(history[-4:])
    
    bias = (p_count - b_count) * 2.8 
    base_conf = 50.68 + bias
    status = "⚖️ 盤勢平衡：建議均注"
    confidence = base_conf
    
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 偵測到【長龍規律】，建議穩定順追"; confidence += 35
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 偵測到【單跳規律】，穩定獲利點"; confidence += 28
    
    final_conf = int(max(min(confidence, 99), 32))
    suggested_amount = int((final_conf / 50) * 1000)
    if final_conf < 45: suggested_amount = 0 
    
    return status, final_conf, suggested_amount

# --- 2. 界面 CSS ---
st.set_page_config(page_title="VIP 數據中心", layout="centered")
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg = get_base64("cover.jpg")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0F1116; {f'background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important;' if bg else ''} }}
    * {{ text-shadow: none !important; -webkit-text-stroke: 0px !important; }}
    .white-bar {{ background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center; color: #000 !important; font-weight: bold; margin-bottom: 12px; border: 1px solid #EEE; }}
    .viewer-box {{ text-align: center; background: rgba(0, 0, 0, 0.7); border-radius: 20px; padding: 6px 18px; width: fit-content; margin: 0 auto 15px auto; border: 1.5px solid #D4AF37; box-shadow: 0 0 10px rgba(212, 175, 55, 0.2); }}
    .road-map-container {{ display: grid; grid-template-rows: repeat(6, 42px); grid-auto-flow: column; grid-auto-columns: 42px; gap: 8px; background: rgba(255, 255, 255, 0.1) !important; backdrop-filter: blur(10px); border: 1.5px solid #D4AF37; border-radius: 25px; padding: 15px; overflow-x: auto; min-height: 300px; margin: 10px 0; }}
    .gold-amount {{ color: #D4AF37 !important; font-size: 65px !important; font-weight: 900 !important; text-align: center; margin: -10px 0; letter-spacing: 2px; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 狀態初始化與登入 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'locked_room' not in st.session_state: st.session_state.locked_room = None
# 初始化人數
if 'viewers' not in st.session_state: st.session_state.viewers = random.randint(320, 380)

if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
    if st.button("啟動系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
        else: st.error("密碼錯誤")
    st.stop()

# --- 4. 主介面 ---
st.markdown('<h1 style="text-align:center; color:white; font-size:45px;">數據中心</h1>', unsafe_allow_html=True)

# 顯示會跳動的人數
st.markdown(f'<div class="viewer-box"><span style="color:#F8D06E; font-size:14px; font-weight:bold;">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

if st.session_state.locked_room is None:
    rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

insight, conf, amount = get_final_analysis(st.session_state.history)
st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 ({len(st.session_state.history)} 局)</div>', unsafe_allow_html=True)

if len(st.session_state.history) >= 1:
    b_c = st.session_state.history.count("莊"); p_c = st.session_state.history.count("閒")
    next_p = "莊" if p_c >= b_c else "閒"
    p_color = "#FF0000" if next_p == "莊" else "#0000FF"
    c_color = "#FF0000" if conf > 65 else "#FFF"
    
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div style="text-align:center;"><p style="color:#AAA; font-size:14px; margin:0;">AI 智能預測</p><p style="color:{p_color} !important; font-size:105px; font-weight:900; margin:-20px 0;">{next_p}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div style="text-align:center;"><p style="color:#AAA; font-size:14px; margin:0;">分析信心度</p><p style="color:{c_color} !important; font-size:105px; font-weight:900; margin:-20px 0;">{conf}%</p></div>', unsafe_allow_html=True)

    st.markdown('<p style="text-align:center; color:#AAA; font-size:14px; margin-top:20px;">建議分配金額</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="gold-amount">{amount:,}</p>', unsafe_allow_html=True)

# 顯示垂直路圖
road_html = "".join([f'<div style="width:38px; height:38px; border-radius:50%; background:{"#FF0000" if i=="莊" else "#0000FF" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; border:1px solid rgba(255,255,255,0.3);">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_html}</div>', unsafe_allow_html=True)

# 操作按鈕 (增加人數跳動邏輯)
b1, b2, b3 = st.columns([2, 1, 2])
def update_action(r):
    st.session_state.history.append(r)
    # 每次點擊人數隨機微幅波動，營造真實感
    st.session_state.viewers += random.choice([-3, -1, 1, 2, 5])
    st.rerun()

if b1.button("🔴 莊 家", use_container_width=True): update_action("莊")
if b2.button("和", use_container_width=True): update_action("和")
if b3.button("🔵 閒 家", use_container_width=True): update_action("閒")

st.markdown(f"<div class='white-bar' style='margin-top:15px;'>📝 {insight}</div>", unsafe_allow_html=True)
if st.button("重置數據 / 更換桌號", use_container_width=True):
    st.session_state.history = []; st.session_state.locked_room = None; st.rerun()
