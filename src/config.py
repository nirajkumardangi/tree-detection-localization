# Supported file formats

SUPPORTED_FORMATS = {
    "jpg",
    "jpeg",
    "png",
    "heic"
}

# Resolution

MIN_WIDTH = 480
MIN_HEIGHT = 480

# Blur thresholds

BLUR_REJECT_THRESHOLD = 50
BLUR_REVIEW_THRESHOLD = 100

# Brightness thresholds

BRIGHTNESS_DARK_THRESHOLD = 40
BRIGHTNESS_BRIGHT_THRESHOLD = 220

# Contrast thresholds

CONTRAST_LOW_THRESHOLD = 20

# Detection

MODEL_PATH = "models/best.pt"

MIN_DETECTION_CONFIDENCE = 0.30
MAX_DETECTIONS = 100

# SAM2

USE_SAM2 = True

SAM2_CHECKPOINT = (
    "models/sam2/checkpoints/"
    "sam2.1_hiera_small.pt"
)

SAM2_CONFIG = "configs/sam2.1/sam2.1_hiera_s"

# Confidence Scoring

PASS_CONFIDENCE = 0.60
REVIEW_CONFIDENCE = 0.30

MIN_TREE_AREA_PERCENTAGE = 5


# Output

ANNOTATED_OUTPUT_DIR = "outputs/annotated"
METADATA_OUTPUT_DIR = "outputs/metadata"
MASK_OUTPUT_DIR = "outputs/masks"
