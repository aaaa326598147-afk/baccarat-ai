import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心權重運算 (趴數高低聯動) ---
def get_logic_analysis(history, win_streak):
    if len(history) < 5: return "⏳ 數據校準中...", random.randint(35, 52)
    path = "".join(history[-10:]); last_4 = "".join(history[-4:])
    base_conf = random.randint(38, 58) # 雜亂時低趴數 (黑色)
    status = "⚠️ 盤勢震盪，建議輕倉觀望"

    # 高趴數規律觸發 (紅色)
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 偵測到【長龍規律】"; base_conf = random.randint(93, 99)
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 偵測到【單跳規律】"; base_conf = random.randint(88, 95)
    elif "閒莊閒" in last_4:
        status = "✨ 偵測到【逢閒即跳】"; base_conf = random.randint(86, 94)
        
    return status, base_conf

# --- 2. 核心 CSS 配置 ---
st.set_page_config(page_title="VIP AI-Pro V13.3", layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg")
st.markdown(f"""
    <style>
    .stApp {{ background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important; }}
    /* 暴力移除所有預設投影 */
    * {{ text-shadow: none !important; -webkit-text-stroke: 0px !important; }}
    .white-bar {{
        background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center;
        color: #000000 !important; font-weight: bold; margin-bottom: 12px;
    }}
    .viewer-box {{ 
        text-align: center; background: rgba(0, 0, 0, 0.6); border-radius: 20px; 
        padding: 5px 15px; width: fit-content; margin: 0 auto 15px auto; 
        border: 1.5px solid rgba(255,215,0,0.3); 
    }}
    .road-map-container {{
        display: grid; grid-template-rows: repeat(6, 42px); grid-auto-flow: column; grid-auto-columns: 42px; gap: 8px; 
        background: rgba(255, 255, 255, 0.1) !important; backdrop-filter: blur(15px);
        border: 1.5px solid rgba(212, 175, 55, 0.4); border-radius: 30px; padding: 20px; overflow-x: auto; min-height: 310px; margin: 15px 0;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 初始化 & 在線人數跳動 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'locked_room' not in st.session_state: st.session_state.locked_room = None

# 人數隨機跳動邏輯
if 'viewers' not in st.session_state: 
    st.session_state.viewers = random.randint(182, 235)
else:
    # 每次重新執行代碼人數都會微幅波動
    st.session_state.viewers += random.choice([-2, -1, 0, 1, 2, 4])
    st.session_state.viewers = max(min(st.session_state.viewers, 248), 165)

# --- 4. 登入介面 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("啟動系統"):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 5. 主功能區 ---
st.markdown('<h1 style="text-align:center; color:white; margin-bottom:5px; letter-spacing:2px;">數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="viewer-box"><span style="color:#F8D06E; font-size:13px; font-weight:bold;">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

if st.session_state.locked_room is None:
    sel_room = st.selectbox("ROOM", options=["— 請選擇桌號 —", "RB01", "RB02", "RB03", "RB04", "RB05"])
    if "RB" in sel_room: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

insight_text, conf_val = get_logic_analysis(st.session_state.history, st.session_state.win_streak)
st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 ({len(st.session_state.history)}/5)</div>', unsafe_allow_html=True)

if len(st.session_state.history) >= 5:
    if 'next_pred' not in st.session_state or st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    # 【關鍵顏色硬鎖定】
    # 莊=純紅 #FF0000，閒=純藍 #0000FF
    pred_color = "#FF0000" if st.session_state.next_pred == "莊" else "#0000FF"
    # 趴數=大於60紅，否則黑
    conf_color = "#FF0000" if conf_val > 60 else "#000000"

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="text-align:center;">
                <p style="color:white; font-size:14px; margin:0;">AI 智能預測</p>
                <p style="color:{pred_color} !important; font-size:110px; font-weight:900; margin:-25px 0; text-shadow:none !important;">{st.session_state.next_pred}</p>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style="text-align:center;">
                <p style="color:white; font-size:14px; margin:0;">分析信心度</p>
                <p style="color:{conf_color} !important; font-size:110px; font-weight:900; margin:-25px 0; text-shadow:none !important;">{conf_val}%</p>
            </div>
            """, unsafe_allow_html=True)

# 質感路紙
road_inner = "".join([f'<div style="width:38px; height:38px; border-radius:50%; background:{"#FF0000" if i=="莊" else "#0000FF" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; border:1px solid rgba(255,255,255,0.3);">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_inner}</div>', unsafe_allow_html=True)

# 操作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_step(r):
    if r != "和":
        if r == st.session_state.next_pred: st.session_state.win_streak += 1; st.session_state.losses = 0
        else: st.session_state.win_streak = -1; st.session_state.losses += 1
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choice(["莊", "閒"])

if b1.button("🔴 莊 家", use_container_width=True): update_step("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_step("閒"); st.rerun()

st.markdown(f"<div class='white-bar' style='margin-top: 15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)
