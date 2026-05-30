import streamlit as st
import pandas as pd

# ======================================================

# PAGE CONFIG

# ======================================================

st.set_page_config(
page_title="Traffic Sentinel AI",
page_icon="🚦",
layout="wide"
)

# ======================================================

# MODERN CSS

# ======================================================

st.markdown("""

<style>

.stApp{
    background:#0A0A0A;
}

.main .block-container{
    max-width:1400px;
    padding-top:2rem;
}

.hero-card{
    background:#171717;
    border:1px solid #2A2A2A;
    border-radius:20px;
    padding:40px;
    text-align:center;
}

.card{
    background:#171717;
    border:1px solid #2A2A2A;
    border-radius:18px;
    padding:24px;
}

.metric-card{
    background:#171717;
    border:1px solid #2A2A2A;
    border-radius:16px;
    padding:20px;
}

.big-number{
    font-size:34px;
    font-weight:700;
    color:white;
}

.label{
    color:#A3A3A3;
    font-size:14px;
}

.ai-box{
    background:#111111;
    border-left:4px solid #10A37F;
    border-radius:12px;
    padding:20px;
}

div[data-testid="stFileUploader"]{
    background:#171717;
    padding:20px;
    border-radius:16px;
}

.stButton button{
    background:#10A37F;
    color:white;
    border:none;
    border-radius:12px;
    height:50px;
    width:100%;
    font-weight:600;
}

</style>

""", unsafe_allow_html=True)

# ======================================================

# HEADER

# ======================================================

st.markdown("""

<div class="hero-card">

<h1>Traffic Sentinel AI</h1>

<p style="color:#A3A3A3;font-size:18px;">
Upload traffic footage and receive an AI-generated
traffic intelligence report.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ======================================================

# FEATURES

# ======================================================

f1,f2,f3,f4 = st.columns(4)

with f1:
st.info("🚗 Vehicle Detection")

with f2:
st.info("⚡ Speed Monitoring")

with f3:
st.info("🚨 Violation Detection")

with f4:
st.info("📊 Traffic Intelligence")

st.write("")

# ======================================================

# UPLOAD SECTION

# ======================================================

uploaded_file = st.file_uploader(
"Upload Traffic Video",
type=["mp4","avi","mov"]
)

if uploaded_file:

```
st.success("Video uploaded successfully")

col1,col2 = st.columns([1,1])

with col1:
    st.video(uploaded_file)

with col2:

    st.markdown("""
    <div class="card">
    <h3>Video Information</h3>
    <p>Ready for AI Analysis</p>
    </div>
    """, unsafe_allow_html=True)

    analyze = st.button(
        "Analyze Traffic"
    )

if analyze:

    # ==================================
    # REPLACE THIS WITH REAL ANALYSIS
    # ==================================

    with st.spinner(
        "Traffic Sentinel AI is analyzing..."
    ):
        import time
        time.sleep(3)

    # ==================================
    # SAMPLE RESULTS
    # ==================================

    total_vehicles = 426
    avg_speed = 57
    violations = 18
    peak_density = "Moderate"

    st.divider()

    st.header("Traffic Intelligence Report")

    m1,m2,m3,m4 = st.columns(4)

    with m1:
        st.metric(
            "Vehicles",
            total_vehicles
        )

    with m2:
        st.metric(
            "Avg Speed",
            f"{avg_speed} km/h"
        )

    with m3:
        st.metric(
            "Violations",
            violations
        )

    with m4:
        st.metric(
            "Risk Level",
            peak_density
        )

    st.write("")

    left,right = st.columns([1.2,1])

    with left:

        st.markdown("""
        ### Processed Traffic Feed
        """)

        st.video(uploaded_file)

    with right:

        st.markdown("""
        <div class="ai-box">

        <h3>AI Traffic Assessment</h3>

        The uploaded traffic footage shows
        moderate traffic density.

        18 vehicles exceeded the configured
        speed threshold.

        Peak congestion occurred near the
        middle of the recording.

        Overall road conditions are classified
        as MODERATE RISK.

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    tabs = st.tabs([
        "Overview",
        "Vehicles",
        "Violations",
        "Export"
    ])

    with tabs[0]:

        overview = pd.DataFrame({
            "Metric":[
                "Traffic Score",
                "Peak Congestion",
                "Average Speed",
                "Road Condition"
            ],
            "Value":[
                "84/100",
                "01:24",
                "57 km/h",
                "Moderate"
            ]
        })

        st.dataframe(
            overview,
            use_container_width=True
        )

    with tabs[1]:

        vehicle_df = pd.DataFrame({
            "Type":[
                "Cars",
                "Bikes",
                "Trucks",
                "Buses"
            ],
            "Count":[
                302,
                89,
                24,
                11
            ]
        })

        st.bar_chart(
            vehicle_df.set_index("Type")
        )

    with tabs[2]:

        violation_df = pd.DataFrame({
            "Vehicle ID":[
                102,
                120,
                154,
                188
            ],
            "Speed":[
                84,
                81,
                79,
                77
            ]
        })

        st.dataframe(
            violation_df,
            use_container_width=True
        )

    with tabs[3]:

        csv = violation_df.to_csv(
            index=False
        )

        st.download_button(
            "Download Report",
            csv,
            "traffic_report.csv"
        )

    st.divider()

    st.subheader(
        "Ask Traffic Sentinel AI"
    )

    question = st.chat_input(
        "Ask about this traffic video..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            st.write(
                "Based on the analyzed footage, congestion increased due to higher vehicle density and reduced average speed during peak intervals."
            )
```
