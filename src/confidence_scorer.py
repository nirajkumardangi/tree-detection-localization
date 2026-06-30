from src.config import (
    PASS_CONFIDENCE,
    REVIEW_CONFIDENCE,
    MIN_TREE_AREA_PERCENTAGE,
)


class ConfidenceScorer:
    """
    A class to score the confidence of tree detections based on various criteria.
    """

    def score(
        self,
        quality,
        detection,
        segmentation
    ):

        flags = []

        # Check if a tree was detected if not detected, return REJECT immediately
        if not detection["tree_detected"]:

            return {
                "validation_status": "REJECT",
                "flags": ["no_tree_detected"]
            }

        # Check highest confidence among detections
        max_confidence = max(
            d["confidence"]
            for d in detection["detections"]
        )

        # Check tree area percentage against minimum threshold
        if segmentation[
            "tree_area_percentage"
        ] < MIN_TREE_AREA_PERCENTAGE:

            flags.append("tree_too_small")

        if quality["overall_quality"] == "FAIL":

            flags.append("poor_image_quality")

        if detection["tree_count"] > 1:

            flags.append("multiple_trees_detected")

        # PASS

        if (
            max_confidence >= PASS_CONFIDENCE
            and quality["overall_quality"] == "PASS"
            and len(flags) == 0
        ):

            return {
                "validation_status": "PASS",
                "confidence": max_confidence,
                "flags": []
            }

        # REVIEW

        if max_confidence >= REVIEW_CONFIDENCE:

            return {
                "validation_status": "REVIEW",
                "confidence": max_confidence,
                "flags": flags
            }

        # REJECT

        return {
            "validation_status": "REJECT",
            "confidence": max_confidence,
            "flags": flags
        }
