from ultralytics import YOLO

from src.config import (
    MODEL_PATH,
    MIN_DETECTION_CONFIDENCE,
    MAX_DETECTIONS,
)


class TreeDetector:
    def __init__(self):
        # Load the YOLO model for tree detection
        self.model = YOLO(MODEL_PATH)

    def detect(self, image_path: str) -> dict:
        """
        Run tree detection on image.
        """

        results = self.model.predict(
            source=image_path,
            conf=MIN_DETECTION_CONFIDENCE,
            max_det=MAX_DETECTIONS,
            verbose=False
        )

        detections = []

        detection_id = 1

        for result in results:

            boxes = result.boxes

            if boxes is None:
                continue

            for box in boxes:

                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append(
                    {
                        "detection_id": detection_id,
                        "class_label": "tree",
                        "confidence": round(confidence, 4),
                        "bounding_box": {
                            "x_min": int(x1),
                            "y_min": int(y1),
                            "x_max": int(x2),
                            "y_max": int(y2),
                        },
                    }
                )

                detection_id += 1

        return {
            "tree_detected": len(detections) > 0,
            "tree_count": len(detections),
            "detections": detections,
        }
        