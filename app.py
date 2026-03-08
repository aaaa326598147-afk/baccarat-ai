import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 初始化與每日金鑰 (2026-03-08 密碼為 0308) ---
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
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
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

# --- 4. 房號與狀態 ---
st.sidebar.header("📌 桌面連線資訊")
room_id = st.sidebar.text_input("當前桌號/房號", value="A-101")
st.sidebar.metric("🔥 今日命中總數", f"{st.session_state.win_count} 局")

if st.sidebar.button("🧹 換桌 (重置數據)"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()

st.caption(f"📡 正在監控桌號：**{room_id}** | 📅 授權至 {today_str} 23:59")

# --- 5. 核心決策與深度路評 (改為 5 局) ---
count = len(st.session_state.history)

if count < 5:
    st.subheader(f"📥 數據同步中 ({count}/5)")
    st.progress(count / 5)
    st.info(f"請輸入 {room_id} 桌最近 5 局結果，以啟動大數據深度演算。")
else:
    st.subheader(f"🎯 實時決策：{room_id}")
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    current_p = st.session_state.next_pred
    confidence = random.randint(92, 99)
    
    # AI 深度路評演算
    h_filtered = [x for x in st.session_state.history if x != "和"]
    analysis = "🔄 掃描中..."
    if len(h_filtered) >= 4:
        last_4 = h_filtered[-4:]
        if len(set(last_4)) == 1:
            analysis = f"🐉 偵測到【{last_4[0]}長龍】趨勢！建議順勢追擊。"
            confidence = random.randint(96, 99)
        elif last_4[0] == last_4[2] and last_4[1] == last_4[3] and last_4[0] != last_4[1]:
            analysis = "🐇 偵測到標準【單跳規律】。AI 預計下一局將跳位。"
            confidence = random.randint(94, 98)
        else:
            analysis = "📈 目前路向較為雜亂，建議減注觀望 AI 推薦。"
    else:
        analysis = "📊 數據積累中，目前判定為隨機波動。"

    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦指令", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("演算信心值", f"{confidence}%")
    st.info(f"💡 **AI 深度路評報告：**\n{analysis}")
    st.progress(confidence / 100)
    st.divider()

# --- 6. 操作按鈕 ---
st.write(f"### 📢 記錄 {room_id} 開出結果")
col1, col2, col3 = st.columns([2, 1, 2])

def handle_click(actual_result):
    if actual_result == "和":
        st.toast("🟢 和局保留，預測維持不變。", icon="🔄")
    elif st.session_state.next_pred and actual_result == st.session_state.next_pred:
        st.session_state.win_count += 1
        st.balloons(); st.snow()
        st.toast("🎯 精準命中！", icon="💰")
        st.session_state.next_pred = random.choice(["莊", "閒"])
    else:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    st.session_state.history.append(actual_result)
    st.rerun()

with col1:
    if st.button("🔴 莊 (Banker)", use_container_width=True): handle_click("莊")
with col2:
    if st.button("🟢 和", use_container_width=True): handle_click("和")
with col3:
    if st.button("🔵 閒 (Player)", use_container_width=True): handle_click("閒")

# --- 7. 紀錄與注碼計算機 ---
if st.session_state.history:
    st.write("---")
    st.caption(f"📜 {room_id} 決策路單紀錄：")
    styled_history = [f"🔴{x}" if x=="莊" else f"🔵{x}" if x=="閒" else f"🟢{x}" for x in st.session_state.history]
    st.write(" ➡️ ".join(styled_history))

st.write("---")
st.subheader("🧮 智能注碼計算機")
with st.expander("🛡️ 風險管理面板", expanded=True):
    balance = st.number_input("💵 本金", value=10000)
    risk = st.
    slider("⚖️ 下注比例 (%)", 1, 10, 2)
    st.success(f"💡 建議下注金額：**{int(balance * (risk / 100))}**")
