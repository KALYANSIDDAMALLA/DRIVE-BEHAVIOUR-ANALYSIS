import streamlit as st
import cv2
import tempfile
import time
from processor import TrafficAnalyzer

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Traffic Sentinel Pro",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 100%
    );
    color: white;
}

h1, h2, h3 {
    color: #f8fafc;
}

.metric-card {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
    text-align: center;
}

.upload-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    height: 3rem;
    width: 100%;
}

.stButton button:hover {
    background-color: #1d4ed8;
}

footer {
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- ANALYZER ---------------- #
@st.cache_resource
def get_analyzer():
    return TrafficAnalyzer()

analyzer = get_analyzer()

# ---------------- HEADER ---------------- #
st.markdown("""
<h1 style='text-align:center'>
🛡️ Traffic Sentinel Pro
</h1>

<p style='text-align:center;color:#cbd5e1'>
AI-Powered Traffic Monitoring, Vehicle Detection &
Speed Violation Analysis
</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.header("⚙️ Configuration")

    conf = st.slider(
        "Detection Confidence",
        0.1,
        1.0,
        0.45,
        0.05
    )

    speed_limit = st.slider(
        "Speed Limit (km/h)",
        30,
        120,
        60
    )

    st.markdown("---")

    st.info(
        f"""
        Confidence: {conf}

        Speed Limit: {speed_limit} km/h
        """
    )

# ---------------- MAIN LAYOUT ---------------- #
left, right = st.columns([3,1])

with left:
    uploaded_file = st.file_uploader(
        "📹 Upload Traffic Video",
        type=["mp4", "avi", "mov"]
    )

with right:
    st.markdown("### System Status")
    status_box = st.empty()

# ---------------- VIDEO PREVIEW ---------------- #
if uploaded_file:

    st.success("Video uploaded successfully.")

    st.video(uploaded_file)

    analyze_btn = st.button(
        "🚀 Analyze Traffic Feed"
    )

    if analyze_btn:

        # Save uploaded video
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        cap = cv2.VideoCapture(tfile.name)

        frame_placeholder = st.empty()

        metric1, metric2, metric3 = st.columns(3)

        fps_metric = metric1.empty()
        detect_metric = metric2.empty()
        violation_metric = metric3.empty()

        progress_bar = st.progress(0)

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        frame_no = 0
        violations = 0

        prev_time = time.time()

        status_box.success("🟢 Processing Started")

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            frame_no += 1

            progress = min(
                frame_no / total_frames,
                1.0
            )

            progress_bar.progress(progress)

            curr_time = time.time()

            fps = 1 / max(
                (curr_time - prev_time),
                0.0001
            )

            prev_time = curr_time

            processed_frame, detections = (
                analyzer.process_frame(
                    frame,
                    conf,
                    speed_limit,
                    6,
                    35
                )
            )

            # Example violation count
            for d in detections:
                if isinstance(d, dict):
                    if d.get("speed", 0) > speed_limit:
                        violations += 1

            display_frame = cv2.resize(
                processed_frame,
                (1000, 550)
            )

            frame_placeholder.image(
                cv2.cvtColor(
                    display_frame,
                    cv2.COLOR_BGR2RGB
                ),
                use_container_width=True
            )

            fps_metric.metric(
                "⚡ FPS",
                f"{fps:.2f}"
            )

            detect_metric.metric(
                "🚗 Vehicles",
                len(detections)
            )

            violation_metric.metric(
                "🚨 Violations",
                violations
            )

        cap.release()

        progress_bar.progress(1.0)

        status_box.success(
            "✅ Analysis Completed Successfully"
        )

        st.balloons()

# ---------------- FOOTER ---------------- #
st.markdown("""
<hr>

<div style='text-align:center;
color:#94a3b8'>
Traffic Sentinel Pro © 2026
<br>
AI-Powered Intelligent Traffic Surveillance System
</div>
""", unsafe_allow_html=True)
