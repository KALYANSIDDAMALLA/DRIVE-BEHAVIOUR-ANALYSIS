import streamlit as st
import tempfile
import pandas as pd
from processor import TrafficAnalyzer

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="GuardianAI Fleet Auditor",
    page_icon="🚦",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
}

.subtitle {
    font-size: 18px;
    color: #cbd5e1;
}

.metric-box {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #38bdf8;
}

.metric-label {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class='big-title'>
        🚦 GuardianAI Fleet Auditor
    </div>

    <div class='subtitle'>
        Enterprise-grade Driver Behaviour Analysis Platform
    </div>

    <br>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Analysis Settings")

confidence = st.sidebar.slider(
    "Detection Confidence",
    0.1,
    1.0,
    0.5
)

speed_limit = st.sidebar.number_input(
    "Speed Limit (km/h)",
    20,
    200,
    70
)

lane_count = st.sidebar.number_input(
    "Lane Count",
    1,
    10,
    4
)

# --------------------------------------------------
# METRICS ROW
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Vehicles", "0")

with c2:
    st.metric("Violations", "0")

with c3:
    st.metric("Avg Speed", "0 km/h")

with c4:
    st.metric("Density", "LOW")

st.divider()

# --------------------------------------------------
# UPLOAD SECTION
# --------------------------------------------------

left, right = st.columns([1, 1])

with left:

    st.subheader("📹 Upload Traffic Footage")

    uploaded_file = st.file_uploader(
        "Choose MP4 video",
        type=["mp4"]
    )

    run_analysis = st.button(
        "🚀 Run Analysis",
        use_container_width=True
    )

with right:

    st.subheader("ℹ️ Features")

    st.info("""
    ✔ Vehicle Detection

    ✔ Speed Monitoring

    ✔ Traffic Density Analysis

    ✔ Risk Assessment

    ✔ AI Generated Reports

    ✔ Driver Behaviour Insights
    """)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if uploaded_file and run_analysis:

    analyzer = TrafficAnalyzer()

    with st.spinner("Processing traffic footage..."):

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        )

        temp_file.write(uploaded_file.read())
        temp_file.close()

        try:

            if hasattr(analyzer, "process_video"):

                results = analyzer.process_video(
                    temp_file.name,
                    {
                        "confidence": confidence,
                        "speed_limit": speed_limit,
                        "lane_count": lane_count
                    }
                )

                st.success("Analysis completed")

                if isinstance(results, pd.DataFrame):

                    st.subheader("📊 Analysis Results")

                    st.dataframe(
                        results,
                        use_container_width=True
                    )

                    st.metric(
                        "Vehicles Analysed",
                        len(results)
                    )

                else:

                    st.write(results)

            else:

                st.warning(
                    "process_video() not found in processor.py"
                )

        except Exception as e:

            st.error(f"Analysis failed: {e}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "GuardianAI Fleet Auditor • Powered by Streamlit & Computer Vision"
)
