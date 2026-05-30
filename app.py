import streamlit as st
import cv2
import tempfile
import time
from processor import TrafficAnalyzer

st.set_page_config(page_title="Traffic Sentinel Pro", layout="wide")

# Persistent Initialization
@st.cache_resource
def get_analyzer():
    return TrafficAnalyzer()

analyzer = get_analyzer()

# UI Layout
st.title("🛡️ Traffic Sentinel Pro")
col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("Configuration")
    conf = st.slider("Detection Confidence", 0.1, 1.0, 0.45)
    speed_limit = st.slider("Speed Limit (km/h)", 30, 120, 60)
    st.divider()
    status_indicator = st.empty()

# Processing Logic
uploaded_file = st.file_uploader("Upload Traffic Feed", type=["mp4"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    frame_placeholder = col1.empty()
    fps_display = st.sidebar.empty()
    
    prev_time = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            st.success("Analysis Complete.")
            break
            
        # Calculation for FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Core Processing
        # Ensure your processor returns a clean, annotated frame
        processed_frame, detections = analyzer.process_frame(
            frame, conf, speed_limit, 6, 35
        )
        
        # Optimize frame for web display (resize if necessary)
        display_frame = cv2.resize(processed_frame, (800, 450))
        
        frame_placeholder.image(
            cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB), 
            channels="RGB", 
            use_container_width=True
        )
        
        fps_display.metric("Processing FPS", f"{fps:.2f}")
        status_indicator.info(f"Objects Detected: {len(detections)}")

    cap.release()
