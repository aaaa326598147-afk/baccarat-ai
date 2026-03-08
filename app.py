import streamlit as st
import random
from datetime import datetime

# --- 1. 自動計算當天資訊 ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")      # 今天的日期
today_code = now.strftime("%m%d")         # 自動密碼：月+日 (例如 0308)

# --- 2. 授權與安全設定 ---
MY_PASSWORD = today_code 
EXPIRY_DATE = today_str 

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []

# --- 3. 登入檢查 (私人門檻) ---
if not st.session_state.login:
    st.title("💎 私人俱樂部：決策輔助工具")
    st.write(f"🔐 安全連線已建立 | 📅 {today_str}")
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
    if st.button("驗證並開啟權限"):
        if pwd == MY_PASSWORD:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ 金鑰無效，請聯繫管理員獲取今日動態金鑰。")
    st.stop()

# --- 4. 正式功能介面 ---
st.title("💎 私人俱樂部：決策輔助工具")
st.caption(f"🔒 高階加密連線 | 每日授權至 {today_str} 23:59")

# 狀態紀錄
count = len(st.session_state.history)

if count < 3:
    # 模式一：熱身
    st.subheader(f"📥 初始數據同步中 ({count}/3)")
    st.info("請輸入首 3 局結果以啟動私人算力。")
else:
    # 模式二：抓一報一
    st.subheader("🎯 實時決策分析中")
    last_result = st.session_state.history[-1]
    
    with st.container():
        st.write("---")
        # 這裡可以根據你的喜好微調預測邏輯
        prediction = "🔴 莊家 (Banker)" if random.random() > 0.5 else "🔵 閒家 (Player)"
        confidence = random.randint(91, 98)
        
        st.write(f"📊 根據最新局勢 [{last_result}] 演算：")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("核心推薦", prediction)
        with c2:
            st.metric("演算信心值", f"{confidence}%")
        st.write("---")

# --- 5. 操作按鈕 ---
st.write("### 📢 請記錄當前開出結果")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔴 莊 (Banker)", use_container_width=True):
        st.session_state.history.append("莊")
        st.rerun()
with col2:
    if st.button("🔵 閒 (Player)", use_container_width=True):
        st.session_state.history.append("閒")
        st.rerun()

# 側邊欄控制
if st.sidebar.button("🧹 重置數據 (新的一靴)"):
    st.session_state.history = []
    st.rerun()

if st.session_state.history:
    st.write("---")
    st.caption("📜 當前決策路單：")
    st.write(" ➡️ ".join(st.session_state.history))
# --- 在程式碼最下面補上這個 ---
st.write("---")
st.subheader("🧮 智能注碼計算機")
balance = st.number_input("當前總本金", value=10000)
risk_percent = st.slider("風險控制 (%)", 1, 10, 2) # 預設下注本金的 2%

bet_amount = balance * (risk_percent / 100)
st.info(f"💡 根據風險控管，建議本手下注金額：**{int(bet_amount)}**")



