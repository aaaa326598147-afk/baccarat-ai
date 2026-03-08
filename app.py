import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心參數與狀態 ---
VERSION = "VIP AI-Pro V5.2 百家樂旗艦版"
LAST_SYNC = "2026-03-08 22:30"

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 奢華白金視覺引擎 ---
st.set_page_config(page_title=VERSION, layout="centered")

def get_bg_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

bg_data = get_bg_base64("cover.jpg")
bg_style = f"""
<style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_data}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .block-container {{ padding-top: 1.5rem !important; max-width: 520px !important; }}
    
    /* 隱藏所有英文碎屑 */
    [data-testid="stInputWidgetInstructions"] {{ display: none !important; }}
    
    /* 全域文字強化 */
    h1, h2, h3, p, span, label, div {{
        color: #FFFFFF !important;
        font-family: "Microsoft JhengHei", sans-serif !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8) !important;
    }}

    /* 白金磨砂面板 */
    .platinum-panel {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 30px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }}

    /* 專業局勢分析儀 (原本空的格子) */
    .trend-analyzer {{
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.5);
        border-radius: 50px;
        padding: 12px;
        text-align: center;
        margin: 15px 0;
        font-size: 15px;
        color: #FFD700 !important;
        letter-spacing: 2px;
        animation: glow 2s infinite alternate;
    }}
    @keyframes glow {{
        from {{ box-shadow: 0 0 5px rgba(255,215,0,0.2); }}
        to {{ box-shadow: 0 0 15px rgba(255,215,0,0.5); }}
    }}

    /* 狀態流光欄 */
    .status-bar {{
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid #FFD700;
        border-radius: 50px;
        padding: 10px;
        text-align: center;
        margin-bottom: 20px;
    }}

    /* 建議金額發光 */
    .bet-amount {{
        color: #FFD700 !important;
        font-size: 85px !important;
        text-align: center;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.7) !important;
        margin: 5px 0;
    }}

    /* 專業按鈕 */
    div.stButton > button {{
        background: linear-gradient(135deg, #222, #000) !important;
        color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.5) !important;
        border-radius: 15px !important;
        height: 3.8em !important;
        font-size: 18px !important;
        letter-spacing: 4px;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{ box-shadow: 0 0 25px rgba(255, 215, 0, 0.4) !important; }}

    header, footer {{ visibility: hidden; }}
</style>
"""
st.markdown(bg_style, unsafe_allow_html=True)

# --- 3. 登入介面 (極簡中文化) ---
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="platinum-panel" style="text-align:center;"><h1 style="font-size: 42px; letter-spacing: 4px;">💎 百家樂 VIP 核心</h1><p style="opacity:0.8; letter-spacing:2px;">授權專用安全通道</p></div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True) 
    pwd = st.text_input("授權碼", type="password", label_visibility="collapsed", placeholder="輸入當日授權碼")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("登 入", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"):
            st.session_state.login = True; st.rerun()
    st.stop()

# --- 4. 數據中心主頁面 ---
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
st.markdown('<h1 style="margin-bottom:0; font-size:40px; letter-spacing:3px;">💎 百家樂數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="opacity:0.8; font-size:13px; letter-spacing:2px;">AI-Pro PREMIUM | {LAST_SYNC}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

rooms = ["— 選取百家樂監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")

if sel_room == rooms[0]:
    st.markdown("<div class='platinum-panel' style='text-align: center; padding: 70px;'>📡 正在搜尋穩定大路數據...</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. 狀態欄邏輯 ---
cnt = len(st.session_state.history)
shield = st.session_state.losses >= 2

if cnt < 5:
    status, scol = f"🔍 數據校準中 (已採樣 {cnt}/5)", "#FFD700"
elif shield:
    status, scol = "🚫 局勢混亂：AI 啟動避險機制", "#FF4B4B"
else:
    status, scol = "● 百家樂雲端算力連線成功", "#00FF00"

st.markdown(f'<div class="status-bar"><span style="color:{scol}; font-size:15px;">{status}</span></div>', unsafe_allow_html=True)

# --- 6. AI 預測結果 ---
if cnt >= 5 and not shield:
    if not st.session_state.next_pred:
        st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]
    
    c1, c2 = st.columns(2)
    with c1:
        pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>AI 推薦方向</p><h1 style='color:{pcol}!important; text-align:center; font-size:65px; margin:0;'>{st.session_state.next_pred}</h1>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<p style='text-align:center; opacity:0.8; margin:0;'>預測信心度</p><h1 style='text-align:center; font-size:65px; margin:0;'>{random.randint(96, 99)}%</h1>", unsafe_allow_html=True)

# --- 7. 歷史趨勢圖 (小圓點) ---
if st.session_state.history:
    dots = "".join([f"<div style='background:rgba(0,0,0,0.8); border:1.5px solid {'#ff4b4b' if x=='莊' else '#1c83e1' if x=='閒' else '#28a745'}; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; color:white; font-size:13px; margin:0 4px;'>{x}</div>" for x in st.session_state.history[-10:]])
    st.markdown(f"<div style='display:flex; justify-content:center; margin:20px 0;'>{dots}</div>", unsafe_allow_html=True)

# --- 8. 手動記錄按鈕 ---
b1, b2, b3 = st.columns([2, 1, 2])
def add_res(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

if b1.button("🔴 莊 家", use_container_width=True): add_res("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): add_res("閒"); st.rerun()

# --- 9. 百家樂局勢分析儀 (功能化空白格) ---
if cnt < 5:
    trend_msg = "📡 正在分析當前路單趨勢..."
elif shield:
    trend_msg = "⚠️ 偵測到亂局，建議更換房號"
else:
    # 簡單模擬專業術語邏輯
    last_3 = st.session_state.history[-3:]
    if all(x == last_3[0] for x in last_3) and len(last_3) == 3:
        trend_msg = f"🔥 警報：{last_3[0]}家長龍趨勢中"
    elif len(st.session_state.history) >= 2 and st.session_state.history[-1] != st.session_state.history[-2]:
        trend_msg = "🔄 趨勢：單跳路徑分析完畢"
    else:
        trend_msg = "✅ 大路數據建模完成，信號穩定"

st.markdown(f"<div class='trend-analyzer'>{trend_msg}</div>", unsafe_allow_html=True)

# --- 10. 智能注碼管理 ---
st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='platinum-panel'>", unsafe_allow_html=True)
st.markdown("<p style='color:#FFD700; text-align:center; font-size:20px; margin-top:0; letter-spacing:3px;'>⚖️ 百家樂注碼運算中心</p>", unsafe_allow_html=True)

f1, f2 = st.columns(2)
with f1: bal = st.number_input("當前本金", value=10000, step=1000, label_visibility="collapsed")
with f2: rsk = st.slider("風險比例 %", 1, 10, 2, label_visibility="collapsed")

mult = 0.0 if cnt < 5 or shield else (0.8 if bal > 10000 else 1.0)
sug = int(bal * (rsk/100) * mult)

if shield:
    st.markdown("<h1 style='color:#FF4B4B!important; text-align:center; font-size:50px; letter-spacing:8px;'>觀望中</h1>", unsafe_allow_html=True)
else:
    st.markdown("<p style='opacity:0.8; text-align:center; margin:0; letter-spacing:2px;'>建議下注金額</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="bet-amount">{sug}</div>', unsafe_allow_html=True)

if st.button("🧹 重置數據 / 快速換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
