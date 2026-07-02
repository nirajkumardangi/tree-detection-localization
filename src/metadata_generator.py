import json
import cv2
from pathlib import Path

from src.config import (
    METADATA_OUTPUT_DIR,
    MASK_OUTPUT_DIR
)

# MetadataGenerator is responsible for generating metadata for the processed images.
class MetadataGenerator:
    
    def generate(
        self,
        image_path,
        quality,
        detection,
        segmentation,
        score,
        annotated_image
    ):

        # Generate mask files if available
        
        mask_files = []
        if segmentation["mask_available"]:
            image_stem = Path(image_path).stem
            for idx, mask in enumerate(segmentation["masks"]):
                mask_filename = f"{image_stem}_mask_{idx+1}.png"
                mask_path = f"{MASK_OUTPUT_DIR}/{mask_filename}"
                cv2.imwrite(mask_path, mask * 255)
                mask_files.append(mask_path)


        # Create segmentation metadata
        
        seg_meta = {
            "mask_available": segmentation["mask_available"],
            "tree_area_pixels": segmentation["tree_area_pixels"],
            "image_total_pixels": segmentation["image_total_pixels"],
            "tree_area_percentage": segmentation["tree_area_percentage"],
            "mask_files": mask_files,
            "mask_file": mask_files[0] if mask_files else None
        }

        # Create the metadata dictionary
        
        metadata = {
            "image_name":
                Path(image_path).name,

            "quality":
                quality,

            "detection":
                detection,

            "segmentation":
                seg_meta,

            "score":
                score,

            "annotated_image":
                annotated_image
        }

        # Save metadata to a JSON file

        filename = (
            Path(image_path).stem
            + ".json"
        )
        
        # Ensure the metadata output directory exists

        output_path = (
            f"{METADATA_OUTPUT_DIR}/"
            f"{filename}"
        )


        with open(
            output_path,
            "w"
        ) as f:

            # Write the metadata dictionary to the JSON file with indentation for readability
            json.dump(
                metadata,
                f,
                indent=4
            )

        return output_path