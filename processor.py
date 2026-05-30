import cv2
import numpy as np

class TrafficAnalyzer:

    def __init__(self):
        pass

    def process_frame(
        self,
        frame,
        conf,
        speed_limit,
        lane_count,
        scale
    ):

        detections = []

        h, w = frame.shape[:2]

        cv2.putText(
            frame,
            "Traffic Sentinel AI",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        return frame, detections

    def generate_summary(
        self,
        vehicles,
        violations,
        avg_speed,
        density
    ):

        return f"""
        Traffic analysis detected {vehicles} vehicles.

        Average speed was {avg_speed:.1f} km/h.

        {violations} violations were detected.

        Traffic density was classified as {density}.
        """
