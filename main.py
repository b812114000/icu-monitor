import streamlit as st
import pandas as pd
from datetime import datetime
import time

# 1. 網頁基本設定 (設定為寬版模式)
st.set_page_config(page_title="第10組 ICU 臨床單床監護儀", page_icon="🏥", layout="wide")

# =================【前端 JavaScript 實時點擊驅動器】=================
# 每 3 秒強迫瀏覽器向後端發送 Rerun 訊號，確保全網頁與資料庫同步刷新
st.components.v1.html(
    """
    <script>
        const interval = setInterval(function() {
            const windowParent = window.parent;
            if (windowParent) {
                windowParent.postMessage({type: 'streamlit:rerun'}, '*');
            }
        }, 3000); // 3000 毫秒 = 3 秒
    </script>
    """,
    height=0,
)
# =========================================================================

st.logo("🏥")

# 2. 全域 CSS 樣式面板優化 (包含危急警報閃爍動畫)
st.markdown("""
    <style>
    .stApp {
        background-color: #06090E;
        color: #E2E8F0;
    }
    .monitor-panel {
        background-color: #0F131A;
        border: 2px solid #1E293B;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        margin-bottom: 20px;
    }
    .status-stable { border-top: 8px solid #10B981 !important; }
    .status-warning { border-top: 8px solid #F59E0B !important; }
    .status-critical {
        border-top: 8px solid #EF4444 !important;
        animation: card-blink 1s infinite alternate;
    }
    @keyframes card-blink {
        0% { border-top-color: #EF4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }
        100% { border-top-color: #7F1D1D; box-shadow: 0 0 30px rgba(239, 68, 68, 0.7); }
    }
    .vital-card {
        background-color: #06090E; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #1E293B; 
        text-align: center;
    }
    .vital-value {
        font-family: 'Courier New', Courier, monospace;
        font-size: 52px;
        font-weight: bold;
        line-height: 1.1;
        margin-top: 10px;
    }
    .text-bpm { color: #10B981; }
    .text-spo2 { color: #38BDF8; }
    .text-bp { color: #ECC94B; }
    .text-alert { color: #F87171; font-weight: 900; }
    .text-gray { color: #64748B; }
    </style>
""", unsafe_allow_html=True)

# 3. 頂部中央監控台標頭
st.markdown(f"""
    <div style="background-color: #0F131A; padding: 15px 25px; border-radius: 8px; border: 1px solid #1E293B; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div>
            <h1 style="color: #38BDF8; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 1px;">🏥 CLINICAL PATIENT MONITOR</h1>
            <p style="color: #64748B; margin: 3px 0 0 0; font-size: 13px;">第 10 組 醫療數據中央監控台 | 實時數據接收端 (Active)</p>
        </div>
        <div style="text-align: right;">
            <span style="background-color: #1E293B; padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #34D399; font-weight: bold;">● LIVE LINK</span>
            <p style="color: #94A3B8; margin: 5px 0 0 0; font-size: 11px; font-family: monospace;">最後同步: {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. 資料獲取與解析 (強力摧毀 Google Sheets 的快取機制)
sheet_url = "https://docs.google.com/spreadsheets/d/1sBJR8rompMp7PwcGHBaXWmjeEUHjdMHc3GokhqJCTtE/edit?gid=0#gid=0"

try:
    csv_url = sheet_url.split('/edit')[0] + '/export?format=csv'
    # 網址後面強行加上亂數時間戳記，繞過 Google Sheets 伺服器端暫存限制
    df = pd.read_csv(f"{csv_url}&nocache={time.time()}")
