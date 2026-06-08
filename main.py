import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="第10組 ICU 臨床單床監護儀", page_icon="🏥", layout="wide")

# 【核心大絕招】直接命令網頁瀏覽器每 3 秒自動按一次 F5 重新整理
st.markdown('<meta http-equiv="refresh" content="3">', unsafe_allow_html=True)

st.logo("🏥") 

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
    }
    .status-stable { border-top: 8px solid #10B981 !important; }
    .status-critical {
        border-top: 8px solid #EF4444 !important;
        animation: card-blink 1s infinite alternate;
    }
    @keyframes card-blink {
        0% { border-top-color: #EF4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }
        100% { border-top-color: #7F1D1D; box-shadow: 0 0 30px rgba(239, 68, 68, 0.7); }
    }
    .vital-value {
        font-family: 'Courier New', Courier, monospace;
        font-size: 50px;
        font-weight: bold;
        line-height: 1;
        margin-top: 10px;
    }
    .text-bpm { color: #10B981; }
    .text-spo2 { color: #38BDF8; }
    .text-bp { color: #ECC94B; }
    .text-alert { color: #F87171; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background-color: #0F131A; padding: 15px 25px; border-radius: 8px; border: 1px solid #1E293B; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div>
            <h1 style="color: #38BDF8; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 1px;">🏥 CLINICAL PATIENT MONITOR</h1>
            <p style="color: #64748B; margin: 3px 0 0 0; font-size: 13px;">第 10 組 醫療數據中央監控台 | 實時數據接收端 (Active)</p>
        </div>
        <div style="text-align: right;">
            <span style="background-color: #1E293B; padding: 6px 12px; border-radius: 20px; font-size: 12px; color: #34D399; font-weight: bold;">● LIVE LINK</span>
            <p style="color: #94A3B8; margin: 5px 0 0 0; font-size: 11px; font-family: monospace;">最後同步: """ + datetime.now().strftime('%H:%M:%S') + """</p>
        </div>
    </div>
""", unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/1sBJR8rompMp7PwcGHBaXWmjeEUHjdMHc3GokhqJCTtE/edit?gid=0#gid=0"

try:
    csv_url = sheet_url.split('/edit')[0] + '/export?format=csv'
    # 網址強行加上不可預測的時間戳記，絕對破除試算表所有的快取快取機制
    df = pd.read_csv(f"{csv_url}&nocache={time.time()}")
    latest_row = df.iloc[-1]
    current_sys = int(latest_row['Systolic'])
    current_dia = int(latest_row['Diastolic'])
    current_spo2 = float(latest_row['SpO2'])
    current_hr = int(latest_row['HeartRate'])
    colab_alert = str(latest_row['Alert'])

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    chart_data = df.set_index('Timestamp')[['Systolic', 'Diastolic', 'SpO2', 'HeartRate']]
    error_mode = False
except Exception as e:
    error_mode = True
    current_sys, current_dia, current_spo2, current_hr = 120, 80, 98, 72
    colab_alert = "NORMAL"
    chart_data = pd.DataFrame()

diagnostic_status = "臨床徵象穩定"
is_critical = False
status_color = "#10B981"

if colab_alert != "NORMAL":
    is_critical = True
    status_color = "#EF4444"
    if colab_alert == "EMERGENCY_HIGH_BP":
        diagnostic_status = "🚨 CRITICAL：血壓極度過高！"
    elif colab_alert == "EMERGENCY_LOW_SPO2":
        diagnostic_status = "🚨 CRITICAL：急性血氧偏低！"
    elif colab_alert == "EMERGENCY_HIGH_HR":
        diagnostic_status = "🚨 CRITICAL：急性心搏過速！"
    elif colab_alert == "EMERGENCY_LOW_HR":
        diagnostic_status = "🚨 CRITICAL：急性心搏過緩！"

card_style = "status-critical" if is_critical else "status-stable"

panel_html = """
    <div class="monitor-panel {c_style}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 28px; font-weight: 800; color: #FFF; letter-spacing: 1px;">🛏️ TARGET LOCATION: BED-001</span>
            <span style="background-color: {s_color}22; border: 2px solid {s_color}; padding: 6px 16px; border-radius: 6px; font-size: 16px; color: {s_color}; font-weight: bold; letter-spacing: 1px;">
                {d_status}
            </span>
        </div>
        <p style="color: #64748B; font-size: 13px; margin: -10px 0 20px 0;">數據來源認證：第10組 雲端模擬監護儀 ｜ 實時狀態</p>
        <hr style="border: 0; border-top: 1px solid #1E293B; margin: 15px 0 25px 0;">
    </div>
""".format(c_style=card_style, s_color=status_color, d_status=diagnostic_status)

st.markdown(panel_html, unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    bp_alert = "text-alert" if colab_alert == "EMERGENCY_HIGH_BP" else "text-bp"
    bp_html = """
        <div style="background-color: #06090E; padding: 25px; border-radius: 8px; border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 14px; color: #64748B; font-weight: bold; letter-spacing: 1px;">NIBP (即時血壓)</div>
            <div class="vital-value {b_alert}">{sys}/{dia} <span style="font-size:16px; font-weight:normal;">mmHg</span></div>
        </div>
    """.format(b_alert=bp_alert, sys=current_sys, dia=current_dia)
    st.markdown(bp_html, unsafe_allow_html=True)

with m2:
    spo2_alert = "text-alert" if colab_alert == "EMERGENCY_LOW_SPO2" else "text-spo2"
    spo2_html = """
        <div style="background-color: #06090E; padding: 25px; border-radius: 8px; border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 14px; color: #64748B; font-weight: bold; letter-spacing: 1px;">SpO2 (即時血氧)</div>
            <div class="vital-value {s_alert}">{spo2} <span style="font-size:16px; font-weight:normal;">%</span></div>
        </div>
    """.format(s_alert=spo2_alert, spo2=current_spo2)
    st.markdown(spo2_html, unsafe_allow_html=True)

with m3:
    hr_alert = "text-alert" if (colab_alert in ["EMERGENCY_HIGH_HR", "EMERGENCY_LOW_HR"]) else "text-bpm"
    hr_html = """
        <div style="background-color: #06090E; padding: 25px; border-radius: 8px; border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 14px; color: #64748B; font-weight: bold; letter-spacing: 1px;">HR (即時心率)</div>
            <div class="vital-value {h_alert}">{hr} <span style="font-size:16px; font-weight:normal;">BPM</span></div>
        </div>
    """.format(h_alert=hr_alert, hr=current_hr)
    st.markdown(hr_html, unsafe_allow_html=True)

if not error_mode and not chart_data.empty:
    st.markdown("<br>", unsafe_allow_html=True)
    st.line_chart(chart_data.tail(30), height=280)
