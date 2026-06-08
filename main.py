import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="第10組 ICU 臨床單床監護儀", page_icon="🏥", layout="wide")

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
        <div style="text-align: right
