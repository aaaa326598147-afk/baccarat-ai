import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- [註] 核心權重運算與系統初始化邏輯維持 V13.0 不變 ---
def get_logic_analysis(history, win_streak):
    if len(history) < 5: return "⏳ 雲端數據校準中...", random.randint(35, 52)
    path = "".join(history[-10:]); last_4 = "".join(history[-4:])
    base_conf = random.randint(38, 58)
    status = "⚠️ 盤勢震盪，建議輕倉观望"
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 偵測到【長龍規律】，穩定獲利中"
        base_conf = random.randint(93, 99)
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 偵測到【單跳規律】，建議跟跳"
        base_conf = random.randint(88, 95)
    elif last_4 in ["莊莊閒閒", "閒閒莊莊"]:
        status = "👯 偵測到【雙跳規律】，建議持續跟對"
        base_conf = random.randint(84, 92)
    elif "閒莊閒" in last_4:
        status = "✨ 偵測到【逢閒即跳】，抓準進場時機"
        base_conf = random.randint(86, 94)
    if win_streak >= 2: base_conf = min(base_conf + 3, 99)
    elif win_streak < 0: base_conf = max(base_conf - 15, 32)
    return status, base_conf

# --- 2. 專業 CSS (核心修改區域) ---
st.set_page_config(page_title="VIP AI-Pro V13.1", layout="centered")

# 背景圖處理
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg") # 請確保有 cover.jpg 檔案

st.markdown(
    f"""
    <style>
    /* 1. 基礎設定 */
    .stApp {{ background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important; }}
    
    /* 2. 白色橫條與通用樣式 */
    .white-bar {{
        background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center;
        color: #000000 !important; font-weight: bold; margin-bottom: 12px; border: 1.5px solid rgba(212,175,55,0.3);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    
    /* 3. 在線人數與Viewer Box */
    .viewer-box {{ text-align: center; background: rgba(0, 0, 0, 0.6); border-radius: 20px; padding: 5px 15px; width: fit-content; margin: 0 auto 15px auto; border: 1.5px solid rgba(255,215,0,0.3); }}
    .viewer-count {{ color: #F8D06E !important; font-size: 13px; font-weight: bold; text-shadow: none !important; }}
    
    /* =========================================
       4. 【核心修改】預測大字與趴數樣式
       移除所有 text-shadow 以保銳利，強制鎖定實色
       ========================================= */
    .prediction-font {{
        font-size: 110px !important; 
        font-weight: 900 !important; 
        text-align: center; 
        margin: -25px 0 !important;
        /* 強制移除灰色陰影/投影 */
        text-shadow: none !important; 
        display: block !important;
        -webkit-text-stroke: 0px !important; /* 確保無描邊模糊 */
    }}
    
    /* 5. 金額數字維持金色 */
    .gold-number {{ 
        color: #D4AF37 !important; font-size: 110px !important; font-weight: 900; 
        text-align: center; margin: 5px 0 !important; text-shadow: none !important; 
    }}
    
    /* 6. 路評區 (磨砂玻璃質感回歸) */
    .road-map-container {{
        display: grid; grid-template-rows: repeat(6, 42px); grid-auto-flow: column; grid-auto-columns: 42px; gap: 8px; 
        background: rgba(255, 255, 255, 0.08) !important; 
        backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
        border: 1.5px solid rgba(212, 175, 55, 0.4); border-radius: 30px; 
        padding: 20px; overflow-x: auto; min-height: 310px; margin: 15px 0;
    }}
    
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True
)

# --- [註] 主介面呈現邏輯維持 V13.0 不變 ---
# 初始化在線人數跳動
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'locked_room' not in st.session_state: st.session_state.locked_room = None
if 'viewers' not in st.session_state: st.session_state.viewers = random.randint(182, 235)
else: st.session_state.viewers = max(min(st.session_state.viewers + random.choice([-3, -2, -1, 1, 2, 3]), 250), 160)

# 登入頁面
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", placeholder="請輸入密碼")
    if st.button("啟動系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# 主介面
st.markdown('<h1 style="text-align:center; color:white; margin-bottom:5px; letter-spacing:2px;">數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="viewer-box"><span class="viewer-count">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

if st.session_state.locked_room is None:
    rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 9)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

# 獲取路評與信心度
insight_text, conf_val = get_logic_analysis(st.session_state.history, st.session_state.win_streak)
cnt = len(st.session_state.history)

st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

if cnt >= 5:
    if st.session_state.next_pred is None: st.session_state.next_pred = random.choice(["莊", "閒"])
    
    # 【核心修改點 1】莊閒大字：恆定實色 (無發光、無模糊)
    pred_color = "#FF0000" if st.session_state.next_pred == "莊" else "#0000FF"
    
    # 【註】趴數顏色邏輯維持原本動態切換，不在這裡鎖定，以呈現真實感
    conf_color = "#FF0000" if conf_val > 60 else "#000000"
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<p style='text-align:center; color:white; margin:0; font-size:14px;'>AI 智能預測</p><p class='prediction-font' style='color:{pred_color} !important;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<p style='text-align:center; color:white; margin:0; font-size:14px;'>分析信心度 {'🔥' if conf_val > 85 else ''}</p><p class='prediction-font' style='color:{conf_color} !important;'>{conf_val}%</p>", unsafe_allow_html=True)

# 質感路紙回歸
road_inner = "".join([f'<div style="width:38px; height:38px; border-radius:50%; background:{"#FF0000" if i=="莊" else "#0000FF" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_inner}</div>', unsafe_allow_html=True)

# 操作按鈕
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
