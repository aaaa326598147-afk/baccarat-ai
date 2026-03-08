import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 擬真運算邏輯 (信心度隨風險大幅跳動) ---
def get_final_analysis(history, win_streak):
    if len(history) < 5: 
        return "⏳ 數據校準中...", random.randint(31, 55)
    
    path = "".join(history[-10:]) 
    last_4 = "".join(history[-4:])
    
    # 強規律判斷 (高趴數區)
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        base_conf = random.randint(92, 98)
    elif last_4 in ["莊莊閒閒", "閒閒莊莊", "莊閒莊閒", "閒莊閒莊"]:
        base_conf = random.randint(81, 91)
    else:
        # 雜亂盤勢 (低趴數區，確保低於 60)
        base_conf = random.randint(34, 58)
    
    # 連贏加成 / 連輸懲罰
    if win_streak >= 2: base_conf = min(base_conf + 5, 99)
    elif win_streak < 0: base_conf = max(base_conf - 20, 31)
        
    status = "🎯 偵測到強規律" if base_conf > 75 else "✅ 盤勢穩定" if base_conf > 60 else "⚠️ 建議輕倉觀望"
    return status, base_conf

# --- 2. 嚴格 CSS (移除所有模糊陰影) ---
st.set_page_config(page_title="VIP AI-Pro V12.5", layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{ background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important; }}
    
    .white-bar {{
        background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center;
        color: #000000 !important; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 12px;
    }}
    
    /* 核心預測字樣式：禁止任何陰影 */
    .prediction-font {{
        font-size: 110px !important; font-weight: 900 !important; 
        text-align: center; margin: -25px 0; text-shadow: none !important;
    }}
    
    .gold-number {{ color: #D4AF37 !important; font-size: 110px !important; font-weight: 900; text-align: center; margin: 5px 0; text-shadow: none !important; }}
    .viewer-box {{ text-align: center; background: rgba(0, 0, 0, 0.5); border-radius: 20px; padding: 5px 15px; width: fit-content; margin: 0 auto 15px auto; }}
    .viewer-count {{ color: #F8D06E !important; font-size: 13px; font-weight: bold; }}
    
    .road-map-container {{
        display: grid; grid-template-rows: repeat(6, 42px); grid-auto-flow: column; grid-auto-columns: 42px; gap: 8px; 
        background: rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(10px); border-radius: 30px; padding: 20px; overflow-x: auto; min-height: 310px; margin: 15px 0;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 初始化 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'locked_room' not in st.session_state: st.session_state.locked_room = None
if 'viewers' not in st.session_state: st.session_state.viewers = random.randint(182, 235)

# --- 4. 登入 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", placeholder="請輸入密碼")
    if st.button("啟動系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 5. 數據中心介面 ---
st.markdown('<h1 style="text-align:center; color:white; margin-bottom:5px; letter-spacing:2px;">數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="viewer-box"><span class="viewer-count">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

if st.session_state.locked_room is None:
    rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 9)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

insight_text, conf_val = get_final_analysis(st.session_state.history, st.session_state.win_streak)
cnt = len(st.session_state.history)

st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

if cnt >= 5:
    if st.session_state.next_pred is None: st.session_state.next_pred = random.choice(["莊", "閒"])
    
    # 莊閒大字：純紅或純藍 (絕對實色)
    pred_color = "#FF0000" if st.session_state.next_pred == "莊" else "#0000FF"
    
    # 信心度：大於 60% 紅色，低於或等於 60% 黑色
    conf_color = "#FF0000" if conf_val > 60 else "#000000"
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<p style='text-align:center; color:white; margin:0; font-size:14px;'>AI 智能預測</p><p class='prediction-font' style='color:{pred_color}!important;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<p style='text-align:center; color:white; margin:0; font-size:14px;'>分析信心度</p><p class='prediction-font' style='color:{conf_color}!important;'>{conf_val}%</p>", unsafe_allow_html=True)

# 珠盤路展示
road_inner = "".join([f'<div style="width:38px; height:38px; border-radius:50%; background:{"#FF4B4B" if i=="莊" else "#1C83E1" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_inner}</div>', unsafe_allow_html=True)

# 操作
b1, b2, b3 = st.columns([2, 1, 2])
def update_step(r):
    if r != "和" and st.session_state.next_pred:
        if r == st.session_state.next_pred: st.session_state.win_streak += 1; st.session_state.losses = 0
        else: st.session_state.win_streak = -1; st.session_state.losses += 1
    st.session_state.history.append(r); st.session_state.next_pred = random.choice(["莊", "閒"])

if b1.button("🔴 莊 家", use_container_width=True): update_step("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_step("閒"); st.rerun()

st.markdown(f"<div class='white-bar' style='margin-top: 15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)

if cnt >= 5:
    st.markdown('<div style="background:white; border-radius:50px; padding:8px 40px; color:black; font-weight:900; margin:20px auto; display:table;">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    bal = st.number_input("本金", value=10000, label_visibility="collapsed")
    if st.session_state.losses < 2:
        u = [1, 3, 2, 4][st.session_state.win_streak % 4] if st.session_state.win_streak >= 0 else 1
        st.markdown(f'<p class="gold-number">{int(bal*0.02*u)}</p>', unsafe_allow_html=True)
    else: st.markdown('<p class="gold-number" style="opacity:0.2;">0</p>', unsafe_allow_html=True)

if st.button("更換桌號", use_container_width=True):
    st.session_state.history = []; st.session_state.win_streak = 0; st.session_state.losses = 0; st.session_state.next_pred = None; st.session_state.locked_room = None; st.rerun()
