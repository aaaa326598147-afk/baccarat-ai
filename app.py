import streamlit as st
import random
from datetime import datetime
import os

# --- 1. AI 權威路評核心邏輯 (含階梯路偵測與百位取整) ---
def get_ai_road_analysis(history, capital):
    if len(history) < 5: 
        return "⚖️ 數據樣本蒐集預熱中...", 0, 0, False
    
    valid_history = [x for x in history if x != "和"]
    path = "".join(valid_history[-12:]) 
    last_4 = "".join(valid_history[-4:])
    
    status = "⚖️ 盤勢平衡：建議觀察趨勢"
    bonus_conf = 0
    
    # --- 專業術語偵測區 (V14.19 更新) ---
    if "莊莊莊莊" in path or "閒閒閒閒" in path:
        status = "🐉 龍體成型：趨勢明確，建議順龍切入"; bonus_conf = 35
    elif "莊閒莊閒" in last_4 or "閒莊閒莊" in last_4:
        status = "🎯 規律單跳：穩定規律，捕捉跳位獲利"; bonus_conf = 28
    # 階梯路偵測 (遞增重複排列)
    elif any(x in path for x in ["莊閒閒莊莊莊", "閒莊莊閒閒閒", "莊莊閒閒閒", "閒閒莊莊莊"]):
        status = "📈 階梯路現蹤：數據遞增規律，穩定跟進"; bonus_conf = 32
    elif "莊莊閒閒" in path or "閒閒莊莊" in path:
        status = "🎨 雙跳趨勢：規律分明"; bonus_conf = 25
    
    b_c = valid_history.count("莊"); p_c = valid_history.count("閒")
    bias = abs(p_c - b_c) * 3.2 
    final_conf = int(max(min(52 + bias + bonus_conf + random.randint(0,2), 99), 50))
    
    # 避險邏輯 (SAFE MODE 門檻)
    base_ratio = 0.1
    if final_conf > 85: base_ratio = 0.28
    elif final_conf > 70: base_ratio = 0.15
    elif final_conf < 58: base_ratio = 0  
    
    # 百位取整邏輯
    raw_amount = capital * base_ratio
    suggested_amount = int(round(raw_amount / 100) * 100) if raw_amount > 0 else 0
    if base_ratio > 0 and suggested_amount == 0: suggested_amount = 100
    
    return status, final_conf, suggested_amount, True

# --- 2. 界面 CSS 強化 (暗黑色系 + 金色質感) ---
st.set_page_config(page_title="VIP 數據中心", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0F1116; }
    .white-bar { background: #FFFFFF !important; border-radius: 50px; padding: 12px; text-align: center; color: #000 !important; font-weight: bold; margin-bottom: 12px; }
    .gold-amount { color: #D4AF37 !important; font-size: 75px !important; font-weight: 900 !important; text-align: center; margin: -10px 0; }
    .balance-box { background: rgba(255,255,255,0.08); padding: 15px; border-radius: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.15); margin-bottom: 20px; }
    .road-map-container { display: flex; flex-wrap: wrap; gap: 8px; background: rgba(255, 255, 255, 0.05); border: 1.5px solid #D4AF37; border-radius: 20px; padding: 15px; min-height: 100px; margin: 10px 0; justify-content: flex-start; }
    .lock-box { height: 180px; display: flex; align-items: center; justify-content: center; border: 2px dashed rgba(255,255,255,0.2); border-radius: 25px; margin: 10px 0; background: rgba(0,0,0,0.3); }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 狀態初始化與分級登入 ---
if 'login' not in st.session_state: st.session_state.login = False
if 'member_level' not in st.session_state: st.session_state.member_level = "基礎版"
if 'history' not in st.session_state: st.session_state.history = []
if 'current_balance' not in st.session_state: st.session_state.current_balance = 10000.0
if 'locked_room' not in st.session_state: st.session_state.locked_room = None

if not st.session_state.login:
    st.markdown("<br><br><br><h1 style='text-align:center; color:white;'>VIP 數據授權登入</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed", placeholder="請輸入 4-5 位授權密碼")
    today = datetime.now().strftime("%m%d") # 獲取當前月日 0309
    
    if st.button("啟動系統", use_container_width=True):
        if pwd == today:
            st.session_state.login = True; st.session_state.member_level = "基礎版"; st.rerun()
        elif pwd == today + "8": # 專業版密碼 03098
            st.session_state.login = True; st.session_state.member_level = "專業版"; st.rerun()
        else:
            st.error("授權密碼錯誤或已失效")
    st.stop()

# 選擇桌號邏輯
if st.session_state.locked_room is None:
    st.markdown("<br><br><h2 style='text-align:center; color:white;'>選擇監控桌號</h2>", unsafe_allow_html=True)
    rooms = ["— 請選擇實時監控房號 —"] + [f"RB0{i}" for i in range(1, 8)] + [f"S0{i}" for i in range(1, 8)]
    sel_room = st.selectbox("ROOM", options=rooms, label_visibility="collapsed")
    if sel_room != rooms[0]: st.session_state.locked_room = sel_room; st.rerun()
    st.stop()

# --- 4. 主介面展示 ---
# 頂部權限與房號標籤
level_info = "🔰 基礎授權模式 (01-07房)" if st.session_state.member_level == "基礎版" else "💎 專業轉線旗艦版 (全功能解鎖)"
st.markdown(f'<div style="text-align:center; color:#D4AF37; font-size:14px; font-weight:bold; margin-bottom:5px;">{level_info}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:#888; font-size:12px; margin-bottom:15px;">當前監控中：{st.session_state.locked_room}</div>', unsafe_allow_html=True)

# 餘額與複利顯示
st.markdown(f'<div class="balance-box"><span style="color:#AAA; font-size:12px;">當前帳戶餘額 (AI 複利計算中)</span><br><span style="color:#FFF; font-size:24px; font-weight:bold;">${st.session_state.current_balance:,.0f}</span></div>', unsafe_allow_html=True)

insight, conf, amount, is_unlocked = get_ai_road_analysis(st.session_state.history, st.session_state.current_balance)

if is_unlocked:
    if amount == 0:
        if st.session_state.member_level == "專業版":
            st.markdown(f"""<div class="lock-box" style="border: 2px solid #D4AF37; background: rgba(212,175,55,0.1);"><div style="text-align:center;"><p style="color:#D4AF37; font-size:32px; font-weight:bold; margin:0;">SAFE MODE</p><p style="color:#FFF; font-size:16px;">AI 偵測亂路，已自動避險</p></div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="lock-box"><div style="text-align:center;"><p style="color:#555; font-size:32px; font-weight:bold; margin:0;">🔒 功能鎖定</p><p style="color:#444; font-size:14px;">高階避險偵測僅限專業版</p></div></div>""", unsafe_allow_html=True)
    else:
        # 顯示 AI 預測大字與信心度
        b_c = st.session_state.history.count("莊"); p_c = st.session_state.history.count("閒")
        next_p = "莊" if p_c >= b_c else "閒"; p_color = "#FF4B4B" if next_p == "莊" else "#4B4BFF"
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div style="text-align:center;"><p style="color:#AAA; font-size:14px; margin:0;">AI 預測</p><p style="color:{p_color}; font-size:100px; font-weight:900; margin:-20px 0;">{next_p}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div style="text-align:center;"><p style="color:#AAA; font-size:14px; margin:0;">信心度</p><p style="color:#FFF; font-size:100px; font-weight:900; margin:-20px 0;">{conf}%</p></div>', unsafe_allow_html=True)
        
        # 顯示百位整數配注金額
        st.markdown(f'<p class="gold-amount">{amount:,}</p>', unsafe_allow_html=True)
        
        # 結算按鈕 (分權限)
        if st.session_state.member_level == "專業版":
            s1, s2 = st.columns(2)
            if s1.button("✅ 獲利結算", use_container_width=True): st.session_state.current_balance += amount; st.rerun()
            if s2.button("❌ 失利結算", use_container_width=True): st.session_state.current_balance -= amount; st.rerun()
        else:
            st.markdown('<div style="text-align:center; padding:10px; background:rgba(255,0,0,0.1); border-radius:10px; color:#FF4B4B; font-size:12px; border: 1px solid #FF4B4B;">⚠️ 自動結算功能已鎖定，請升級專業授權</div>', unsafe_allow_html=True)
else:
    # 預熱中畫面
    st.markdown(f"""<div class="lock-box"><div style="text-align:center;"><p style="color:#888; font-size:24px; margin:0;">⌛ 數據分析鎖定中</p><p style="color:#555; font-size:14px;">請連續輸入 {5 - len(st.session_state.history)} 局開牌紀錄</p></div></div>""", unsafe_allow_html=True)

# 珠盤路圖顯示
road_html = "".join([f'<div style="width:30px; height:30px; border-radius:50%; background:{"#FF4B4B" if i=="莊" else "#4B4BFF" if i=="閒" else "#28A745"}; display:flex; align-items:center; justify-content:center; color:white; font-size:12px; font-weight:bold; border:1px solid rgba(255,255,255,0.2);">{i}</div>' for i in st.session_state.history])
st.markdown(f'<div class="road-map-container">{road_html}</div>', unsafe_allow_html=True)

# 開牌動作按鈕
b1, b2, b3 = st.columns([2, 1, 2])
def update_action(r):
    st.session_state.history.append(r); st.rerun()
if b1.button("🔴 莊 家", use_container_width=True): update_action("莊")
if b2.button("和", use_container_width=True): update_action("和")
if b3.button("🔵 閒 家", use_container_width=True): update_action("閒")

# 專業術語即時路評 (包含階梯路偵測)
st.markdown(f"<div class='white-bar' style='margin-top:15px;'>{insight}</div>", unsafe_allow_html=True)

# 底部重置功能
if st.button("更換桌號 / 重置系統數據", use_container_width=True):
    st.session_state.history = []; st.session_state.locked_room = None; st.session_state.current_balance = 10000.0; st.rerun()
