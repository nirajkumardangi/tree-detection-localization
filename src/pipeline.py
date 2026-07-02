from src import (
    QualityChecker,
    TreeDetector,
    TreeSegmenter,
    ConfidenceScorer,
    AnnotationGenerator,
    MetadataGenerator,
)


class TreeDetectionPipeline:

    def __init__(self):
        from pathlib import Path
        from src.config import ANNOTATED_OUTPUT_DIR, METADATA_OUTPUT_DIR, MASK_OUTPUT_DIR

        # Ensure output directories exist
        Path(ANNOTATED_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        Path(METADATA_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        Path(MASK_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        
        self.quality_checker = (
            QualityChecker()
        )

        self.detector = (
            TreeDetector()
        )

        self.segmenter = (
            TreeSegmenter()
        )

        self.scorer = (
            ConfidenceScorer()
        )

        self.annotator = (
            AnnotationGenerator()
        )

        self.metadata_generator = (
            MetadataGenerator()
        )

    def run(
        self,
        image_path
    ):

        # Step 1 : Check image quality like blurriness, brightness, contrast, etc.

        quality = (
            self.quality_checker.check(
                image_path
            )
        )

        # Step 2 : Run tree detection to identify trees in the image and get their bounding boxes and confidence scores

        detection = (
            self.detector.detect(
                image_path
            )
        )

        # Step 3 : Run tree segmentation, it generates masks for each detected tree and calculates tree area percentage

        segmentation = (
            self.segmenter.segment(
                image_path,
                detection
            )
        )

        # Step 4 : It combine previous outputs to calculate confidence scores

        score = (
            self.scorer.score(
                quality,
                detection,
                segmentation
            )
        )

        # Step 5 : Generate annotated image with bounding boxes, masks, and confidence scores

        annotated_image = (
            self.annotator.generate(
                image_path,
                detection,
                segmentation,
                score
            )
        )

        # Step 6 : Generate metadata JSON file with all relevant information

        metadata_file = (
            self.metadata_generator.generate(
                image_path,
                quality,
                detection,
                segmentation,
                score,
                annotated_image
            )
        )

        return {
            "status":
                score[
                    "validation_status"
                ],

            "annotated_image":
                annotated_image,

            "metadata":
                metadata_file
        }
        