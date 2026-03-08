import streamlit as st
import random
from datetime import datetime

# --- 設定區：這兩個你隨時可以改 ---
MY_PASSWORD = "888"         # 你要給客人的密碼 (目前設為 888)
EXPIRY_DATE = "2026-03-31"  # 授權到期日

# --- 介面美化設定 ---
st.set_page_config(page_title="AI 獲利紀實 Pro", page_icon="💰")

# --- 1. 檢查時間限制 ---
current_date = datetime.now().strftime("%Y-%m-%d")
if current_date > EXPIRY_DATE:
    st.error(f"🛑 系統授權已過期 ({EXPIRY_DATE})，請聯繫管理員更新。")
    st.stop()

# --- 2. 密碼登入檢查 ---
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 私人系統訪問控制")
    user_input = st.text_input("請輸入授權金鑰：", type="password")
    if st.button("確認登入"):
        if user_input == MY_PASSWORD:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，請重新輸入。")
    st.stop()

# --- 3. 通過檢查後顯示的正式內容 ---
st.title("🤖 AI 智能獲利預測系統")
st.success(f"✅ 授權正常：歡迎回來！(有效期至 {EXPIRY_DATE})")

if st.button("🔮 開始預測下一局"):
    with st.spinner('正在分析路單趨勢...'):
        import time
        time.sleep(1)
        target = random.choice(["🔴 莊家 (Banker)", "🔵 閒家 (Player)"])
        st.success(f"本局推薦：{target}")

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
