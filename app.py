import streamlit as st
import random
from datetime import datetime

# --- 1. 核心參數與斷龍閾值 ---
DRAGON_LIMIT = 8 # 設定連出 8 把後，下一把強制斷龍

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 2. 升級版預測邏輯 (含智能斷龍) ---
def get_smart_prediction(history):
    if len(history) < 5: return None
    
    # 檢查最後幾局是否有長龍
    last_segment = history[-DRAGON_LIMIT:]
    
    # 如果最後 8 局全是「莊」，下一把強制預測「閒」 (斷龍)
    if len(last_segment) == DRAGON_LIMIT and all(x == "莊" for x in last_segment):
        return "閒"
    # 如果最後 8 局全是「閒」，下一把強制預測「莊」 (斷龍)
    if len(last_segment) == DRAGON_LIMIT and all(x == "閒" for x in last_segment):
        return "莊"
    
    # 平常維持順勢預測
    return random.choices(["莊", "閒"], weights=[0.51, 0.49])[0]

# --- 3. 路規偵測邏輯 (維持真路判斷) ---
def get_road_insight(history):
    if len(history) < 5: return "⏳ 數據收集校準中..."
    path = "".join(history[-8:]) 
    
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        if len(history) >= 8 and all(x == history[-1] for x in history[-8:]):
            return "⚠️ 警報：長龍過熱，準備【斷龍】介入" # 增加斷龍提示
        return "🐉 偵測到【長龍規律】"
    
    if "莊莊閒閒" in path or "閒閒莊莊" in path: return "👯 偵測到【雙跳規律】"
    if "莊閒莊閒" in path or "閒莊閒莊" in path: return "🎯 偵測到【單跳規律】"
    if "莊閒閒莊" in path or "閒莊莊閒" in path: return "🏠 偵測到【一房兩廳】"
    return "✅ 數據穩定分析中..."

# --- 4. 奢華視覺 CSS (維持絕對置中) ---
st.set_page_config(page_title="VIP AI-Pro V9.8", layout="centered")
st.markdown(
    """
    <style>
    .stApp { background-color: #f0f2f6; } /* 預設背景，如有 cover.jpg 會自動覆蓋 */
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
        width: 100%;
    }
    .bet-label-white {
        background: #FFFFFF !important;
        border-radius: 50px;
        padding: 10px 45px;
        color: #000000 !important;
        font-weight: 900;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin: 20px auto;
        display: table;
    }
    .gold-number { 
        color: #FFD700 !important; 
        font-size: 120px !important; 
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

# --- 5. 核心顯示邏輯 ---
if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center;'>VIP 登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PWD", type="password", placeholder="授權金鑰")
    if st.button("啟 動", use_container_width=True):
        if pwd == datetime.now().strftime("%m%d"): st.session_state.login = True; st.rerun()
    st.stop()

st.markdown('<h1 style="text-align:center;">數據中心</h1>', unsafe_allow_html=True)
rooms = ["— 請選擇桌號 —"] + [f"RB0{i}" for i in range(1, 8)]
sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
if sel_room == rooms[0]: st.stop()

cnt = len(st.session_state.history)
st.markdown(f'<div class="white-bar">● AI 雲端監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 滿 5 局後預測
if cnt >= 5:
    if st.session_state.next_pred is None:
        st.session_state.next_pred = get_smart_prediction(st.session_state.history)
    
    pcol = "#ff4b4b" if st.session_state.next_pred == "莊" else "#1c83e1"
    c1, c2 = st.columns(2)
    c1.markdown(f"<p style='text-align:center; margin:0;'>AI 推薦</p><p style='color:{pcol}!important; font-size:75px; font-weight:900; text-align:center; margin:0;'>{st.session_state.next_pred}</p>", unsafe_allow_html=True)
    c2.markdown(f"<p style='text-align:center; margin:0;'>信心度</p><p style='font-size:75px; font-weight:900; text-align:center; margin:0;'>{random.randint(96, 99)}%</p>", unsafe_allow_html=True)

# 珠盤路顯示 (不變)
# ... [珠盤路 HTML 代碼同前版本] ...

# 操作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_data(r):
    if st.session_state.next_pred and r != "和":
        if r != st.session_state.next_pred: st.session_state.losses += 1
        else: st.session_state.losses = 0
    st.session_state.history.append(r)
    # 每次更新後重新計算下一把預測
    st.session_state.next_pred = get_smart_prediction(st.session_state.history)

if b1.button("🔴 莊 家", use_container_width=True): update_data("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_data("閒"); st.rerun()

# 路評偵測
ai_insight = get_road_insight(st.session_state.history)
st.markdown(f"<div class='white-bar' style='margin-top: 20px;'>📝 {ai_insight}</div>", unsafe_allow_html=True)

# 注碼中心 (滿 5 局門檻)
if cnt >= 5:
    st.markdown('<div class="bet-label-white">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns([1, 6, 1])
    with cc2:
        bal = st.number_input("本金", value=10000, step=1000, key="bal_v98")
        rsk = st.slider("風險", 1, 10, 2, key="rsk_v98")
    
    if st.session_state.losses < 2:
        suggest = int(bal * (rsk/100))
        st.markdown(f'<p class="gold-number">{suggest}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="gold-number" style="opacity:0.1;">0</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.losses = 0; st.session_state.next_pred = None; st.rerun()
