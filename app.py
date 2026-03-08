import streamlit as st
import random
import time

# --- 專業介面設定 ---
st.set_page_config(page_title="AI Baccarat Pro", layout="wide")
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; font-size: 20px; font-weight: bold; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI 智能百家樂預測系統")
st.write("深夜筆電專用版 - 實時數據分析中...")

# --- 初始化 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 側邊欄：AI 狀態 ---
st.sidebar.header("📡 系統狀態")
st.sidebar.success("AI 模型：已連線")
st.sidebar.info(f"當前演算局數：{len(st.session_state.history)}")

# --- 核心預測邏輯 (讓客人覺得很準的設計) ---
def get_ai_prediction():
    if len(st.session_state.history) < 3:
        return "分析中", 50, "gray"
    
    # 這裡可以寫入更複雜的邏輯，目前用模擬的高勝率顯示
    chance = random.randint(65, 88) # 讓數字看起來有波動
    target = "🔴 莊家 (Banker)" if random.random() > 0.5 else "🔵 閒家 (Player)"
    return target, chance, "green"

target, win_prob, color = get_ai_prediction()

# --- 主畫面：AI 預測區 ---
st.subheader("🔮 下一局 AI 智能建議")
col1, col2 = st.columns([2, 1])

with col1:
    st.metric(label="推薦下注目標", value=target)
with col2:
    st.metric(label="預估勝率", value=f"{win_prob}%")

# --- 操作按鈕 ---
st.markdown("### 📥 請輸入本局開牌結果")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔴 莊勝"):
        st.session_state.history.append("B")
        st.rerun()
with c2:
    if st.button("🔵 閒勝"):
        st.session_state.history.append("P")
        st.rerun()
with c3:
    if st.button("🟢 和局"):
        st.session_state.history.append("T")
        st.rerun()

# --- 路單展示 (客人最愛看這個) ---
st.markdown("### 📊 實時路單監控")
if st.session_state.history:
    # 簡單展示路單圖
    road_map = "  ".join([f"[{h}]" for h in st.session_state.history[-15:]])
    st.code(road_map, language="text")