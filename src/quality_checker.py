from pathlib import Path

import cv2

from src.config import (
    SUPPORTED_FORMATS,
    MIN_WIDTH,
    MIN_HEIGHT,
    BLUR_REJECT_THRESHOLD,
    BLUR_REVIEW_THRESHOLD,
    BRIGHTNESS_DARK_THRESHOLD,
    BRIGHTNESS_BRIGHT_THRESHOLD,
    CONTRAST_LOW_THRESHOLD,
)


class QualityChecker:
    def check(self, image_path: str) -> dict:
        """
        Main method to validate image quality.
        """

        flags = []

        
        # Validate file
        
        image = cv2.imread(image_path)

        if image is None:
            return {
                "blur_score": 0,
                "blur_status": "invalid",
                "brightness": "invalid",
                "brightness_value": 0,
                "contrast": "invalid",
                "contrast_value": 0,
                "resolution": "unknown",
                "resolution_status": "invalid",
                "file_format": self._get_extension(image_path),
                "file_valid": False,
                "overall_quality": "FAIL",
                "quality_flags": ["corrupt_or_unreadable_file"],
            }

       
        # Validate format
        
        file_format = self._get_extension(image_path)

        if file_format not in SUPPORTED_FORMATS:
            flags.append("unsupported_format")

       
        # Resolution Check
      
        height, width = image.shape[:2]

        resolution = f"{width}x{height}"

        if width < MIN_WIDTH or height < MIN_HEIGHT:
            resolution_status = "reject"
            flags.append("resolution_too_low")
        else:
            resolution_status = "acceptable"

       
        # Blur Check
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur_score = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        if blur_score < BLUR_REJECT_THRESHOLD:
            blur_status = "reject"
            flags.append("very_blurry")

        elif blur_score < BLUR_REVIEW_THRESHOLD:
            blur_status = "review"
            flags.append("slightly_blurry")

        else:
            blur_status = "acceptable"

        
        # Brightness Check

        brightness_value = float(gray.mean())

        if brightness_value < BRIGHTNESS_DARK_THRESHOLD:
            brightness_status = "too_dark"
            flags.append("too_dark")

        elif brightness_value > BRIGHTNESS_BRIGHT_THRESHOLD:
            brightness_status = "too_bright"
            flags.append("overexposed")

        else:
            brightness_status = "normal"

       
        # Contrast Check

        contrast_value = float(gray.std())

        if contrast_value < CONTRAST_LOW_THRESHOLD:
            contrast_status = "low"
            flags.append("low_contrast")

        else:
            contrast_status = "normal"


        # Overall Quality

        critical_flags = {
            "very_blurry",
            "resolution_too_low",
        }

        if any(flag in critical_flags for flag in flags):
            overall_quality = "FAIL"

        elif flags:
            overall_quality = "REVIEW"

        else:
            overall_quality = "PASS"


        # Final Response

        return {
            "blur_score": round(float(blur_score), 2),
            "blur_status": blur_status,
            "brightness": brightness_status,
            "brightness_value": round(brightness_value, 2),
            "contrast": contrast_status,
            "contrast_value": round(contrast_value, 2),
            "resolution": resolution,
            "resolution_status": resolution_status,
            "file_format": file_format,
            "file_valid": True,
            "overall_quality": overall_quality,
            "quality_flags": flags,
        }

    @staticmethod
    def _get_extension(image_path: str) -> str:
        return Path(image_path).suffix.lower().replace(".", "")

