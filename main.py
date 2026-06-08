import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(page_title="第10組 ICU 臨床單床監護儀 ", page_icon="🏥", layout="wide")


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
    if sheet_url == "貼上網址":
        raise ValueError("尚未設定網址")


    csv_url = sheet_url.split('/edit')[0] + '/export?format=csv'
    df = pd.read_csv(csv_url)

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
    st.sidebar.markdown("<h3 style='color: #38BDF8; margin-top:0;'>🧪 現場 Live 展示控制</h3>", unsafe_allow_html=True)
    demo_bpm = st.sidebar.slider("模擬目前心率 (BPM)", 40, 140, 72)
    demo_spo2 = st.sidebar.slider("模擬目前血氧 (%)", 85, 100, 98)

    current_sys, current_dia, current_spo2, current_hr = 120, 80, demo_spo2, demo_bpm
    colab_alert = "NORMAL"
    if demo_bpm < 50:
        colab_alert = "EMERGENCY_LOW_HR"
    elif demo_bpm > 120:
        colab_alert = "EMERGENCY_HIGH_HR"
    elif demo_spo2 < 94:
        colab_alert = "EMERGENCY_LOW_SPO2"

    chart_data = pd.DataFrame()

# --- 臨床邏輯判斷 ---
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

# --- 主畫面：單床監控大面板 ---
st.markdown(f"""
    <div class="monitor-panel {card_style}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 28px; font-weight: 800; color: #FFF; letter-spacing: 1px;">🛏️ TARGET LOCATION: BED-001</span>
            <span style="background-color: {status_color}22; border: 2px solid {status_color}; padding: 6px 16px; border-radius: 6px; font-size: 16px; color: {status_color}; font-weight: bold; letter-spacing: 1px;">
                {diagnostic_status}
            </span>
        </div>
        <p style="color: #64748B; font-size: 13px; margin: -10px 0 20px 0;">數據來源認證：第10組 雲端模擬監護儀 ｜ 實時狀態</p>
        <hr style="border: 0; border-top: 1px solid #1E293B; margin: 15px 0 25px 0;">
    </div>
""", unsafe_allow_html=True)

if error_mode:
    st.info("💡 貼心提示：目前為 Demo 模式。請確認 Google Sheet 是否已開啟『知道連結的任何人都可以檢視』共用權限！")

m1, m2, m3 = st.columns(3)

with m1:
    bp_alert = "text-alert" if colab_alert == "EMERGENCY_HIGH_BP" else "text-bp"
    st.markdown(f"""
        <div style="background-color: #06090E; padding: 25px; border-radius: 8px; border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 14px; color: #64748B; font-weight: bold; letter-spacing: 1px;">NIBP (即時血壓)</div>
            <div class="vital-value {bp_alert}">{current_sys}/{current_dia} <span style="font-size:16px; font-weight:normal;">mmHg</span></div>
            <div style="font-size: 11px; color: #64748B; margin-top: 10px;">收縮壓/舒張壓</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    spo2_alert = "text-alert" if colab_alert == "EMERGENCY_LOW_SPO2" else "text-spo2"
    st.markdown(f"""
        <div style="background-color: #06090E; padding: 25px; border-radius: 8px; border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 14px; color: #64748B; font-weight: bold; letter-spacing: 1px;">SpO2 (即時血氧)</div>
            <div class="vital-value {spo2_alert}">{current_spo2} <span style="font-size:16px; font-weight:normal;">%</span></div>
            <div style="font-size: 11px; color: #64748B; margin-top: 10px;">正常範圍: &ge; 94 %</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    hr_alert = "text-alert" if (colab_alert in ["EMERGENCY_HIGH_HR", "EMERGENCY_LOW_HR"]) else "text-bpm"
    st.markdown(f"""
        <div style="background-color: #06090E; padding: 25px; border-radius: 8px; border: 1px solid #1E293B; text-align: center;">
            <div style="font-size: 14px; color: #64748B; font-weight: bold; letter-spacing: 1px;">HR (即時心率)</div>
            <div class="vital-value {hr_alert}">{current_hr} <span style="font-size:16px; font-weight:normal;">BPM</span></div>
            <div style="font-size: 11px; color: #64748B; margin-top: 10px;">正常範圍: 50 ~ 120 BPM</div>
        </div>
    """, unsafe_allow_html=True)

if not error_mode and not chart_data.empty:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #38BDF8; font-size: 18px; font-weight: 700;'>📈 多生理徵象連續採樣趨勢 (Clinical Waveforms)</h3>", unsafe_allow_html=True)
    st.line_chart(chart_data.tail(30), height=280)
