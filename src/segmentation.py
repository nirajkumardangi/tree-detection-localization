import cv2
import numpy as np


class TreeSegmenter:

    def __init__(self):
        import sys
        from pathlib import Path
        import torch

        # Add models/sam2_repo to sys.path so we can import sam2
        ROOT_DIR = Path(__file__).resolve().parent.parent
        sam2_path = str(ROOT_DIR / "models" / "sam2_repo")
        if sam2_path not in sys.path:
            sys.path.append(sam2_path)

        from src.config import USE_SAM2, SAM2_CHECKPOINT, SAM2_CONFIG

        self.use_sam2 = USE_SAM2
        self.predictor = None

        if self.use_sam2:
            try:
                from sam2.build_sam import build_sam2
                from sam2.sam2_image_predictor import SAM2ImagePredictor

                # Determine device
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                
                # Resolve paths
                checkpoint_path = str(ROOT_DIR / SAM2_CHECKPOINT)
                config_path = SAM2_CONFIG
                
                # Load the model
                model = build_sam2(config_path, checkpoint_path, device=self.device)
                self.predictor = SAM2ImagePredictor(model)
            except Exception as e:
                print(f"Warning: Failed to load SAM2 model, falling back to bounding box masks. Error: {e}")
                self.use_sam2 = False

    def generate_mask(
        self,
        image,
        x1,
        y1,
        x2,
        y2
    ):
        if self.use_sam2 and self.predictor is not None:
            box = np.array([x1, y1, x2, y2], dtype=np.float32)
            masks, scores, logits = self.predictor.predict(
                box=box,
                multimask_output=False
            )
            # convert boolean mask to uint8 with values 0 and 1
            binary_mask = masks[0].astype(np.uint8)
            return binary_mask
        else:
            # Fallback: create a bounding box mask (filled rectangle with 1s)
            h, w = image.shape[:2]
            mask = np.zeros((h, w), dtype=np.uint8)
            mask[y1:y2, x1:x2] = 1
            return mask

    def segment(
        self,
        image_path,
        detection_result
    ):

        masks = []

        if not detection_result["tree_detected"]:
            return {
                "mask_available": False,
                "tree_area_pixels": 0,
                "image_total_pixels": 0,
                "tree_area_percentage": 0,
                "masks": []
            }

        image = cv2.imread(image_path)

        height, width = image.shape[:2]

        image_pixels = height * width

        total_tree_pixels = 0

        # Set the image to the predictor once if using SAM2
        if self.use_sam2 and self.predictor is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.predictor.set_image(image_rgb)

        for detection in detection_result["detections"]:

            box = detection["bounding_box"]

            x1 = box["x_min"]
            y1 = box["y_min"]
            x2 = box["x_max"]
            y2 = box["y_max"]

            # SAM2 prediction here

            mask = self.generate_mask(
                image,
                x1,
                y1,
                x2,
                y2
            )

            tree_pixels = int(mask.sum())

            total_tree_pixels += tree_pixels

            masks.append(mask)

        tree_percentage = (
            total_tree_pixels / image_pixels
        ) * 100

        return {
            "mask_available": True,
            "tree_area_pixels": total_tree_pixels,
            "image_total_pixels": image_pixels,
            "tree_area_percentage": round(
                tree_percentage,
                2
            ),
            "masks": masks
        }