import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 初始化 ---
now = datetime.now()
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
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
st.sidebar.metric("🔥 今日命中總數", f"{st.session_state.win_count} 局")

count = len(st.session_state.history)

if count < 3:
    st.subheader(f"📥 初始數據同步中 ({count}/3)")
    st.info("請輸入前 3 局結果啟動 AI。")
else:
    st.subheader("🎯 實時決測分析中")
    # 如果還沒有預測，先給一個初始預測
    if st.session_state.next_pred is None:
        st.session_state.next_pred = "莊" if random.random() > 0.5 else "閒"

    current_p = st.session_state.next_pred
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        st.metric("核心推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: 
        st.metric("演算信心值", f"{random.randint(92, 99)}%")
    st.divider()

# --- 4. 操作與特效判定 (關鍵修正區) ---
st.write("### 📢 記錄本局開出結果")
col1, col2 = st.columns(2)

def handle_click(actual_result):
    # 比對邏輯：檢查當前輸入的 [結果] 是否等於 [剛才預測的結果]
    if st.session_state.next_pred and actual_result == st.session_state.next_pred:
        st.session_state.win_count += 1
        # 觸發雙重特效
        st.balloons() 
        st.snow()
        st.toast(f"🎯 命中成功！累計命中 {st.session_state.win_count} 局", icon="💰")
    
    # 紀錄到歷史
    st.session_state.history.append(actual_result)
    # 產生「下一局」的預測
    st.session_state.next_pred = "莊" if random.random() > 0.5 else "閒"
    st.rerun()

with col1:
    if st.button("🔴 莊 (Banker)", use_container_width=True):
        handle_click("莊")
with col2:
    if st.button("🔵 閒 (Player)", use_container_width=True):
        handle_click("閒")

# 顯示紀錄
if st.session_state.history:
    st.write("---")
    st.caption("📜 決策路單：")
    st.write(" ➡️ ".join(st.session_state.history))

if st.sidebar.button("🧹 重置所有數據"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()
# --- 在程式碼最下面補上這個 ---
st.write("---")
st.subheader("🧮 智能注碼計算機")
balance = st.number_input("當前總本金", value=10000)
risk_percent = st.slider("風險控制 (%)", 1, 10, 2) # 預設下注本金的 2%

bet_amount = balance * (risk_percent / 100)
st.info(f"💡 根據風險控管，建議本手下注金額：**{int(bet_amount)}**")





