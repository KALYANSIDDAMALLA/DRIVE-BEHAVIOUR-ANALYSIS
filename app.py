import streamlit as st
import cv2
import tempfile
from processor import TrafficAnalyzer

st.set_page_config(page_title="Traffic Sentinel AI", layout="wide")

# Persistent Analyzer Initialization
@st.cache_resource
def get_analyzer():
    return TrafficAnalyzer()

analyzer = get_analyzer()

st.title("🧠 AI Surveillance Engine")

# Configuration Sidebar
with st.sidebar:
    st.header("Calibration")
    conf = st.slider("Confidence", 0.1, 1.0, 0.35)
    speed_limit = st.slider("Speed Limit", 30, 100, 50)

# Main Processing Loop
uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    frame_placeholder = st.empty()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        processed_frame, _ = analyzer.process_frame(frame, conf, speed_limit, 6, 35)
        frame_placeholder.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), channels="RGB")
        
    cap.release()
