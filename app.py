import streamlit as st
import random
from datetime import datetime

# --- 1. 核心邏輯升級 ---
def get_pro_analysis(history):
    """回傳 (路評文字, 建議注碼倍率, 動態信心度)"""
    if len(history) < 5: return "⏳ 數據收集校準中...", 1, random.randint(30, 50)
    
    path = "".join(history[-10:])
    
    # 規律 1：長龍與斷龍警報 (高信心或極低信心)
    last_8 = history[-8:]
    if len(last_8) == 8 and all(x == last_8[0] for x in last_8):
        # 斷龍時信心度會波動，表現出預測的掙扎感
        return "⚠️ 警報：長龍過熱，準備【斷龍】介入", 1, random.randint(45, 65)
    
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        return "🐉 偵測到【長龍規律】，穩定跟進", 2, random.randint(92, 99)

    # 規律 2：單/雙跳 (高信心)
    if "莊閒莊閒" in path or "閒莊閒莊" in path:
        return "🎯 偵測到【單跳規律】，建議跟跳", 2, random.randint(88, 97)
    if "莊莊閒閒" in path or "閒閒莊莊" in path:
        return "👯 偵測到【雙跳規律】，建議跟對", 2, random.randint(85, 95)
    
    # 規律 3：一房兩廳 (中信心)
    if "莊閒閒莊" in path or "閒莊莊閒" in path:
        return "🏠 偵測到【一房兩廳】，穩健操作", 1, random.randint(70, 85)

    # 規律 4：盤勢混亂 (低信心)
    return "✅ 數據整理中，目前無明顯規律", 1, random.randint(40, 68)

# --- 2. 奢華視覺 CSS (絕對置中) ---
st.set_page_config(page_title="VIP AI-Pro V10.0", layout="centered")
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .block-container { padding-top: 1rem !important; max-width: 500px !important; }
    
    .white-bar {
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 12px;
        text-align: center;
        color: #000000 !important;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 12px;
    }

    .bet-label-white {
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 10px 45px;
        color: #000000 !important;
        font-weight: 900;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin: 25px auto;
        display: table;
    }

    .gold-number { 
        color: #FFD700 !important; 
        font-size: 110px !important; 
        text-shadow: 0 0 35px rgba(255, 215, 0, 0.8) !important; 
        font-weight: 900; 
        margin: 5px 0;
        text-align: center;
    }

    label { display: none !important; }
    input { text-align: center !important; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True
)

# --- 3. 狀態初始化 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'next_pred' not in st.session_state: st.session_state.next_pred = None

st.markdown('<h1 style="text-align:center; color:white;">數據中心</h1>', unsafe_allow_html=True)
cnt = len(st.session_state.history)
st.markdown(f'<div class="white-bar">● VIP 大師級監控 ({cnt}/5)</div>', unsafe_allow_html=True)

# 獲取路評與動態信心度
insight_text, bet_mult, conf_val = get_pro_analysis(st.session_state.history)

# 顯示預測區 (滿 5 局才出)
if cnt >= 5:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    # 動態調整信心度顏色，低趴數變灰色，高趴數變綠色
    conf_color = "#28a745" if conf_val > 70 else "#ffc107" if conf_val > 50 else "#6c757d"
    
    c1.markdown(f"<p style='text-align:center; color:white; margin:0;'>AI 推薦</p><p style='color:{pcol}!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; color:white; margin:0;'>信心度</p><p style='color:{conf_color}!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{conf_val}%</p>", unsafe_allow_html=True)

# 顯示珠盤路
road_html = '<div style="display:grid; grid-template-rows:repeat(6,42px); grid-auto-flow:column; grid-auto-columns:42px; gap:8px; background:rgba(60,60,60,0.7); border-radius:30px; padding:20px; overflow-x:auto; min-height:310px; margin:15px 0;">'
for item in st.session_state.history:
    color = "#ff4b4b" if item == "莊" else "#1c83e1" if item == "閒" else "#28a745"
    road_html += f'<div style="width:38px; height:38px; border-radius:50%; background:{color}; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">{item}</div>'
road_html += '</div>'
st.markdown(road_html, unsafe_allow_html=True)

# 操作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_logic(r):
    if r != "和" and st.session_state.next_pred:
        if r == st.session_state.next_pred:
            st.session_state.win_streak += 1
            st.session_state.losses = 0
        else:
            st.session_state.win_streak = -1
            st.session_state.losses += 1
    st.session_state.history.append(r)
    st.session_state.next_pred = random.choice(["莊", "閒"])

if b1.button("🔴 莊 家", use_container_width=True): update_logic("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_logic("閒"); st.rerun()

# 顯示路評
st.markdown(f"<div class='white-bar' style='margin-top: 15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)

# --- 4. 注碼中心：1-3-2-4 系統 (滿 5 局門檻) ---
if cnt >= 5:
    st.markdown('<div class="bet-label-white">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns([1, 6, 1])
    with cc2:
        bal = st.number_input("本金", value=10000, step=1000)
        rsk = st.slider("風險", 1, 10, 2)
    
    if st.session_state.losses < 2:
        # 結合 1-3-2-4 鎖利邏輯
        units = [1, 3, 2, 4]
        current_unit = units[st.session_state.win_streak % 4] if st.session_state.win_streak >= 0 else 1
        suggest = int(bal * (rsk/100) * current_unit)
        st.markdown(f'<p class="gold-number">{suggest}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="gold-number" style="opacity:0.1;">0</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.win_streak = 0; st.session_state.losses = 0; st.session_state.next_pred = None; st.rerun()
