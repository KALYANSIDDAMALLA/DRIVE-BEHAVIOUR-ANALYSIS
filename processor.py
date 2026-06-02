import pandas as pd


class TrafficAnalyzer:

    def __init__(self):
        pass

    def process_video(self, video_path, config):

        data = {
            "Vehicle ID": [1, 2, 3],
            "Risk Level": ["LOW", "MEDIUM", "HIGH"],
            "Average Speed": [45, 62, 88],
            "Traffic Density": ["LOW", "MEDIUM", "HIGH"]
        }

        return pd.DataFrame(data)

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
