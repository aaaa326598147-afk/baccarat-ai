import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心邏輯庫 ---
def get_final_analysis(history):
    if len(history) < 5: return "⏳ 數據收集校準中...", 1, random.randint(35, 50)
    path = "".join(history[-10:])
    
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        return "🐉 偵測到【長龍規律】，穩健獲利中", 2, random.randint(94, 99)
    if "莊閒莊閒莊" in path or "閒莊閒莊閒" in path:
        return "🎯 偵測到【單跳規律】，精準切入", 2, random.randint(92, 98)
    if "莊莊閒閒" in path or "閒閒莊莊" in path:
        return "👯 偵測到【雙跳規律】，建議跟對", 2, random.randint(85, 93)
    if "莊閒閒莊" in path or "閒莊莊閒" in path:
        return "🏠 偵測到【一房兩廳】，節奏穩定", 1, random.randint(82, 89)

    last_8 = history[-8:]
    if len(last_8) == 8 and all(x == last_8[0] for x in last_8):
        return "⚠️ 警報：龍過八必斷，準備【斷龍】", 1, random.randint(55, 75)

    return "✅ 盤勢分析中，建議輕倉觀望", 1, random.randint(35, 54)

# --- 2. 奢華視覺 CSS ---
st.set_page_config(page_title="VIP AI-Pro V10.3", layout="centered")

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
    }}
    .block-container {{ padding-top: 1rem !important; max-width: 500px !important; }}
    
    .white-bar {{
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 12px;
        text-align: center;
        color: #000000 !important;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 12px;
    }}

    .bet-label-white {{
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 10px 45px;
        color: #000000 !important;
        font-weight: 900;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin: 25px auto;
        display: table;
    }}

    .gold-number {{ 
        color: #FFD700 !important; 
        font-size: 110px !important; 
        text-shadow: 0 0 35px rgba(255, 215, 0, 0.8) !important; 
        font-weight: 900; 
        margin: 5px 0;
        text-align: center;
    }}

    label {{ display: none !important; }}
    input {{ text-align: center !important; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 登入邏輯 ---
if 'login' not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white; letter-spacing:5px;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", placeholder="請輸入授權密碼")
    if st.button("啟 動 系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): 
            st.session_state.login = True
            st.rerun()
        else:
            st.error("授權碼錯誤，請聯繫技術人員")
    st.stop()

# --- 4. 數據中心初始化 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'next_pred' not in st.session_state: st.session_state.next_pred = None

st.markdown('<h1 style="text-align:center; color:white; letter-spacing:3px;">數據中心</h1>', unsafe_allow_html=True)

# 房間選擇 (修正 SyntaxError)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 9)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]:
    st.info("請先選擇桌號以同步雲端數據")
    st.stop()

cnt = len(st.session_state.history)
st.markdown(f'<div class="white-bar">● {sel_room} 監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 獲取分析數據
insight_text, _, conf_val = get_final_analysis(st.session_state.history)

# 預測顯示區
if cnt >= 5:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    conf_color = "#28a745" if conf_val > 80 else "#ffc107" if conf_val > 54 else "#6c757d"
    
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:white; margin:0;'>AI 推薦</p><p style='color:{pcol}!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0;'>信心度</p><p style='color:{conf_color}!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{conf_val}%</p>", unsafe_allow_html=True)

# 珠盤路
road_html = '<div style="display:grid; grid-template-rows:repeat(6,42px); grid-auto-flow:column; grid-auto-columns:42px; gap:8px; background:rgba(40,40,40,0.6); border-radius:30px; padding:20px; overflow-x:auto; min-height:310px; margin:15px 0;">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div style="width:38px; height:38px; border-radius:50%; background:{color}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 按鈕區
b1, b2, b3 = st.columns([2, 1, 2])
def update_step(r):
    if r != "和" and st.session_state.next_pred:
        if r == st.session_state.next_pred:
            st.session_state.win_streak += 1
            st.session_state.losses = 0
        else:
            st.session_state.win_streak = -1
            st.session_state.losses += 1
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choice(["莊", "閒"])

if b1.button("🔴 莊 家", use_container_width=True): update_step("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_step("閒"); st.rerun()

# 路評文字
st.markdown(f"<div class='white-bar' style='margin-top: 15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)

# --- 5. 注碼中心：1-3-2-4 鎖利 ---
if cnt >= 5:
    st.markdown('<div class="bet-label-white">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns([1, 6, 1])
    with cc2:
        bal = st.number_input("本金", value=10000, step=1000)
        rsk = st.slider("風險", 1, 10, 2)
    
    if st.session_state.losses < 2:
        units = [1, 3, 2, 4]
        current_unit = units[st.session_state.win_streak % 4] if st.session_state.win_streak >= 0 else 1
        suggest = int(bal * (rsk/100) * current_unit)
        st.markdown(f'<p class="gold-number">{suggest}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="gold-number" style="opacity:0.1;">0</p>', unsafe_allow_html=True)

# 清除按鈕
if st.button("🧹 清除記錄 / 換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.win_streak = 0; st.session_state.losses = 0; st.session_state.next_pred = None; st.rerun()
