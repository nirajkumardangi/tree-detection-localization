import cv2
import numpy as np
from PIL import Image
import os


class ImageQualityChecker:

    SUPPORTED_FORMATS = ["JPG", "JPEG", "PNG", "HEIC"]

    def __init__(self):
        self.MIN_WIDTH = 280
        self.MIN_HEIGHT = 200

    # Blur Detection using Variance of Laplacian
    def check_blur(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur_score = float(
            cv2.Laplacian(gray, cv2.CV_64F).var()
        )

        if blur_score < 50:
            status = "reject"
        elif blur_score < 100:
            status = "review"
        else:
            status = "acceptable"

        return blur_score, status

    # Brightness Analysis using Mean Pixel Intensity
    def check_brightness(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        brightness_value = float(np.mean(gray))

        if brightness_value < 50:
            brightness = "dark"
        elif brightness_value > 200:
            brightness = "overexposed"
        else:
            brightness = "normal"

        return brightness_value, brightness

    # Resolution Check based on Minimum Dimensions
    def check_resolution(self, image):
        height, width = image.shape[:2]

        resolution = f"{width}x{height}"

        if (
            width < self.MIN_WIDTH
            or height < self.MIN_HEIGHT
        ):
            status = "reject"
        else:
            status = "acceptable"

        return resolution, status

    # File Validation using PIL
    def validate_file(self, image_path):

        if not os.path.exists(image_path):
            return False, None

        try:
            img = Image.open(image_path)

            file_format = img.format.upper()

            if file_format not in self.SUPPORTED_FORMATS:
                return False, file_format

            img.verify()

            return True, file_format

        except Exception:
            return False, None

    # Main Quality Check Function
    def check_quality(self, image_path):

        quality_flags = []

        file_valid, file_format = self.validate_file(
            image_path
        )

        if not file_valid:
            return {
                "file_valid": False,
                "overall_quality": "FAIL",
                "quality_flags": [
                    "invalid_or_corrupt_file"
                ]
            }

        image = cv2.imread(image_path)

        if image is None:
            return {
                "file_valid": False,
                "overall_quality": "FAIL",
                "quality_flags": [
                    "unable_to_read_image"
                ]
            }

        # Run checks
        
        blur_score, blur_status = self.check_blur(
            image
        )

        brightness_value, brightness = (
            self.check_brightness(image)
        )

        resolution, resolution_status = (
            self.check_resolution(image)
        )

       # Flags for borderline cases

        if blur_status == "reject":
            quality_flags.append("very_blurry")

        elif blur_status == "review":
            quality_flags.append("slightly_blurry")

        if brightness == "dark":
            quality_flags.append("low_brightness")

        if brightness == "overexposed":
            quality_flags.append("overexposed")

        if resolution_status == "reject":
            quality_flags.append("low_resolution")

        # Determine overall quality

        if (
            blur_status == "reject"
            or resolution_status == "reject"
        ):
            overall_quality = "FAIL"

        elif len(quality_flags) > 0:
            overall_quality = "REVIEW"

        else:
            overall_quality = "PASS"

        return {
            "blur_score": round(
                blur_score, 2
            ),
            "blur_status": blur_status,

            "brightness": brightness,
            "brightness_value": round(
                brightness_value, 2
            ),

            "resolution": resolution,
            "resolution_status":
                resolution_status,

            "file_format": file_format,
            "file_valid": True,

            "overall_quality":
                overall_quality,

            "quality_flags":
                quality_flags
        }


# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":

    image_path = "sample_images/test_trees/high_contrast.png"

    checker = ImageQualityChecker()

    result = checker.check_quality(
        image_path
    )

    print(result)