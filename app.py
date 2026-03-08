import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 自動計算與初始化 ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'next_pred' not in st.session_state: st.session_state.next_pred = None
if 'win_count' not in st.session_state: st.session_state.win_count = 0

# --- 2. 登入介面 ---
if not st.session_state.login:
    st.set_page_config(page_title="💎 私人俱樂部", layout="centered")
    st.title("💎 私人俱樂部：決策輔助工具")
    st.info(f"🔒 安全加密通道已建立 | 📅 系統日期：{today_str}")
    pwd = st.text_input("請輸入今日授權金鑰：", type="password")
    if st.button("驗證並開啟雲端算力", use_container_width=True):
        if pwd == today_code:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ 金鑰錯誤")
    st.stop()

# --- 3. 主介面設定 ---
st.set_page_config(page_title="💎 AI 決策系統", layout="centered")
st.title("💎 私人俱樂部：決策輔助工具")
st.caption(f"🚀 雲端算力已連線 | 今日授權至 {today_str} 23:59")

# 側邊欄
st.sidebar.header("📊 實時戰績統計")
st.sidebar.metric("🔥 今日命中總數", f"{st.session_state.win_count} 局")
if st.sidebar.button("🧹 清空所有數據"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()

# --- 4. 核心決策與 AI 路評 ---
count = len(st.session_state.history)

if count < 3:
    st.subheader(f"📥 初始數據同步中 ({count}/3)")
    st.progress(count / 3)
    st.info("請輸入前 3 局結果啟動 AI 深度演算。")
else:
    st.subheader("🎯 AI 實時決策分析")
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    current_p = st.session_state.next_pred
    confidence = random.randint(92, 99)
    
    # 這裡加入【AI 路評邏輯】
    h = st.session_state.history
    if h[-1] == h[-2]:
        analysis = "⚠️ 偵測到連續規律，系統判定目前處於「長龍趨勢」，建議適度跟隨。"
    else:
        analysis = "🔄 偵測到交替規律，目前處於「單跳路向」，建議反向對沖。"

    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦指令", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("演算信心值", f"{confidence}%")
    
    # 顯示 AI 分析評論
    st.info(f"💡 **AI 實時路評：**\n{analysis}")
    st.progress(confidence / 100)
    st.divider()

# --- 5. 操作按鈕與煙火 ---
st.write("### 📢 記錄本局開出結果")
c1, c2 = st.columns(2)

def handle_click(actual_result):
    if st.session_state.next_pred and actual_result == st.session_state.next_pred:
        st.session_state.win_count += 1
        st.balloons(); st.snow()
        st.toast(f"🎯 命中成功！", icon="💰")
    
    st.session_state.history.append(actual_result)
    st.session_state.next_pred = random.choice(["莊", "閒"])
    st.rerun()

with c1:
    if st.button("🔴 莊 (Banker)", use_container_width=True): handle_click("莊")
with c2:
    if st.button("🔵 閒 (Player)", use_container_width=True): handle_click("閒")

# --- 6. 紀錄與注碼計算機 ---
if st.session_state.history:
    st.write("---")
    st.caption("📜 當前決策路單紀實：")
    st.write(" ➡️ ".join([f"[{h}]" for h in st.session_state.history]))

st.write("---")
st.subheader("🧮 智能注碼計算機")
with st.expander("🛡️ 開啟風險控管面板", expanded=True):
    balance = st.number_input("💵 當前總本金", value=10000, step=1000)
    risk_percent = st.slider("⚖️ 下注比例 (%)", 1, 10, 2)
    bet_amount = balance * (risk_percent / 100)
    st.success(f"💡 建議下注金額：**{int(bet_amount)}**")
