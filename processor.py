import cv2
import numpy as np
from ultralytics import YOLO
import math

class TrafficAnalyzer:
    def __init__(self, model_path="yolov8n.pt", device="cpu"):
        self.model = YOLO(model_path).to(device)
        self.class_labels = {2: "Car", 3: "Bike", 5: "Bus", 7: "Truck"}

    def process_frame(self, frame, conf, speed_limit, accel_thresh, weaving_thresh):
        """Analyzes a single frame for behavioral metrics."""
        results = self.model.track(frame, persist=True, conf=conf, classes=[2, 3, 5, 7], verbose=False)
        annotated_frame = frame.copy()
        metrics = []

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            
            for box, tid in zip(boxes, ids):
                x1, y1, x2, y2 = map(int, box)
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                
                # Logic: Annotate and collect behavioral data
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                metrics.append({"id": tid, "center": (cx, cy)})
                
        return annotated_frame, metrics
