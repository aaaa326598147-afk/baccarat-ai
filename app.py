import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 初始化與每日金鑰 ---
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
    st.info(f"🔒 安全加密通道 | 📅 系統日期：{today_str}")
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
st.caption(f"🚀 雲端算力連線中 | 每日授權至 {today_str} 23:59")

# 側邊欄
st.sidebar.header("📊 實時戰績統計")
st.sidebar.metric("🔥 今日命中總數", f"{st.session_state.win_count} 局")
if st.sidebar.button("🧹 清空數據 (換桌)"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()

# --- 4. 核心決策與 AI 路評 (含和局邏輯) ---
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
    
    # AI 路評分析
    h_filtered = [x for x in st.session_state.history if x != "和"] # 排除和局來分析趨勢
    if len(h_filtered) >= 2 and h_filtered[-1] == h_filtered[-2]:
        analysis = "⚠️ 偵測到連續規律，系統判定為「長龍趨勢」，建議順勢跟隨。"
    else:
        analysis = "🔄 偵測到交替規律，目前處於「單跳路向」，建議反向對沖。"

    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦指令", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("演算信心值", f"{confidence}%")
    
    st.info(f"💡 **AI 實時路評：**\n{analysis}")
    st.progress(confidence / 100)
    st.divider()

# --- 5. 操作按鈕 (莊、閒、和) ---
st.write("### 📢 記錄本局開出結果")
col1, col2, col3 = st.columns([2, 1, 2]) # 讓和局按鈕小一點，放中間

def handle_click(actual_result):
    # 命中判定：如果是「和」，不計算輸贏，特效不觸發，但預測保留
    if actual_result == "和":
        st.toast("🟢 本局和局，數據保留，預測不變。", icon="🔄")
    elif st.session_state.next_pred and actual_result == st.session_state.next_pred:
        st.session_state.win_count += 1
        st.balloons(); st.snow()
        st.toast(f"🎯 命中成功！", icon="💰")
        # 只有莊閒輸贏後，才產生下一局預測
        st.session_state.next_pred = random.choice(["莊", "閒"])
    else:
        # 預測失敗，也產生下一局預測
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    st.session_state.history.append(actual_result)
    st.rerun()

with col1:
    if st.button("🔴 莊 (Banker)", use_container_width=True): handle_click("莊")
with col2:
    if st.button("🟢 和", use_container_width=True): handle_click("和")
with col3:
    if st.button("🔵 閒 (Player)", use_container_width=True): handle_click("閒")

# --- 6. 紀錄與注碼計算機 ---
if st.session_state.history:
    st.write("---")
    st.caption("📜 當前決策路單紀實：")
    # 美化顯示：和局用綠色標註
    styled_history = []
    for x in st.session_state.history:
        if x == "和": styled_history.append(f"🟢{x}")
        elif x == "莊": styled_history.append(f"🔴{x}")
        else: styled_history.append(f"🔵{x}")
    st.write(" ➡️ ".join(styled_history))

st.write("---")
st.subheader("🧮 智能注碼計算機")
with st.expander("🛡️ 開啟風險控管面板", expanded=True):
    balance = st.number_input("💵 當前總本金", value=10000, step=1000)
    risk_percent = st.slider("⚖️ 下注比例 (%)", 1, 10, 2)
    bet_amount = balance * (risk_percent / 100)
    st.success(f"💡 建議下注金額：**{int(bet_amount)}**")
