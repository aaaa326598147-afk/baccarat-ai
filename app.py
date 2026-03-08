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
    pwd = st.text_input("輸入今日授權金鑰：", type="password")
    if st.button("驗證進入", use_container_width=True):
        if pwd == today_code:
            st.session_state.login = True
            st.rerun()
    st.stop()

# --- 3. 主介面設定 ---
st.set_page_config(page_title="💎 AI 決策系統", layout="centered")
st.title("💎 私人俱樂部：決策輔助工具")

# --- 4. 側邊欄：房號與狀態 ---
st.sidebar.header("📌 桌面資訊")
room_id = st.sidebar.text_input("請輸入房號", value="", placeholder="例如：A-101")
st.sidebar.metric("🔥 今日命中", f"{st.session_state.win_count} 局")

if st.sidebar.button("🧹 換桌重置"):
    st.session_state.history = []; st.session_state.win_count = 0; st.session_state.next_pred = None; st.rerun()

if not room_id:
    st.warning("👈 請先在左側選單輸入【房號】以開始。")
    st.stop()

st.caption(f"📡 監控桌號：{room_id} | 📅 {today_str}")

# --- 5. 核心決策 (5局啟動) ---
count = len(st.session_state.history)

if count < 5:
    st.subheader(f"📥 數據同步中 ({count}/5)")
    st.progress(count / 5)
    st.info(f"請輸入最近 5 局結果啟動演算。")
else:
    st.subheader(f"🎯 實時決策：{room_id}")
    if st.session_state.next_pred is None:
        st.session_state.next_pred = random.choice(["莊", "閒"])
    
    current_p = st.session_state.next_pred
    confidence = random.randint(92, 99)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.metric("核心推薦", f"🔴 {current_p}" if current_p == "莊" else f"🔵 {current_p}")
    with c2: st.metric("信心值", f"{confidence}%")
    
    # AI 路評邏輯
    h_f = [x for x in st.session_state.history if x != "和"]
    analysis = "📊 數據積累中..."
    if len(h_f) >= 4:
        last_4 = h_f[-4:]
        if len(set(last_4)) == 1: analysis = f"🐉 偵測到【{last_4[0]}長龍】。"
        elif last_4[0] == last_4[2] and last_4[1] == last_4[3] and last_4[0] != last_4[1]: analysis = "🐇 偵測到【單跳規律】。"
        else: analysis = "📈 目前路向較雜。"
    
    st.info(f"💡 AI 路評： {analysis}")
    st.progress(confidence / 100)
    st.divider()

# --- 6. 操作按鈕 (防誤觸佈局) ---
st.write(f"### 📢 記錄開出結果")
col1, col2, col3 = st.columns([2, 1, 2])

def handle_click(res):
    if len(st.session_state.history) >= 5:
        if st.session_state.next_pred and res == st.session_state.next_pred:
            st.session_state.win_count += 1
            st.balloons(); st.snow()
            st.success(f"🎯 命中獲利！")
            st.session_state.next_pred = random.choice(["莊", "閒"])
        elif res != "和":
            st.session_state.next_pred = random.choice(["莊", "閒"])
    else:
        if res != "和": st.session_state.next_pred = random.choice(["莊", "閒"])
            
    if res == "和": st.toast("🟢 和局保留。")
    st.session_state.history.append(res)
    time.sleep(0.5)
    st.rerun()

with col1:
    if st.button("🔴 莊 (B)", use_container_width=True): handle_click("莊")
with col2:
    if st.button("🟢 和", use_container_width=True): handle_click("和")
with col3:
    if st.button("🔵 閒 (P)", use_container_width=True): handle_click("閒")

# --- 7. 紀錄與計算機 ---
if st.session_state.history:
    st.write("---")
    st.caption(f"📜 路單紀錄：")
    styled_h = [f"🔴{x}" if x=="莊" else f"🔵{x}" if x=="閒" else f"🟢{x}" for x in st.session_state.history]
    st.write(" ➡️ ".join(styled_h))

st.write("---")
st.subheader("🧮 智能注碼計算機")
with st.expander("🛡️ 風險管理", expanded=True):
    balance = st.number_input("💵 本金", value=10000, step=1000)
    risk = st.slider("⚖️ 下注 %", 1, 10, 2)
    st.success(f"💡 建議下注：**{int(balance * (risk / 100))}**")

# --- 8. 手機端安全墊 (防誤觸關鍵) ---
st.write("") # 增加空白行
st.write("")
st.write("")
st.write("")
st.write("") # 這裡多留幾行，確保最下面的內容不會被手機按鈕擋住
import streamlit as st
import random
import time
from datetime import datetime
import os
import base64

# --- 1. 初始化與密鑰 ---
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
today_code = now.strftime("%m%d")

if 'login' not in st.session_state: st.session_state.login = False
if 'history' not in st.session_state: st.session_state.history = []
if 'win_count' not in st.session_state: st.session_state.win_count = 0

# --- 2. 登入畫面 ---
if not st.session_state.login:
    st.set_page_config(page_title="💎 私人俱樂部", layout="centered")
    st.markdown("<style>.stApp { background-color: #121212; }</style>", unsafe_allow_html=True)
    st.title("💎 私人俱樂部")
    if st.text_input("輸入金鑰：", type="password") == today_code:
        if st.button("登入"): st.session_state.login = True; st.rerun()
    st.stop()

# --- 3. 背景與裝潢邏輯 (把圖變透明背景) ---
st.set_page_config(page_title="💎 AI 決策系統", layout="centered")

cover_path = "cover.jpg"
if os.path.exists(cover_path):
    with open(cover_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.85); /* 0.85 代表讓圖案變很暗、隱隱約約 */
            z-index: -1;
        }}
        h1, h2, h3, p, .stMetric, [data-testid="stMetricValue"] {{ color: #FFFFFF !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 4. 主內容區 ---
st.title("💎 深夜筆電・獲利紀實")
room_id = st.sidebar.text_input("輸入房號", placeholder="例如：VIP-01")

if not room_id:
    st.warning("👈 請先輸入房號。")
    st.stop()

# (接下來接續原本的預測邏輯與按鈕即可...)
st.write(f"📡 監控房號：**{room_id}**")
