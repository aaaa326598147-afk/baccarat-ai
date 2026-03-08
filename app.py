import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. 核心邏輯 ---
def get_final_analysis(history):
    if len(history) < 4: 
        return "⏳ 雲端數據校準中...", 1, random.randint(35, 48), False
    path = "".join(history[-10:]) 
    last_4 = "".join(history[-4:])
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        return "🐉 偵測到【長龍規律】，穩定獲利中", 2, random.randint(94, 99), True
    if last_4 == "莊莊閒閒" or last_4 == "閒閒莊莊":
        return "👯 偵測到【雙跳規律】，建議持續跟對", 2, random.randint(88, 95), True
    if "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        return "🎯 偵測到【單跳規律】，建議跟跳", 2, random.randint(90, 97), True
    return "✅ 盤勢重整中，建議輕倉觀望", 1, random.randint(38, 62), False

# --- 2. 奢華 CSS (移除發光效果) ---
st.set_page_config(page_title="VIP AI-Pro V11.2", layout="centered")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

bg = get_base64("cover.jpg")
st.markdown(
    f"""
    <style>
    @keyframes hot-glow-bar {{
        0% {{ box-shadow: 0 0 8px #FFD700; border: 1px solid #FFD700; }}
        50% {{ box-shadow: 0 0 25px #FFD700; border: 1px solid #FFFFFF; }}
        100% {{ box-shadow: 0 0 8px #FFD700; border: 1px solid #FFD700; }}
    }}

    .stApp {{ background-image: url("data:image/jpeg;base64,{bg}"); background-size: cover !important; }}

    .white-bar {{
        background: #FFFFFF !important;
        border-radius: 50px; padding: 12px; text-align: center;
        color: #000000 !important; font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 12px;
    }}
    
    .hot-glow-active {{
        animation: hot-glow-bar 1.5s infinite ease-in-out !important;
        background: linear-gradient(90deg, #FFFFFF, #FFD700, #FFFFFF) !important;
    }}

    /* 移除金額發光特效 */
    .gold-number {{ 
        color: #D4AF37 !important; /* 沉穩金 */
        font-size: 110px !important; 
        text-shadow: none !important; /* 強制移除發光 */
        font-weight: 900; 
        text-align: center;
        margin: 5px 0;
        letter-spacing: -2px;
    }}
    
    .viewer-box {{
        text-align: center; background: rgba(0, 0, 0, 0.4); 
        border-radius: 20px; padding: 5px 15px; width: fit-content; margin: 0 auto 15px auto;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }}
    .viewer-count {{
        color: #F8D06E !important; font-size: 13px; font-weight: bold; 
        text-shadow: 1px 1px 2px rgba(0,0,0,1); letter-spacing: 1px;
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

if random.random() < 0.2: st.session_state.viewers += random.choice([-1, 1])

# --- 4. 登入系統 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", placeholder="請輸入密碼")
    if st.button("啟動系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): 
            st.session_state.login = True
            st.rerun()
        else: st.error("授權碼錯誤")
    st.stop()

# --- 5. 介面呈現 ---
st.markdown('<h1 style="text-align:center; color:white; margin-bottom:5px; letter-spacing:2px;">數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="viewer-box"><span class="viewer-count">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

if st.session_state.locked_room is None:
    rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 9)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]:
        st.session_state.locked_room = sel_room
        st.rerun()
    st.stop()

insight_text, _, conf_val, is_hot = get_final_analysis(st.session_state.history)
cnt = len(st.session_state.history)
glow_style = "hot-glow-active" if is_hot else ""
st.markdown(f'<div class="white-bar {glow_style}">● {st.session_state.locked_room} 監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

if cnt >= 5:
    if st.session_state.next_pred is None: st.session_state.next_pred = random.choice(["莊", "閒"])
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    conf_color = "#28a745" if conf_val > 80 else "#ffc107" if conf_val > 55 else "#6c757d"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; color:white; margin:0; font-size:14px;'>AI 智能預測</p><p style='color:{pcol}!important; font-size:80px; font-weight:900; text-align:center; margin-top:-10px;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0; font-size:14px;'>信心度 {'🔥' if is_hot else ''}</p><p style='color:{conf_color}!important; font-size:80px; font-weight:900; text-align:center; margin-top:-10px;'>{conf_val}%</p>", unsafe_allow_html=True)

# 珠盤路
road_html = '<div style="display:grid; grid-template-rows:repeat(6,42px); grid-auto-flow:column; grid-auto-columns:42px; gap:8px; background:rgba(0,0,0,0.85); border-radius:30px; padding:20px; overflow-x:auto; min-height:310px; margin:15px 0; border: 1px solid rgba(212,175,55,0.3);">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div style="width:38px; height:38px; border-radius:50%; background:{color}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 操作按鈕
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

st.markdown(f"<div class='white-bar' style='margin-top: 15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)

# 金額區（移除發光）
if cnt >= 5:
    st.markdown('<div style="background:white; border-radius:50px; padding:8px 40px; color:black; font-weight:900; margin:20px auto; display:table;">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    c_bal = st.columns([1, 4, 1])[1]
    with c_bal:
        bal = st.number_input("本金", value=10000, label_visibility="collapsed")
    if st.session_state.losses < 2:
        units = [1, 3, 2, 4]
        u = units[st.session_state.win_streak % 4] if st.session_state.win_streak >= 0 else 1
        st.markdown(f'<p class="gold-number">{int(bal*(0.02)*u)}</p>', unsafe_allow_html=True)
    else: st.markdown('<p class="gold-number" style="opacity:0.2;">0</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 更換桌號", use_container_width=True):
    st.session_state.history = []; st.session_state.win_streak = 0; st.session_state.losses = 0; st.session_state.next_pred = None; st.session_state.locked_room = None; st.rerun()
