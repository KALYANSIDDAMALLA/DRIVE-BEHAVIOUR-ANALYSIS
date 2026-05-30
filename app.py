import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict, deque
import math
import torch
import tempfile
import os
import pandas as pd

# --- Page Setup & Theme Styling ---
st.set_page_config(
    page_title="Behavioral AI Surveillance Engine",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0f111a; color: #ffffff; }
    h1 { color: #ff3366; font-family: 'Arial Black', sans-serif; }
    .stAlert { background-color: #1a1c24; border: 1px solid #ff3366; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Deep Learning Driver Behavior Analysis & Aggressive Driving Detection")
st.subheader("MSc Thesis Deployment Sandbox — Advanced Telemetry Behavioral Profiling")
st.markdown("---")

# --- Sidebar Parameter Tuning Panel ---
st.sidebar.header("⚙️ Behavioral Calibration Thresholds")
speed_limit = st.sidebar.slider("Segment Speed Limit (km/h)", 30, 100, 50, 5)
acceleration_threshold = st.sidebar.slider("Aggressive Acceleration Delta (km/h/frame)", 3, 15, 6, 1)
weaving_threshold = st.sidebar.slider("Lateral Weaving Variance (Pixels)", 10, 100, 35, 5)

confidence_threshold = st.sidebar.slider("YOLO Detection Confidence", 0.10, 1.00, 0.35, 0.05)
max_frames_to_run = st.sidebar.number_input("Maximum Frames to Process", min_value=50, max_value=2000, value=300, step=50)

device = "mps" if torch.backends.mps.is_available() else "cpu"
st.sidebar.success(f"🚀 Execution Backend: {device.upper()}")

@st.cache_resource
def load_yolo_model():
    return YOLO("yolov8n.pt")

model = load_yolo_model().to(device)

uploaded_video = st.file_uploader("📂 Upload Traffic Stream Footage Asset", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_video.read())
    cap = cv2.VideoCapture(tfile.name)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🎥 Live Behavioral Vision Stream")
        frame_placeholder = st.empty()
    with col2:
        st.markdown("### 📊 Active Behavioral HUD")
        metric_tracked = st.metric(label="Total Monitored Drivers", value=0)
        metric_aggressive = st.metric(label="Aggressive Drivers Flagged", value=0)
        
        st.markdown("🚨 **Real-Time Driver Infraction Manifest:**")
        infraction_area = st.empty()
        infraction_log = ""

    # Processing Buffers
    vehicle_history = defaultdict(lambda: deque(maxlen=30))
    speed_history = defaultdict(lambda: deque(maxlen=5))
    counted_ids = set()
    aggressive_ids = set()
    class_labels_map = {2: "Car", 3: "Bike", 5: "Bus", 7: "Truck"}
    
    # Behavioral Analytics Registries
    driver_profiles = defaultdict(lambda: {
        "type": "Unknown", "speeds": [], "x_coords": [], "infractions": set()
    })

    progress_bar = st.progress(0.0)
    frame_idx = 0
    
    while cap.isOpened() and frame_idx < max_frames_to_run:
        ret, frame = cap.read()
        if not ret: break
            
        frame_idx += 1
        progress_bar.progress(float(frame_idx / max_frames_to_run))
        frame = cv2.resize(frame, (1280, 720))
        
        results = model.track(frame, persist=True, conf=confidence_threshold, classes=[2,3,5,7], device=device, verbose=False)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)
            
            for box, track_id, cls_id in zip(boxes, ids, classes):
                x1, y1, x2, y2 = map(int, box)
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                
                vehicle_history[track_id].append((cx, cy))
                v_label = class_labels_map.get(cls_id, "Car")
                
                if track_id not in counted_ids:
                    counted_ids.add(track_id)
                    driver_profiles[track_id]["type"] = v_label
                
                driver_profiles[track_id]["x_coords"].append(cx)
                
                # 1. Speed & Rapid Acceleration Calculations
                speed = 0
                acceleration = 0
                if len(vehicle_history[track_id]) >= 2:
                    x_prev, y_prev = vehicle_history[track_id][-2]
                    distance = math.sqrt((cx - x_prev)**2 + (cy - y_prev)**2)
                    speed = int(distance * 1.8)
                    
                    if len(driver_profiles[track_id]["speeds"]) > 0:
                        acceleration = speed - driver_profiles[track_id]["speeds"][-1]
                        
                    speed_history[track_id].append(speed)
                    speed = int(np.mean(speed_history[track_id]))
                    driver_profiles[track_id]["speeds"].append(speed)

                # --- Behavioral Threat Analysis Core Heuristics ---
                is_aggressive = False
                
                # Check A: Speeding Infraction
                if speed > speed_limit:
                    driver_profiles[track_id]["infractions"].add("Speeding")
                
                # Check B: Aggressive Drag-Race Acceleration
                if acceleration >= acceleration_threshold:
                    driver_profiles[track_id]["infractions"].add("Reckless Acceleration")
                    
                # Check C: Lane Weaving / Erratic Swerving Swings
                if len(driver_profiles[track_id]["x_coords"]) >= 15:
                    recent_x = driver_profiles[track_id]["x_coords"][-15:]
                    x_variance = np.std(recent_x)
                    if x_variance > weaving_threshold:
                        driver_profiles[track_id]["infractions"].add("Erratic Weaving")

                if len(driver_profiles[track_id]["infractions"]) > 0:
                    is_aggressive = True
                    if track_id not in aggressive_ids:
                        aggressive_ids.add(track_id)
                        new_infractions = ", ".join(driver_profiles[track_id]["infractions"])
                        infraction_log = f"🚨 Vehicle ID {track_id} ({v_label}) Flagged: {new_infractions}\n" + infraction_log

                # Visual Graphic Overlays
                box_color = (0, 0, 255) if is_aggressive else (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
                
                status_text = "AGGRESSIVE" if is_aggressive else "NORMATIVE"
                cv2.putText(frame, f"ID:{track_id} | {status_text} | {speed} km/h", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB")
        
        metric_tracked.metric(label="Total Monitored Drivers", value=len(counted_ids))
        metric_aggressive.metric(label="Aggressive Drivers Flagged", value=len(aggressive_ids))
        infraction_area.text(infraction_log)
        
    cap.release()
    st.success("🏁 Behavioral analysis run execution complete!")
    
    # ----------------------------------------------------------------------------------
    # POST-RUN ANALYTICS SUMMARY LAYER
    # ----------------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("## 📊 Run Analytics Summary (Behavioral Profiling)")
    
    if len(counted_ids) > 0:
        summary_rows = []
        for tid in counted_ids:
            profile = driver_profiles[tid]
            max_spd = max(profile["speeds"]) if profile["speeds"] else 0
            avg_spd = int(np.mean(profile["speeds"])) if profile["speeds"] else 0
            infractions_list = list(profile["infractions"])
            risk_label = "🚨 HIGH RISK (Aggressive)" if infractions_list else "✅ LOW RISK (Safe)"
            
            summary_rows.append({
                "Driver Track ID": tid,
                "Vehicle Class": profile["type"],
                "Average Speed (km/h)": avg_spd,
                "Peak Speed (km/h)": max_spd,
                "Detected Infractions": ", ".join(infractions_list) if infractions_list else "None",
                "Behavioral Risk Classification": risk_label
            })
            
        df = pd.DataFrame(summary_rows)
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric("Aggressive Risk Ratio", f"{round((len(aggressive_ids)/len(counted_ids))*100, 1)}%")
        with sc2:
            st.metric("Speeding Violators", len(df[df["Detected Infractions"].str.contains("Speeding")]))
        with sc3:
            st.metric("Reckless Weaving Incidents", len(df[df["Detected Infractions"].str.contains("Weaving")]))
            
        st.markdown("### 📝 Extracted Driver Profile Analytics Log")
        st.dataframe(df, use_container_width=True)
        
        # ----------------------------------------------------------------------------------
        # ACADEMIC DATA DESCRIPTIONS (FOR ACADEMIC DOCUMENTATION)
        # ----------------------------------------------------------------------------------
        st.markdown("---")
        st.markdown("## 📖 Academic System Data Descriptions")
        st.markdown("""
        This data dictionary breaks down the behavioral variables captured by the vision pipeline, matching the standards required for your MSc thesis methodology section.
        """)
        
        data_description_dict = {
            "Data Field Name": [
                "Driver Track ID", 
                "Vehicle Class", 
                "Average Speed (km/h)", 
                "Peak Speed (km/h)", 
                "Detected Infractions", 
                "Behavioral Risk Classification"
            ],
            "Type / Structural Format": [
                "Integer (Discrete Keys)", 
                "Categorical (String Nominal)", 
                "Continuous Float (Aggregated)", 
                "Continuous Float (Scalar Extreme)", 
                "String List / Text Manifest", 
                "Binary String Nominal Identifier"
            ],
            "Mathematical Extraction Heuristic / Description": [
                "Unique primary index assigned by the ByteTrack linear Hungarian assignment matrix to preserve structural continuity.",
                "Vehicle category translated from target tensor index maps into standardized classes (Car, Bike, Bus, Truck).",
                "The temporal mean of velocity calculations based on Euclidean frame distance vectors: $Distance = \\sqrt{\\Delta x^2 + \\Delta y^2}$.",
                "The maximum single scalar velocity computation indexed inside the tracking timeline array for a specific vehicle object.",
                "Flag log triggered by conditional threshold checks monitoring speed violations ($Speed > Speed_{limit}$) or lateral coordinate standard deviation ($Std(\\mathbf{X}_{recent}) > Weaving_{threshold}$).",
                "Risk label applied to the instance. Evaluated as HIGH RISK if the tracked entity violates one or more behavioral threshold matrices."
            ]
        }
        st.table(pd.DataFrame(data_description_dict))
        
    else:
        st.warning("No tracking nodes were logged. Please provide an active video feed path containing traffic stream instances.")
        
    try: os.unlink(tfile.name)
    except: pass
