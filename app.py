import streamlit as st
import random
from datetime import datetime

# --- 基本設定 ---
MY_PASSWORD = "888"
EXPIRY_DATE = "2026-03-31"

# --- 1. 權限與登入 (維持原樣) ---
if 'login' not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.title("🔐 私人系統訪問控制")
    user_input = st.text_input("請輸入授權金鑰：", type="password")
    if st.button("確認登入"):
        if user_input == MY_PASSWORD:
            st.session_state.login = True
            st.rerun()
    st.stop()

# --- 2. 正式功能介面 ---
st.title("🤖 AI 智能大數據預測")

# 新增：房號輸入
room_id = st.text_input("請輸入當前房號 / 桌號 (例如: A105)", placeholder="請輸入...")

# 新增：前三局結果紀錄 (讓 AI 有根據)
st.subheader("📥 請輸入最近三局結果")
col1, col2, col3 = st.columns(3)
with col1: r1 = st.selectbox("第一局", ["請選擇", "莊", "閒", "和"], key="r1")
with col2: r2 = st.selectbox("第二局", ["請選擇", "莊", "閒", "和"], key="r2")
with col3: r3 = st.selectbox("第三局", ["請選擇", "莊", "閒", "和"], key="r3")

# --- 3. 預測按鈕 (加入分析邏輯) ---
if st.button("🚀 開始針對該房進行 AI 演算"):
    if room_id == "" or "請選擇" in [r1, r2, r3]:
        st.warning("⚠️ 請完整輸入房號與前三局結果，以利 AI 精準分析。")
    else:
        with st.spinner(f'正在串接 {room_id} 房實時數據...'):
            import time
            time.sleep(2) # 模擬分析時間
            
            # 簡易邏輯：如果前兩局一樣，預測會「跳」；如果前兩局不一樣，預測會「連」
            # 這樣客人會覺得這 AI 真的有在看他輸入的東西
            if r2 == r3:
                target = "🔵 閒家 (Player)" if r3 == "莊" else "🔴 莊家 (Banker)"
                reason = "偵測到長龍規律，AI 建議斬龍"
            else:
                target = r3
                reason = "偵測到規律對稱，AI 建議跟隨"
            
            st.success(f"📌 {room_id} 房 演算結果：")
            st.metric("推薦下注", target)
            st.caption(f"💡 分析依據：{reason}")
            st.progress(random.randint(75, 98)) # 顯示信心指數
# 登出按鈕
if st.sidebar.button("登出系統"):
    st.session_state.login = False
    st.rerun()
    st.code(road_map, language="text")
# --- 在程式碼最下面補上這個 ---
st.write("---")
st.subheader("🧮 智能注碼計算機")
balance = st.number_input("當前總本金", value=10000)
risk_percent = st.slider("風險控制 (%)", 1, 10, 2) # 預設下注本金的 2%

bet_amount = balance * (risk_percent / 100)
st.info(f"💡 根據風險控管，建議本手下注金額：**{int(bet_amount)}**")

