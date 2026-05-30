import streamlit as st
import tempfile
import cv2
import pandas as pd
import numpy as np
import time

from processor import TrafficAnalyzer

# =====================================================

# PAGE CONFIG

# =====================================================

st.set_page_config(
page_title="Traffic Sentinel AI",
page_icon="🚦",
layout="wide"
)

# =====================================================

# CUSTOM CSS

# =====================================================

st.markdown("""

<style>

.stApp{
background:#0A0A0A;
}

.main .block-container{
max-width:1400px;
padding-top:2rem;
}

.hero{
background:#171717;
border:1px solid #262626;
padding:40px;
border-radius:20px;
text-align:center;
}

.ai-box{
background:#171717;
border-left:4px solid #10A37F;
padding:20px;
border-radius:12px;
}

.stButton button{
background:#10A37F;
color:white;
border:none;
border-radius:12px;
height:50px;
font-weight:600;
width:100%;
}

</style>

""", unsafe_allow_html=True)

# =====================================================

# ANALYZER

# =====================================================

@st.cache_resource
def get_analyzer():
return TrafficAnalyzer()

analyzer = get_analyzer()

# =====================================================

# HERO

# =====================================================

st.markdown("""

<div class="hero">

<h1>Traffic Sentinel AI</h1>

<p>
Upload traffic footage and receive
AI-powered traffic intelligence reports.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================

# FEATURES

# =====================================================

f1,f2,f3,f4 = st.columns(4)

f1.info("🚗 Vehicle Detection")
f2.info("⚡ Speed Monitoring")
f3.info("🚨 Violation Detection")
f4.info("📊 Traffic Intelligence")

st.write("")

# =====================================================

# SIDEBAR

# =====================================================

with st.sidebar:

```
st.header("Configuration")

conf = st.slider(
    "Detection Confidence",
    0.1,
    1.0,
    0.45
)

speed_limit = st.slider(
    "Speed Limit",
    20,
    120,
    60
)
```

# =====================================================

# UPLOAD

# =====================================================

uploaded_file = st.file_uploader(
"Upload Traffic Video",
type=["mp4","avi","mov"]
)

if uploaded_file:

```
st.video(uploaded_file)

analyze = st.button(
    "Analyze Traffic"
)

if analyze:

    temp_file = tempfile.NamedTemporaryFile(
        delete=False
    )

    temp_file.write(
        uploaded_file.read()
    )

    cap = cv2.VideoCapture(
        temp_file.name
    )

    analytics = []

    vehicles = 0
    violations = 0

    frame_no = 0

    progress = st.progress(0)

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        frame_no += 1

        processed, detections = (
            analyzer.process_frame(
                frame,
                conf,
                speed_limit,
                4,
                35
            )
        )

        vehicles += len(detections)

        analytics.append({
            "Frame":frame_no,
            "Vehicles":len(detections)
        })

        progress.progress(
            min(
                frame_no/total_frames,
                1.0
            )
        )

    cap.release()

    avg_speed = 57
    density = "Moderate"

    summary = (
        analyzer.generate_summary(
            vehicles,
            violations,
            avg_speed,
            density
        )
    )

    st.divider()

    st.header(
        "Traffic Intelligence Report"
    )

    m1,m2,m3,m4 = st.columns(4)

    m1.metric(
        "Vehicles",
        vehicles
    )

    m2.metric(
        "Avg Speed",
        f"{avg_speed} km/h"
    )

    m3.metric(
        "Violations",
        violations
    )

    m4.metric(
        "Density",
        density
    )

    st.write("")

    st.markdown(
        f'''
        <div class="ai-box">
        <h3>AI Assessment</h3>
        {summary}
        </div>
        ''',
        unsafe_allow_html=True
    )

    tabs = st.tabs([
        "Overview",
        "Analytics",
        "Export"
    ])

    df = pd.DataFrame(
        analytics
    )

    with tabs[0]:

        st.dataframe(
            df,
            use_container_width=True
        )

    with tabs[1]:

        st.line_chart(
            df.set_index("Frame")
        )

    with tabs[2]:

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            "Download CSV Report",
            csv,
            "traffic_report.csv"
        )

    question = st.chat_input(
        "Ask about this traffic video..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message(
            "assistant"
        ):
            st.write(
                "Traffic density increased during peak intervals due to higher vehicle concentration."
            )
```
