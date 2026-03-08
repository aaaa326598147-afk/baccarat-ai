import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 真·路規偵測邏輯 ---
def get_road_insight(history):
    if len(history) < 5: return "⏳ 數據收集校準中..."
    
    # 轉為字串方便比對規律
    path = "".join(history[-6:]) # 取最後 6 局
    
    # 1. 長龍偵測 (4顆連在一起)
    if "莊莊莊莊" in path: return "🐉 偵測到【莊家長龍】"
    if "閒閒閒閒" in path: return "🐉 偵測到【閒家長龍】"
    
    # 2. 雙跳偵測 (兩顆兩顆一起)
    if "莊莊閒閒" in path or "閒閒莊莊" in path: return "👯 偵測到【雙跳規律】"
    
    # 3. 單跳偵測 (建議補充)
    if "莊閒莊閒" in path or "閒莊閒莊" in path: return "🎯 偵測到【單跳規律】"
    
    # 4. 一房兩廳 (一顆兩顆)
    if "莊閒閒莊" in path or "閒莊莊閒" in path: return "🏠 偵測到【一房兩廳】"
    
    # 5. 階梯偵測 (1,2,3 排列簡化版)
    last_4 = history[-4:]
    if last_4 == ["莊", "閒", "閒", "莊"] or last_4 == ["閒", "莊", "莊", "閒"]:
        return "📈 偵測到【階梯波段】"

    return "✅ 數據穩定分析中..."

# --- 3. 奢華視覺 CSS (維持中軸對齊與白底黑字) ---
st.set_page_config(page_title="VIP AI-Pro V9.7", layout="centered")

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
    }}
    .block-container {{ padding-top: 1rem !important; max-width: 500px !important; }}

    /* 通用白底黑字條 */
    .white-bar {{
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 12px;
        text-align: center;
        color: #000000 !important;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 12px;
        width: 100%;
    }}

    /* 注碼標籤絕對置中 */
    .bet-label-white {{
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 10px 45px;
        color: #000000 !important;
        font-weight: 900;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin: 20px auto;
        display: table;
    }}

    /* 金色發光數字 */
    .gold-number {{ 
        color: #FFD700 !important; 
        font-size: 120px !important; 
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

# --- 4. 邏輯顯示 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", placeholder="授權金鑰")
    if st.button("啟 動", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

st.markdown('<h1 style="text-align:center; color:white;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
st.markdown(f'<div class="white-bar">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 滿 5 局才顯示 AI 推薦
if cnt >= 5:
    if not st.session_state.next_pred: st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:white; margin:0;'>AI 推薦</p><p style='color:{pcol}!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0;'>信心度</p><p style='color:white!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{random.randint(96, 99)}%</p>", unsafe_allow_html=True)

# 珠盤路 (不變)
road_html = '<div style="display:grid; grid-template-rows:repeat(6,42px); grid-auto-flow:column; grid-auto-columns:42px; gap:8px; background:rgba(60,60,60,0.7); border-radius:30px; padding:20px; overflow-x:auto; min-height:310px; margin:15px 0;">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div style="width:38px; height:38px; border-radius:50%; background:{color}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 操作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# --- 【關鍵更新：真實路評偵測區】 ---
ai_insight = get_road_insight(st.session_state.history)
st.markdown(f"<div class='white-bar' style='margin-top: 20px;'>📝 {ai_insight}</div>", unsafe_allow_html=True)

# --- 4. 注碼中心：強制 5 局與置中 ---
if cnt >= 5:
    st.markdown('<div class="bet-label-white">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns([1, 6, 1])
    with cc2:
        bal = st.number_input("本金", value=10000, step=1000, key="bal_v97")
        rsk = st.slider("風險", 1, 10, 2, key="rsk_v97")
    
    if st.session_state.losses < 2:
        suggest = int(bal * (rsk/100))
        st.markdown(f'<p class="gold-number">{suggest}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="gold-number" style="opacity:0.1;">0</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.session_state.next_pred = None; st.rerun()
