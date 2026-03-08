import streamlit as st
import random
from datetime import datetime

# --- 1. 核心大師邏輯庫 ---
def analyze_road_pro(history):
    """大師級路規掃描器"""
    if len(history) < 5: return "⏳ 數據收集校準中...", 1
    
    path = "".join(history[-10:])
    
    # 規律 1：長龍與斷龍 (龍過八必斷)
    last_8 = history[-8:]
    if len(last_8) == 8 and all(x == last_8[0] for x in last_8):
        return "⚠️ 警報：長龍過熱，準備【斷龍】介入", 1
    
    # 規律 2：單跳 (BPBPBP)
    if "莊閒莊閒" in path or "閒莊閒莊" in path:
        return "🎯 偵測到【單跳規律】，建議跟跳", 2
    
    # 規律 3：雙跳 (BBPPBB)
    if "莊莊閒閒" in path or "閒閒莊莊" in path:
        return "👯 偵測到【雙跳規律】，建議跟對", 2
    
    # 規律 4：一房兩廳 (BPPBPP)
    if "莊閒閒莊" in path or "閒莊莊閒" in path:
        return "🏠 偵測到【一房兩廳】，穩健操作", 1
        
    return "✅ 盤勢分析穩定，請按計畫操作", 1

def get_bet_unit_1324(win_streak):
    """1-3-2-4 鎖利投注邏輯"""
    # 1-3-2-4 系統：第一把勝後進階 3，再勝回撤 2，四連勝衝 4
    units = [1, 3, 2, 4]
    if win_streak < 0: return 1 # 輸了回歸 1 單位
    return units[win_streak % 4]

# --- 2. 奢華視覺 CSS (維持中軸對齊與白底黑字) ---
st.set_page_config(page_title="VIP AI-Pro V9.9", layout="centered")
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; } /* 配合黑色底背景 */
    .block-container { padding-top: 1rem !important; max-width: 500px !important; }
    
    /* 白底黑字通用狀態條 */
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

    /* 建議分配金額標籤 - 絕對居中 */
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

    /* 金色發光大數字 */
    .gold-number { 
        color: #FFD700 !important; 
        font-size: 115px !important; 
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

# --- 3. 核心運行邏輯 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'win_streak' not in st.session_state: st.session_state.win_streak = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# 登入與基礎顯示 (略過重複代碼)
st.markdown('<h1 style="text-align:center; color:white;">數據中心</h1>', unsafe_allow_html=True)
cnt = len(st.session_state.history)
st.markdown(f'<div class="white-bar">● AI 大師級監控中 ({cnt}/5)</div>', unsafe_allow_html=True)

# 顯示路規偵測 (白底黑字)
insight_text, confidence = analyze_road_pro(st.session_state.history)
st.markdown(f"<div class='white-bar' style='margin-top: 15px;'>📝 {insight_text}</div>", unsafe_allow_html=True)

# 操作與按鈕邏輯
b1, b2, b3 = st.columns([2, 1, 2])
def update_pro(r):
    # 計算下一把預測 (含斷龍邏輯)
    last_8 = st.session_state.history[-8:]
    if len(last_8) == 8 and all(x == last_8[0] for x in last_8):
        pred = "閒" if last_8[0] == "莊" else "莊"
    else:
        pred = random.choice(["莊", "閒"])
    
    # 判斷輸贏與連勝
    if r != "和":
        if r == pred:
            st.session_state.win_streak += 1
            st.session_state.losses = 0
        else:
            st.session_state.win_streak = -1 # 斷連勝
            st.session_state.losses += 1
    
    st.session_state.history.append(r)

if b1.button("🔴 莊 家", use_container_width=True): update_pro("莊"); st.rerun()
if b2.button("和", use_container_width=True): st.session_state.history.append("和"); st.rerun()
if b3.button("🔵 閒 家", use_container_width=True): update_pro("閒"); st.rerun()

# --- 4. 注碼中心：1-3-2-4 鎖利建議 (滿 5 局門檻) ---
if cnt >= 5:
    st.markdown('<div class="bet-label-white">⚖️ 建議分配金額</div>', unsafe_allow_html=True)
    
    cc1, cc2, cc3 = st.columns([1, 6, 1])
    with cc2:
        bal = st.number_input("本金", value=10000, step=1000)
        rsk = st.slider("風險", 1, 10, 2)
    
    # 計算最終注碼
    if st.session_state.losses < 2:
        unit = get_bet_unit_1324(st.session_state.win_streak)
        base_bet = int(bal * (rsk/100))
        final_bet = base_bet * unit
        st.markdown(f'<p class="gold-number">{final_bet}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="gold-number" style="opacity:0.1;">0</p>', unsafe_allow_html=True)

if st.button("🧹 清除記錄 / 換桌", use_container_width=True):
    st.session_state.history = []; st.session_state.win_streak = 0; st.session_state.losses = 0; st.rerun()
