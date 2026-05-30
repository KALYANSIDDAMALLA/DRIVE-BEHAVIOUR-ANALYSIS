import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from fpdf import FPDF
from collections import defaultdict, deque

class TrafficAnalyzer:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
    
    def process_video(self, video_path, thresholds):
        cap = cv2.VideoCapture(video_path)
        counted_ids = set()
        driver_profiles = defaultdict(lambda: {"speeds": [], "infractions": set()})
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            results = self.model.track(frame, persist=True, verbose=False)
            if results[0].boxes.id is not None:
                for track_id in results[0].boxes.id.int().cpu().numpy():
                    counted_ids.add(track_id)
                    # Simulated speed calculation for demonstration
                    speed = np.random.randint(20, 100) 
                    driver_profiles[track_id]["speeds"].append(speed)
                    if speed > thresholds['speed_limit']:
                        driver_profiles[track_id]["infractions"].add("Speeding")
        
        cap.release()
        
        data = []
        for tid in counted_ids:
            data.append({
                "Driver Track ID": tid,
                "Average Speed (km/h)": int(np.mean(driver_profiles[tid]["speeds"])),
                "Detected Infractions": ", ".join(driver_profiles[tid]["infractions"]) or "None",
                "Risk": "HIGH" if driver_profiles[tid]["infractions"] else "LOW"
            })
        return pd.DataFrame(data)

    def generate_pdf(self, df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, "Driver Behavior Analysis Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        for _, row in df.iterrows():
            txt = f"Driver {row['Driver Track ID']} | Risk: {row['Risk']} | Speed: {row['Average Speed (km/h)']} km/h"
            pdf.cell(190, 10, txt=txt, ln=True)
        return pdf.output(dest='S')
