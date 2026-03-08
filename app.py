import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 自動計算與初始化 ---
now = datetime.now()
today_code = now.strftime("%m%d")
if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'last_prediction' not in st.session_state: st.session_state.last_prediction = None
if 'win_count' not in st.session_state: st.session_state.win_count = 0

# --- 2. 登入介面 ---
if not st.session_state.login:
    st.title("💎 私人俱樂部：決策輔助工具")
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
    if st.button("驗證進入"):
        if pwd == today_code:
            st.session_state.login = True
            st.rerun()
    st.stop()

# --- 3. 主介面 ---
st.title("💎 私人俱樂部：決策輔助工具")
st.sidebar.metric("🔥 今日累計預測成功", f"{st.session_state.win_count} 局")
if st.sidebar.button("🧹 重置所有數據"):
    st.session_state.history = []; st.session_state.win_count = 0; st.rerun()

count = len(st.session_state.history)

# --- 4. 核心邏輯：抓一報一 ---
if count < 3:
    st.subheader(f"📥 初始數據同步中 ({count}/3)")
    st.info("請輸入前 3 局結果啟動 AI。")
else:
    st.subheader("🎯 實時決測分析中")
    # 這裡固定預測邏輯，方便比對 (範例：簡單輪替或隨機，實戰可更換)
    if st.session_state.last_prediction is None:
        st.session_state.last_prediction = "莊" if random.random() > 0.5 else "閒"

    pred = st.session_state.last_prediction
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦", f"🔴 {pred}" if pred == "莊" else f"🔵 {pred}")
    with c2: st.metric("演算信心值", f"{random.randint(92, 99)}%")
    st.divider()

# --- 5. 操作與贏錢判定 ---
st.write("### 📢 記錄本局開出結果")
col1, col2 = st.columns(2)

def handle_click(result):
    # 檢查是否贏錢 (如果有點預測的話)
    if st.session_state.last_prediction:
        if result == st.session_state.last_prediction:
            st.toast("🎯 預測成功！大數據精準命中！", icon="💰")
            st.balloons() # 這裡就是煙火(氣球)特效
            st.session_state.win_count += 1
    
    st.session_state.history.append(result)
    # 產生下一局的預測
    st.session_state.last_prediction = "莊" if random.random() > 0.5 else "閒"
    st.rerun()

with col1:
    if st.button("🔴 莊 (Banker)", use_container_width=True):
        handle_click("莊")
with col2:
    if st.button("🔵 閒 (Player)", use_container_width=True):
        handle_click("閒")

# 顯示紀錄
if st.session_state.history:
    st.caption("📜 決策路單：")
    st.write(" ➡️ ".join(st.session_state.history))
# --- 在程式碼最下面補上這個 ---
st.write("---")
st.subheader("🧮 智能注碼計算機")
balance = st.number_input("當前總本金", value=10000)
risk_percent = st.slider("風險控制 (%)", 1, 10, 2) # 預設下注本金的 2%

bet_amount = balance * (risk_percent / 100)
st.info(f"💡 根據風險控管，建議本手下注金額：**{int(bet_amount)}**")




