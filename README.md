# 🌳 Tree Detection & Localization System

AI-powered tree detection and localization pipeline for validating tree-tagging images before they are approved as digital tree assets.

---

## Overview

This project provides an automated image validation and tree detection workflow for tree-tagging applications.

The system analyzes uploaded images and determines:

- Whether one or more trees are present
- The location of detected trees using bounding boxes
- Pixel-level tree segmentation masks
- Image quality status
- Detection confidence
- Final validation status (PASS / REVIEW / REJECT)

The goal is to improve tree asset quality by preventing non-tree, low-quality, or ambiguous images from entering the approval workflow.

---

## Problem Statement

Tree-tagging applications often rely on manually captured field images.

Common issues include:

- Non-tree images accidentally uploaded
- Blurry or low-quality images
- Partial tree captures
- Multiple trees in a single image
- Low visibility due to lighting conditions

These issues can result in incorrect tree records and affect downstream reporting and carbon offset calculations.

This solution introduces an AI-assisted validation layer that automatically verifies tree presence and location before approval.

---

## Solution Architecture

![High Level Architecture](docs/images/hld.png)

### Processing Flow

```text
Input Image
      │
      ▼
Image Quality Validation
      │
      ▼
Tree Detection (YOLOv8)
      │
      ▼
Tree Localization
(Bounding Boxes + Masks)
      │
      ▼
Confidence Validation
      │
      ▼
Metadata Generation
      │
      ▼
Annotated Image + JSON Output
````

The architecture follows a modular pipeline design, allowing each component to be improved independently.

---

## Key Features

### Image Quality Validation

Performs image pre-checks before AI inference.

Checks include:

* Blur detection
* Brightness validation
* Contrast validation
* Resolution validation
* Corrupt file detection
* File format validation

Output:

```json
{
  "overall_quality": "PASS",
  "blur_score": 145.6,
  "resolution": "1920x1080"
}
```

---

### Tree Detection

Detects visible trees in uploaded images.

Capabilities:

* Single tree detection
* Multiple tree detection
* Bounding box generation
* Confidence scoring

Model:

```text
YOLOv8
```

Output:

```json
{
  "tree_detected": true,
  "tree_count": 2
}
```

---

### Tree Segmentation

Provides pixel-level localization for detected trees.

Capabilities:

* Tree mask generation
* Tree area estimation
* Improved localization accuracy

Models:

```text
SAM (Segment Anything)
or
YOLOv8-Seg
```

---

### Confidence Validation

Combines:

* Quality score
* Detection confidence
* Segmentation metrics

Produces:

```text
PASS
REVIEW
REJECT
```

---

### Metadata Generation

Creates structured JSON output for downstream systems.

Includes:

* Tree count
* Bounding boxes
* Confidence scores
* Segmentation information
* Quality metrics
* Validation status

---

## Project Structure

```text
tree-detection-localization/
│
├── api/
│
├── dashboard/
│
├── docs/
│
├── models/
│
├── outputs/
│   ├── annotated/
│   ├── masks/
│   └── metadata/
│
├── sample_images/
│   ├── test_trees/
│   └── test_non_trees/
│
├── src/
│   ├── quality_checker.py
│   ├── tree_detector.py
│   ├── segmentation.py
│   ├── confidence_scorer.py
│   ├── metadata_generator.py
│   └── pipeline.py
│
├── tests/
│
├── venv/                  # Local virtual environment (excluded from Git)
│   ├── Include/
│   ├── Lib/
│   └── Scripts/
│
├── .gitignore
├── README.md
├── requirements.txt
└── project_plan.md
```

### Directory Description

| Directory | Purpose |
|------------|----------|
| `api/` | FastAPI application and API endpoints |
| `dashboard/` | Web-based review dashboard |
| `docs/` | Architecture diagrams, design documents, and approach documentation |
| `models/` | YOLO and segmentation model weights (not committed to Git) |
| `outputs/annotated/` | Images with bounding boxes and segmentation overlays |
| `outputs/masks/` | Generated tree segmentation masks |
| `outputs/metadata/` | JSON metadata outputs |
| `sample_images/test_trees/` | Sample tree images used for testing |
| `sample_images/test_non_trees/` | Negative test images |
| `src/` | Core AI pipeline modules |
| `tests/` | Unit and integration tests |
| `venv/` | Python virtual environment (local development only) |

> Note: The `venv/` directory should not be committed to the repository and must be included in `.gitignore`.

---

## Technology Stack

### AI / ML

* Python
* PyTorch
* Ultralytics YOLOv8
* Segment Anything Model (SAM)
* OpenCV
* Pillow

### Backend

* FastAPI
* Uvicorn

### Frontend

* HTML
* JavaScript
* Bootstrap

### Storage

* Local File System
* JSON Metadata

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-org/tree-detection-localization.git

cd tree-detection-localization
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

### Process Single Image

```bash
python src/pipeline.py \
--image sample_images/test_trees/tree_01.jpg
```

Output:

```text
outputs/
├── annotated/
├── masks/
└── metadata/
```

---

## Running the API

Start server:

```bash
uvicorn api.app:app --reload
```

API available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Detect Trees

```http
POST /detect
```

### Get Results

```http
GET /results
```

### Get Specific Result

```http
GET /results/{image_id}
```

---

## Sample Response

```json
{
  "image_id": "tree_001",
  "status": "PASS",
  "tree_detected": true,
  "tree_count": 2,
  "overall_confidence": 0.91,
  "flags": []
}
```

---

## Sample Output

### Annotated Image

Contains:

* Bounding boxes
* Segmentation masks
* Confidence labels
* Validation status banner

### JSON Metadata

```json
{
  "tree_detected": true,
  "tree_count": 2,
  "confidence": 0.91,
  "status": "PASS"
}
```

---

## Validation Rules

| Status | Criteria                           |
| ------ | ---------------------------------- |
| PASS   | Confidence ≥ 0.75 and Quality PASS |
| REVIEW | Confidence between 0.50–0.74       |
| REJECT | No tree detected or Quality FAIL   |

---

## Known Limitations

* Dense forests may produce overlapping detections.
* Small saplings may not be detected reliably.
* Night-time images can reduce accuracy.
* Heavy occlusion may impact segmentation quality.
* General YOLO models may require fine-tuning for outdoor tree species.

---

## Future Improvements

* Custom-trained tree detection model
* Species classification
* Height estimation
* Carbon sequestration estimation
* Geospatial validation
* Edge-device deployment
* ONNX optimization
* Mobile inference support

---

## Testing Scenarios

* Clear tree image
* Multiple trees
* Non-tree image
* Blurry image
* Night image
* Dense forest image
* Corrupt file
* Low-resolution image

---

## Security Considerations

Do not commit:

* Private geo-tagged images
* Farm location data
* Credentials
* API keys
* Model weights
* Sensitive project information
