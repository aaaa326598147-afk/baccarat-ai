import streamlit as st
import random
from datetime import datetime
import os
import base64

# --- 1. AI 權威路評核心邏輯 (含百位取整與避險) ---
def get_ai_road_analysis(history, capital):
    if len(history) < 5: 
        return "⚖️ 數據樣本蒐集預熱中...", 0, 0, False
    
    valid_history = [x for x in history if x != "和"]
    path = "".join(valid_history[-12:]) 
    last_4 = "".join(valid_history[-4:])
    
    status = "⚖️ 盤勢平衡：建議觀察趨勢"
    bonus_conf = 0
    
    # 專業術語偵測
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 龍體成型：趨勢明確，建議順龍切入"; bonus_conf = 35
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 規律單跳：穩定規律，捕捉跳位獲利"; bonus_conf = 28
    elif "莊莊閒閒" in path or "閒閒莊莊" in path:
        status = "🎨 雙跳趨勢：規律分明，建議加倍切入"; bonus_conf = 25
    elif "莊閒閒莊閒閒" in path or "閒莊莊閒莊莊" in path:
        status = "🏠 一房兩廳：結構完整，建議按路投註"; bonus_conf = 30
    elif path.endswith("閒莊") and valid_history.count("閒") > 3:
        status = "✨ 逢閒即跳：慣性跳點形成，勝率極高"; bonus_conf = 22
    elif "莊莊莊閒閒" in path or "閒閒閒莊莊" in path:
        status = "🪜 階梯路成型：階梯攀升，建議縮注跟隨"; bonus_conf = 18
    
    # 信心度計算 (保底 50%)
    b_c = valid_history.count("莊"); p_c = valid_history.count("閒")
    bias = abs(p_c - b_c) * 3.2 
    final_conf = int(max(min(52 + bias + bonus_conf + random.randint(0,2), 99), 50))
    
    # 配注比例與避險門檻
    base_ratio = 0.1
    if final_conf > 85: base_ratio = 0.28
    elif final_conf > 70: base_ratio = 0.15
    elif final_conf < 58: base_ratio = 0  
    
    # 計算原始金額並進行「百位取整」
    raw_amount = capital * base_ratio
    if raw_amount > 0:
        # 四捨五入到百位數
        suggested_amount = int(round(raw_amount / 100) * 100)
        # 防止四捨五入後變 0 (最低保底 100)
        if suggested_amount == 0: suggested_amount = 100
    else:
        suggested_amount = 0

    if suggested_amount == 0:
        status = "🛡️ 盤勢震盪：AI 偵測亂路，建議暫停下注"
    
    return status, final_conf, suggested_amount, True

# --- 2. 界面 CSS 強化 ---
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
    .viewer-box {{ text-align: center; background: rgba(0, 0, 0, 0.7); border-radius: 20px; padding: 6px 18px; width: fit-content; margin: 0 auto 15px auto; border: 1.5px solid #D4AF37; }}
    .road-map-container {{ display: grid; grid-template-rows: repeat(6, 42px); grid-auto-flow: column; grid-auto-columns: 42px; gap: 8px; background: rgba(255, 255, 255, 0.1) !important; backdrop-filter: blur(10px); border: 1.5px solid #D4AF37; border-radius: 25px; padding: 15px; overflow-x: auto; min-height: 300px; margin: 10px 0; }}
    .gold-amount {{ color: #D4AF37 !important; font-size: 75px !important; font-weight: 900 !important; text-align: center; margin: -10px 0; }}
    .balance-box {{ background: rgba(255,255,255,0.1); padding: 10px; border-radius: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.2); }}
    .lock-box {{ height: 180px; display: flex; align-items: center; justify-content: center; border: 2px dashed rgba(255,255,255,0.2); border-radius: 25px; margin: 10px 0; background: rgba(0,0,0,0.3); }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 狀態初始化與流程 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'locked_room' not in st.session_state: st.session_state.locked_room = None
if 'history' not in st.session_state: st.session_state.history = []
if 'viewers' not in st.session_state: st.session_state.viewers = random.randint(320, 380)
if 'current_balance' not in st.session_state: st.session_state.current_balance = 10000.0

if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 系統登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="請輸入 4 位授權碼")
    if st.button("啟動系統", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

if st.session_state.locked_room is None:
    st.markdown("<br><br><h2 style='text-align:center; color:white;'>選擇監控桌號</h2>", unsafe_allow_html=True)
    rooms = ["— 請選擇 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

# --- 4. 主畫面展示 ---
st.markdown('<h1 style="text-align:center; color:white; font-size:45px; margin-top:-20px;">數據中心</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="viewer-box"><span style="color:#F8D06E; font-size:14px; font-weight:bold;">● 雲端連線監控中：{st.session_state.viewers} 名 VIP</span></div>', unsafe_allow_html=True)

# 帳戶本金管理區 (顯示複利效果)
c_col1, c_col2 = st.columns(2)
with c_col1:
    st.markdown('<p style="text-align:center; color:#AAA; font-size:12px; margin-bottom:0;">初始本金設定</p>', unsafe_allow_html=True)
    init_cap = st.number_input("CAP", value=10000, step=1000, label_visibility="collapsed")
with c_col2:
    st.markdown('<p style="text-align:center; color:#AAA; font-size:12px; margin-bottom:0;">當前帳戶餘額</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="balance-box"><span style="color:#FFF; font-size:18px; font-weight:bold;">${st.session_state.current_balance:,.0f}</span></div>', unsafe_allow_html=True)

# 核心分析計算
insight, conf, amount, is_unlocked = get_ai_road_analysis(st.session_state.history, st.session_state.current_balance)
st.markdown(f'<div class="white-bar">● {st.session_state.locked_room} 監控中 (進度: {len(st.session_state.history)}/5)</div>', unsafe_allow_html=True)

if is_unlocked:
    if amount == 0:
        st.markdown(f"""<div class="lock-box"><div style="text-align:center;"><p style="color:#D4AF37; font-size:32px; font-weight:bold; margin:0;">SAFE MODE</p><p style="color:#888; font-size:16px;">AI 偵測亂路，目前建議觀望</p></div></div>""", unsafe_allow_html=True)
    else:
        # 顯示預測大字與百位整數金額
        b_c = st.session_state.history.count("莊"); p_c = st.session_state.history.count("閒")
        next_p = "莊" if p_c >= b_c else "閒"; p_color = "#FF0000" if next_p == "莊" else "#0000FF"
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div style="text-align:center;"><p style="color:#AAA; font-size:14px; margin:0;">AI 預測</p><p style="color:{p_color} !important; font-size:105px; font-weight:900; margin:-20px 0;">{next_p}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div style="text-align:center;"><p style="color:#AAA; font-size:14px; margin:0;">信心度</p><p style="color:#FFF !important; font-size:105px; font-weight:900; margin:-20px 0;">{conf}%</p></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="gold-amount">{amount:,}</p>', unsafe_allow_html=True)
        
        # 獲利/失利結算按鈕
        s1, s2 = st.columns(2)
        if s1.button("✅ 獲利結算", use_container_width=True):
            st.session_state.current_balance += amount; st.rerun()
        if s2.button("❌ 失利結算", use_container_width=True):
            st.session_state.current_balance -= amount; st.rerun()
else:
    st.markdown(f"""<div class="lock-box"><div style="text-align:center;"><p style="color:#888; font-size:24px; margin:0;">⌛ 數據分析鎖定中</p><p style="color:#555; font-size:14px;">請先輸入 {5 - len(st.session_state.history)} 局開牌紀錄</p></div></div>""", unsafe_allow_html=True)

# 珠盤路圖
road_html = "".join([f'<div style="width:38px; height:38px; border-radius:50%; background:{"#FF0000" if i=="莊" else "#0000FF" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; border:1px solid rgba(255,255,255,0.3);">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_html}</div>', unsafe_allow_html=True)

# 動作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_action(r):
    st.session_state.history.append(r)
    st.session_state.viewers += random.choice([-2, 1, 4])
    st.rerun()
if b1.button("🔴 莊 家", use_container_width=True): update_action("莊")
if b2.button("和", use_container_width=True): update_action("和")
if b3.button("🔵 閒 家", use_container_width=True): update_action("閒")

# 即時路評白條
st.markdown(f"<div class='white-bar' style='margin-top:15px;'>{insight}</div>", unsafe_allow_html=True)

if st.button("更換桌號 / 重置系統", use_container_width=True):
    st.session_state.history = []; st.session_state.locked_room = None; st.session_state.current_balance = float(init_cap); st.rerun()
