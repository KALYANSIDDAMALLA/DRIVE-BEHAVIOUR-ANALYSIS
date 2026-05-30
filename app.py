import cv2


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

        cv2.putText(
            frame,
            "Traffic Sentinel AI",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
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
        Total vehicles detected: {vehicles}

        Average speed: {avg_speed} km/h

        Violations detected: {violations}

        Traffic density: {density}
        """
