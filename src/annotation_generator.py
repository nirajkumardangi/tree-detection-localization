import cv2
from pathlib import Path

from src.config import (
    ANNOTATED_OUTPUT_DIR
)


class AnnotationGenerator:

    def generate(
        self,
        image_path,
        detection,
        segmentation,
        score
    ):

        image = cv2.imread(image_path)

        # Draw green mask for detected tree areas if available

        if segmentation["mask_available"]:

            for mask in segmentation["masks"]:

                overlay = image.copy()

                overlay[mask > 0] = (
                    0,
                    255,
                    0
                )

                image = cv2.addWeighted(
                    overlay,
                    0.3,
                    image,
                    0.7,
                    0
                )

        # Draw green bounding boxes and confidence scores for each detected tree

        for detection_item in detection[
            "detections"
        ]:

            box = detection_item[
                "bounding_box"
            ]

            confidence = detection_item[
                "confidence"
            ]

            cv2.rectangle(
                image,
                (
                    box["x_min"],
                    box["y_min"]
                ),
                (
                    box["x_max"],
                    box["y_max"]
                ),
                (0, 255, 0),
                2
            )

            cv2.putText(
                image,
                f"Tree: {confidence:.2f}",
                (
                    box["x_min"],
                    box["y_min"] - 10
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # Status Banner

        cv2.putText(
            image,
            score["validation_status"],
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        filename = (
            Path(image_path).stem
            + "_annotated.jpg"
        )

        output_path = (
            f"{ANNOTATED_OUTPUT_DIR}/"
            f"{filename}"
        )

        cv2.imwrite(
            output_path,
            image
        )

        return output_path