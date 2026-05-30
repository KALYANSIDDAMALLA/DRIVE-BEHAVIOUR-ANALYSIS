import streamlit as st
import cv2
import tempfile
import time
import pandas as pd
import numpy as np
from processor import TrafficAnalyzer

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Traffic Sentinel Pro",
    page_icon="🚦",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#0B1120;
    color:white;
}

.block-container{
    padding-top:1rem;
}

.metric-card{
    background:#111827;
    border-radius:15px;
    padding:15px;
    border:1px solid #1F2937;
}

.dashboard-card{
    background:#111827;
    border-radius:15px;
    padding:20px;
    border:1px solid #1F2937;
}

h1,h2,h3{
    color:white;
}

[data-testid="stSidebar"]{
    background:#111827;
}

.stButton button{
    width:100%;
    background:#00B4D8;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton button:hover{
    background:#0096C7;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_analyzer():
    return TrafficAnalyzer()

analyzer = load_analyzer()

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<h1 style='text-align:center'>
🚦 Traffic Sentinel Pro
</h1>

<p style='text-align:center;color:#94A3B8'>
AI-Powered Traffic Monitoring & Violation Detection Platform
</p>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("⚙️ Configuration")

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

    lane_count = st.selectbox(
        "Lane Count",
        [2,3,4,5,6]
    )

    st.divider()

    st.info(
        f"""
        Confidence : {conf}

        Speed Limit : {speed_limit} km/h

        Lanes : {lane_count}
        """
    )

# =====================================================
# VIDEO UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4","avi","mov"]
)

if uploaded_file:

    st.video(uploaded_file)

    if st.button("🚀 Start Analysis"):

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())

        cap = cv2.VideoCapture(temp_file.name)

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        # ==========================================
        # DASHBOARD PLACEHOLDERS
        # ==========================================

        video_col, stats_col = st.columns([3,1])

        video_placeholder = video_col.empty()

        with stats_col:
            density_box = st.empty()
            status_box = st.empty()

        k1,k2,k3,k4,k5,k6 = st.columns(6)

        vehicle_metric = k1.empty()
        speed_metric = k2.empty()
        violation_metric = k3.empty()
        density_metric = k4.empty()
        fps_metric = k5.empty()
        max_speed_metric = k6.empty()

        progress_bar = st.progress(0)

        # ==========================================
        # DATA STORAGE
        # ==========================================

        analytics = []

        total_vehicles = 0
        violations = 0
        max_speed = 0

        frame_no = 0
        prev_time = time.time()

        # ==========================================
        # PROCESSING LOOP
        # ==========================================

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            frame_no += 1

            progress_bar.progress(
                min(frame_no/total_frames,1.0)
            )

            current_time = time.time()

            fps = 1 / max(
                current_time - prev_time,
                0.001
            )

            prev_time = current_time

            processed_frame, detections = (
                analyzer.process_frame(
                    frame,
                    conf,
                    speed_limit,
                    lane_count,
                    35
                )
            )

            vehicle_count = len(detections)

            # ----------------------------------
            # Example statistics
            # ----------------------------------

            speeds = []

            for det in detections:

                if isinstance(det, dict):

                    speed = det.get("speed",0)

                    speeds.append(speed)

                    if speed > speed_limit:
                        violations += 1

            avg_speed = (
                np.mean(speeds)
                if len(speeds)
                else 0
            )

            if len(speeds):
                max_speed = max(
                    max_speed,
                    max(speeds)
                )

            total_vehicles += vehicle_count

            # ----------------------------------
            # Traffic Density
            # ----------------------------------

            if vehicle_count < 10:
                density = "LOW"
                density_color = "🟢"

            elif vehicle_count < 25:
                density = "MEDIUM"
                density_color = "🟡"

            else:
                density = "HIGH"
                density_color = "🔴"

            # ----------------------------------
            # Store Analytics
            # ----------------------------------

            analytics.append({
                "Frame":frame_no,
                "Vehicles":vehicle_count,
                "Avg Speed":avg_speed,
                "Violations":violations
            })

            # ----------------------------------
            # Display Frame
            # ----------------------------------

            display = cv2.resize(
                processed_frame,
                (1200,650)
            )

            video_placeholder.image(
                cv2.cvtColor(
                    display,
                    cv2.COLOR_BGR2RGB
                ),
                use_container_width=True
            )

            # ----------------------------------
            # Metrics
            # ----------------------------------

            vehicle_metric.metric(
                "🚗 Vehicles",
                vehicle_count
            )

            speed_metric.metric(
                "⚡ Avg Speed",
                f"{avg_speed:.1f}"
            )

            violation_metric.metric(
                "🚨 Violations",
                violations
            )

            density_metric.metric(
                "📊 Density",
                density
            )

            fps_metric.metric(
                "💻 FPS",
                f"{fps:.1f}"
            )

            max_speed_metric.metric(
                "🏎 Max Speed",
                f"{max_speed:.1f}"
            )

            density_box.success(
                f"{density_color} Traffic Density: {density}"
            )

            status_box.info(
                f"Frame {frame_no}"
            )

        cap.release()

        # ==========================================
        # ANALYTICS SECTION
        # ==========================================

        st.divider()

        st.subheader("📈 Traffic Analytics")

        df = pd.DataFrame(analytics)

        c1,c2 = st.columns(2)

        with c1:
            st.markdown("### Vehicle Trend")
            st.line_chart(
                df.set_index("Frame")["Vehicles"]
            )

        with c2:
            st.markdown("### Average Speed Trend")
            st.line_chart(
                df.set_index("Frame")["Avg Speed"]
            )

        st.markdown("### Violation Trend")
        st.bar_chart(
            df.set_index("Frame")["Violations"]
        )

        # ==========================================
        # SUMMARY
        # ==========================================

        st.divider()

        st.subheader("📋 Analysis Summary")

        s1,s2,s3,s4 = st.columns(4)

        s1.metric(
            "Total Vehicles",
            total_vehicles
        )

        s2.metric(
            "Total Violations",
            violations
        )

        s3.metric(
            "Maximum Speed",
            f"{max_speed:.1f}"
        )

        s4.metric(
            "Frames Processed",
            frame_no
        )

        # ==========================================
        # LOG TABLE
        # ==========================================

        st.subheader("📝 Detection Log")

        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )

        # ==========================================
        # EXPORT REPORT
        # ==========================================

        csv = df.to_csv(index=False)

        st.download_button(
            "📥 Download Traffic Report",
            csv,
            "traffic_analysis_report.csv",
            "text/csv"
        )

        st.success("✅ Traffic Analysis Completed Successfully")
