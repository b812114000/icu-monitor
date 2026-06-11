import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random

# 1. 網頁基本設定
st.set_page_config(page_title="第10組 ICU 臨床單床監護儀", page_icon="🏥", layout="wide")

# 前端 5 秒自動刷新
st.components.v1.html(
    """
    <script>
        const interval = setInterval(function() {
            const windowParent = window.parent;
            if (windowParent) { windowParent.postMessage({type: 'streamlit:rerun'}, '*'); }
        }, 5000);
    </script>
    """,
    height=0,
)

st.logo("🏥")

# 2. 全域 CSS
st.markdown("""
    <style>
    .stApp { background-color: #06090E; color: #E2E8F0; }
    .monitor-panel { background-color: #0F131A; border: 2px solid #1E293B; border-radius: 12px; padding: 20px; margin-bottom: 15px; border-top: 8px solid #10B981; }
    .vital-card { background-color: #06090E; padding: 15px; border-radius: 8px; border: 1px solid #1E293B; text-align: center; height: 140px; }
    .vital-value { font-family: 'Courier New', Courier, monospace; font-weight: bold; line-height: 1.1; margin-top: 5px; font-size: 42px; }
    </style>
""", unsafe_allow_html=True)

# 3. 標頭
st.markdown(f"""
    <div style="background-color: #0F131A; padding: 15px 25px; border-radius: 8px; border: 1px solid #1E293B; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <h1 style="color: #38BDF8; margin: 0; font-size: 24px; font-weight: 800;">🏥 CLINICAL PATIENT MONITOR</h1>
            <p style="color: #64748B; margin: 3px 0 0 0; font-size: 12px;">第 10 組 醫療數據中央監控台</p>
        </div>
        <div style="text-align: right;">
            <p style="color: #94A3B8; margin: 0; font-size: 12px; font-family: monospace;">網頁刷新時間: {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. 資料獲取（加入極端偵錯模式）
sheet_url = "https://docs.google.com/spreadsheets/d/1pg-uFGYgdBANJOnRxqiRo64IhgYH4FDuZPlmOFYFHpU/edit?hl=zh-tw&gid=0#gid=0"
debug_msg = "正常連線"
error_detail = ""

try:
    base_url = sheet_url.split('/edit')[0]
    csv_url = f"{base_url}/export?format=csv"
    cache_buster = f"&nocache={time.time()}&rand={random.randint(10000, 99999)}"
    
    # 讀取 CSV
    df = pd.read_csv(csv_url + cache_buster)
    
    # 強制轉型
    df['Systolic'] = pd.to_numeric(df['Systolic'], errors='coerce').fillna(120).astype(int)
    df['Diastolic'] = pd.to_numeric(df['Diastolic'], errors='coerce').fillna(80).astype(int)
    df['SpO2'] = pd.to_numeric(df['SpO2'], errors='coerce').fillna(98.0).astype(float)
    df['HeartRate'] = pd.to_numeric(df['HeartRate'], errors='coerce').fillna(75).astype(int)
    df['Alert'] = df['Alert'].astype(str).str.strip()
    
    # 抓取最新一筆
    latest_row = df.iloc[-1]
    current_sys = int(latest_row['Systolic'])
    current_dia = int(latest_row['Diastolic'])
    current_spo2 = float(latest_row['SpO2'])
    current_hr = int(latest_row['HeartRate'])
    colab_alert = str(latest_row['Alert'])
    
    chart_data = df[['Systolic', 'Diastolic', 'SpO2', 'HeartRate']]
except Exception as e:
    debug_msg = "❌ 讀取發生錯誤"
    error_detail = str(e)
    current_sys, current_dia, current_spo2, current_hr = 0, 0, 0, 0
    colab_alert = "ERROR"
    chart_data = pd.DataFrame()

# 5. 渲染主要面板
st.markdown(f"""
    <div class="monitor-panel">
        <span style="font-size: 20px; font-weight: 800; color: #FFF;">🛏️ TARGET LOCATION: BED-001</span>
    </div>
""", unsafe_allow_html=True)

# 6. 三欄數據卡
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="vital-card"><div style="color:#64748B;">NIBP</div><div class="vital-value" style="color:#ECC94B;">{current_sys}/{current_dia}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="vital-card"><div style="color:#64748B;">SpO2</div><div class="vital-value" style="color:#38BDF8;">{current_spo2:.1f}%</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="vital-card"><div style="color:#64748B;">HR</div><div class="vital-value" style="color:#10B981;">{current_hr} BPM</div></div>', unsafe_allow_html=True)

# 7. 圖表
st.markdown("<br>", unsafe_allow_html=True)
if not chart_data.empty:
    st.line_chart(chart_data.tail(30), height=250)

# =========================================================================
# 🛠️ 【第 10 組專用：極端後台數據抓漏面板】
# =========================================================================
st.markdown("---")
st.subheader("🛠️ 後台連線抓漏實時狀態 (上台前請刪除此區塊)")

col_a, col_b = st.columns(2)
with col_a:
    st.metric("目前雲端資料庫「總資料筆數」", len(chart_data) if not chart_data.empty else 0)
    st.text(f"連線診斷狀態: {debug_msg}")
    if error_detail:
        st.error(f"Python 報錯原因: {error_detail}")

with col_b:
    st.write("▼ 目前 Python 真正從網路上抓到的最後 3 筆資料（對照 Google 用）：")
    if not chart_data.empty:
        st.dataframe(df.tail(3)[['Timestamp', 'Systolic', 'Diastolic', 'SpO2', 'HeartRate', 'Alert']])
    else:
        st.warning("完全抓不到任何資料，請檢查 Google 試算表是否已被意外關閉『發布到網路』！")
