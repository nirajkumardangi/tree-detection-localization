# FloCard Tree Detection and Localization Challenge
# 8-Day Development Plan

---

## Overview

| Detail | Info |
|--------|------|
| **Project** | Tree Detection and Localization for FloCard Tree Planters App |
| **Duration** | 8 Days |
| **Goal** | Build an AI-assisted pipeline that detects and localizes trees in uploaded images |
| **Output** | Working detection pipeline + annotated images + JSON metadata + review interface |

---

## Team Roles (Suggested)

| Role | Responsibility |
|------|---------------|
| ML Engineer | Model selection, training, detection pipeline |
| Backend Developer | API, file handling, metadata generation |
| Frontend Developer | Review dashboard / simple UI |
| QA / Tester | Image testing, edge cases, validation |
| Project Lead | Documentation, coordination, PR submission |

> Note: Roles can overlap for smaller teams. Solo contributors should follow the same day plan sequentially.

---

## Daily Plan

### DAY 1 — Project Setup and Research
**Theme: Foundation**

#### Goals:
- Set up the project repository and folder structure
- Understand the full problem and define scope clearly
- Research and finalize the tech stack and model choices
- Identify and collect open-license tree images for testing

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1.1 | Fork the FloCard repository and create feature branch | All | [ ] |
| 1.2 | Set up Python virtual environment | ML / Backend | [ ] |
| 1.3 | Install base dependencies — OpenCV, Pillow, PyTorch, Ultralytics YOLO | ML | [ ] |
| 1.4 | Define project folder structure (see below) | Backend | [ ] |
| 1.5 | Research YOLOv8 capabilities for tree/plant detection | ML | [ ] |
| 1.6 | Research SAM (Segment Anything Model) integration | ML | [ ] |
| 1.7 | Collect 30–50 open-license tree images for testing | All | [ ] |
| 1.8 | Collect 10–15 non-tree images for negative testing | All | [ ] |
| 1.9 | Create requirements.txt with all dependencies | Backend | [ ] |
| 1.10 | Write initial README.md with project description | Lead | [ ] |

#### Folder Structure to Create:
```
flocard-tree-detection/
├── src/
│   ├── quality_checker.py
│   ├── tree_detector.py
│   ├── segmentation.py
│   ├── confidence_scorer.py
│   ├── metadata_generator.py
│   └── pipeline.py
├── api/
│   └── app.py
├── dashboard/
│   └── index.html
├── models/
│   └── (model weights stored here - not committed)
├── sample_images/
│   ├── test_trees/
│   └── test_non_trees/
├── outputs/
│   ├── annotated/
│   └── metadata/
├── tests/
│   └── test_pipeline.py
├── docs/
│   └── approach.md
├── requirements.txt
├── README.md
└── plan.md
```

#### End of Day Checklist:
- [ ] Repository forked and branch created
- [ ] Environment running without errors
- [ ] Sample images collected and organized
- [ ] Folder structure created
- [ ] Tech stack finalized and documented

---

### DAY 2 — Image Quality Checker Module
**Theme: Gate Keeper**

#### Goals:
- Build the first layer of the pipeline — image quality validation
- Ensure bad images are flagged before hitting the detection model
- Define quality scoring logic

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 2.1 | Build blur detection using Laplacian variance (OpenCV) | ML / Backend | [ ] |
| 2.2 | Build brightness and contrast checker | ML / Backend | [ ] |
| 2.3 | Build resolution validator (minimum 480x480) | Backend | [ ] |
| 2.4 | Build file format validator (JPG, PNG, HEIC support) | Backend | [ ] |
| 2.5 | Build corrupt image / unreadable file handler | Backend | [ ] |
| 2.6 | Combine all checks into quality_checker.py module | Backend | [ ] |
| 2.7 | Define quality score output format | Lead | [ ] |
| 2.8 | Write unit tests for quality checker | QA | [ ] |
| 2.9 | Test with collected sample images (good and bad) | QA | [ ] |
| 2.10 | Document quality check thresholds and reasoning | Lead | [ ] |

#### Quality Score Output Format:
```json
{
  "blur_score": 145.6,
  "blur_status": "acceptable",
  "brightness": "normal",
  "brightness_value": 118.4,
  "resolution": "1920x1080",
  "resolution_status": "acceptable",
  "file_format": "JPG",
  "file_valid": true,
  "overall_quality": "PASS",
  "quality_flags": []
}
```

#### Blur Threshold Reference:
```
Laplacian Variance:
< 50   → Very blurry → REJECT
50–100 → Slightly blurry → FLAG FOR REVIEW
> 100  → Acceptable → PASS
```

#### End of Day Checklist:
- [ ] quality_checker.py complete and functional
- [ ] Unit tests written and passing
- [ ] Tested on at least 20 sample images
- [ ] Thresholds documented

---

### DAY 3 — Tree Detection Module
**Theme: Core Intelligence**

#### Goals:
- Build the main tree detection module using YOLOv8
- Output bounding boxes, confidence scores, and tree count
- Handle single tree and multiple tree scenarios

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 3.1 | Install Ultralytics YOLOv8 | ML | [ ] |
| 3.2 | Load pre-trained YOLOv8 model (COCO weights) | ML | [ ] |
| 3.3 | Identify relevant class labels for trees/plants in COCO | ML | [ ] |
| 3.4 | Build tree_detector.py — run inference on input image | ML | [ ] |
| 3.5 | Extract bounding box coordinates per detection | ML | [ ] |
| 3.6 | Extract confidence score per detection | ML | [ ] |
| 3.7 | Filter detections below minimum confidence threshold (0.4) | ML | [ ] |
| 3.8 | Handle zero detection case (no tree found) | ML | [ ] |
| 3.9 | Handle multiple detections (multiple trees in one image) | ML | [ ] |
| 3.10 | Return structured detection result from module | ML | [ ] |
| 3.11 | Test detector on collected sample images | QA | [ ] |
| 3.12 | Log false positives and false negatives found | QA | [ ] |

#### Detection Output Format:
```json
{
  "tree_detected": true,
  "tree_count": 2,
  "detections": [
    {
      "detection_id": 1,
      "class_label": "tree",
      "confidence": 0.91,
      "bounding_box": {
        "x_min": 120,
        "y_min": 45,
        "x_max": 480,
        "y_max": 890
      }
    }
  ]
}
```

#### COCO Class Notes:
```
COCO Dataset includes:
- Class 58: potted plant
- Custom fine-tuning may be needed for outdoor trees
- Consider using open tree detection datasets for fine-tuning
  (OpenImages, iNaturalist, TreeDetection datasets)
```

#### End of Day Checklist:
- [ ] tree_detector.py complete and returning structured output
- [ ] Tested on sample images — trees detected correctly
- [ ] False positives and negatives logged
- [ ] Confidence threshold documented

---

### DAY 4 — Segmentation Module and Confidence Scoring
**Theme: Precision and Judgment**

#### Goals:
- Add pixel-level segmentation using SAM or YOLOv8-seg
- Build confidence scoring and validation status logic
- Define PASS / REVIEW / REJECT logic

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 4.1 | Evaluate SAM vs YOLOv8-seg for segmentation — pick one | ML | [ ] |
| 4.2 | Install and load chosen segmentation model | ML | [ ] |
| 4.3 | Build segmentation.py — generate masks for detected trees | ML | [ ] |
| 4.4 | Calculate tree area percentage in image from mask | ML | [ ] |
| 4.5 | Handle cases where segmentation fails or produces no mask | ML | [ ] |
| 4.6 | Build confidence_scorer.py | Backend | [ ] |
| 4.7 | Define scoring logic combining detection + quality scores | Backend | [ ] |
| 4.8 | Define PASS / NEEDS REVIEW / REJECT thresholds | Lead | [ ] |
| 4.9 | Generate flags list for each image | Backend | [ ] |
| 4.10 | Test segmentation on sample images | QA | [ ] |
| 4.11 | Test scoring on multiple scenarios | QA | [ ] |
| 4.12 | Document scoring rules | Lead | [ ] |

#### Confidence Scoring Logic:
```
PASS         → Detection confidence >= 0.75 AND quality PASS
NEEDS REVIEW → Detection confidence 0.50–0.74 OR quality FLAGGED
REJECT       → No tree detected OR quality FAIL (very blurry / corrupt)

Flags triggered by:
- Low confidence detection
- Multiple trees detected (verify single tree tagging intent)
- Tree area < 10% of image (tree too small / far away)
- Quality issues (blur, brightness)
- No tree detected
```

#### Segmentation Output Addition:
```json
{
  "mask_available": true,
  "tree_area_pixels": 145200,
  "image_total_pixels": 2073600,
  "tree_area_percentage": 7.0,
  "mask_file": "outputs/masks/tree_tag_001_mask.png"
}
```

#### End of Day Checklist:
- [ ] segmentation.py complete and generating masks
- [ ] confidence_scorer.py complete with PASS/REVIEW/REJECT logic
- [ ] Tested scoring across all image scenarios
- [ ] Scoring rules documented

---

### DAY 5 — Full Pipeline Integration and Metadata Generator
**Theme: Putting It All Together**

#### Goals:
- Integrate all modules into one end-to-end pipeline
- Build metadata generator producing final JSON output
- Build annotated image output with drawn boxes and masks

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 5.1 | Build pipeline.py — orchestrate all modules in sequence | Backend | [ ] |
| 5.2 | Define pipeline input (image file path or bytes) | Backend | [ ] |
| 5.3 | Define pipeline output (annotated image path + JSON path) | Backend | [ ] |
| 5.4 | Build metadata_generator.py — compile full JSON output | Backend | [ ] |
| 5.5 | Build annotated image generator using OpenCV draw functions | ML | [ ] |
| 5.6 | Draw bounding boxes on detected trees | ML | [ ] |
| 5.7 | Overlay segmentation masks (transparent color overlay) | ML | [ ] |
| 5.8 | Add confidence score label on each bounding box | ML | [ ] |
| 5.9 | Add status banner on image (PASS / REVIEW / REJECT) | ML | [ ] |
| 5.10 | Save annotated image to outputs/annotated/ | Backend | [ ] |
| 5.11 | Save JSON metadata to outputs/metadata/ | Backend | [ ] |
| 5.12 | Run end-to-end test on 20+ sample images | QA | [ ] |
| 5.13 | Fix integration bugs | All | [ ] |

#### Full Pipeline Flow in Code:
```python
# pipeline.py execution flow

def run_pipeline(image_path):
    # Step 1 — Quality Check
    quality_result = check_image_quality(image_path)
    
    # Step 2 — Tree Detection
    detection_result = detect_trees(image_path)
    
    # Step 3 — Segmentation
    segmentation_result = segment_trees(image_path, detection_result)
    
    # Step 4 — Confidence Scoring
    score_result = calculate_confidence(
        quality_result,
        detection_result,
        segmentation_result
    )
    
    # Step 5 — Generate Annotated Image
    annotated_image_path = generate_annotated_image(
        image_path,
        detection_result,
        segmentation_result,
        score_result
    )
    
    # Step 6 — Generate JSON Metadata
    metadata_path = generate_metadata(
        image_path,
        quality_result,
        detection_result,
        segmentation_result,
        score_result,
        annotated_image_path
    )
    
    return {
        "annotated_image": annotated_image_path,
        "metadata": metadata_path,
        "status": score_result["validation_status"]
    }
```

#### End of Day Checklist:
- [ ] pipeline.py running end-to-end without errors
- [ ] Annotated images generating correctly
- [ ] JSON metadata generating correctly
- [ ] Tested on full sample image set

---

### DAY 6 — API Layer and Simple Review Interface
**Theme: Usability**

#### Goals:
- Wrap the pipeline in a simple REST API
- Build a minimal review interface (web-based)
- Enable image upload and result viewing

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 6.1 | Build FastAPI or Flask app in api/app.py | Backend | [ ] |
| 6.2 | Create POST /detect endpoint — accepts image upload | Backend | [ ] |
| 6.3 | Create GET /results/{image_id} endpoint | Backend | [ ] |
| 6.4 | Create GET /results endpoint — list all processed images | Backend | [ ] |
| 6.5 | Add file size limit and format validation at API level | Backend | [ ] |
| 6.6 | Return annotated image URL and JSON metadata in response | Backend | [ ] |
| 6.7 | Build minimal HTML review dashboard (dashboard/index.html) | Frontend | [ ] |
| 6.8 | Image upload form in dashboard | Frontend | [ ] |
| 6.9 | Display original image and annotated image side by side | Frontend | [ ] |
| 6.10 | Display detection metadata in readable format | Frontend | [ ] |
| 6.11 | Show PASS / REVIEW / REJECT status clearly with color coding | Frontend | [ ] |
| 6.12 | Add manual approve / reject buttons in dashboard | Frontend | [ ] |
| 6.13 | Test API with Postman or curl | QA | [ ] |
| 6.14 | Test dashboard in browser | QA | [ ] |

#### API Endpoints:
```
POST   /detect              → Upload image, run pipeline, return result
GET    /results             → List all processed image results
GET    /results/{image_id}  → Get specific image result
GET    /health              → API health check
```

#### API Response Example:
```json
{
  "image_id": "tree_tag_20240815_001",
  "status": "PASS",
  "tree_detected": true,
  "tree_count": 2,
  "overall_confidence": 0.91,
  "annotated_image_url": "/outputs/annotated/tree_tag_001_annotated.jpg",
  "metadata_url": "/outputs/metadata/tree_tag_001.json",
  "flags": [],
  "recommendation": "Image contains clearly visible trees. Approved for tagging."
}
```

#### Dashboard Color Coding:
```
PASS         → Green banner
NEEDS REVIEW → Yellow / Orange banner
REJECT       → Red banner
```

#### End of Day Checklist:
- [ ] API running locally without errors
- [ ] All endpoints tested and working
- [ ] Dashboard loading and functional
- [ ] Image upload and result display working

---

### DAY 7 — Testing, Edge Cases, and Quality Assurance
**Theme: Hardening**

#### Goals:
- Thoroughly test the full pipeline against edge cases
- Identify and fix failure cases
- Improve thresholds based on test results

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 7.1 | Test with blurry images — verify REJECT or FLAG behavior | QA | [ ] |
| 7.2 | Test with non-tree images (vehicles, people, buildings) | QA | [ ] |
| 7.3 | Test with images of seedlings and small plants | QA | [ ] |
| 7.4 | Test with dense forest / multiple overlapping tree images | QA | [ ] |
| 7.5 | Test with very dark or night-condition images | QA | [ ] |
| 7.6 | Test with high-angle or aerial-style images | QA | [ ] |
| 7.7 | Test with images containing tree + person in frame | QA | [ ] |
| 7.8 | Test with corrupt or empty image files | QA | [ ] |
| 7.9 | Test with very high resolution images (>10MB) | QA | [ ] |
| 7.10 | Test with very low resolution images (<480px) | QA | [ ] |
| 7.11 | Compile test results table — pass/fail/flag outcomes | QA / Lead | [ ] |
| 7.12 | Adjust confidence thresholds based on test results | ML | [ ] |
| 7.13 | Fix any pipeline crash bugs | All | [ ] |
| 7.14 | Write unit tests for all modules | QA | [ ] |
| 7.15 | Run full test suite and confirm passing | QA | [ ] |

#### Test Results Table Template:
```
| Image Type              | Expected Result | Actual Result | Pass/Fail | Notes |
|-------------------------|-----------------|---------------|-----------|-------|
| Clear single tree       | PASS            |               |           |       |
| Blurry tree             | REVIEW/REJECT   |               |           |       |
| Non-tree (car)          | REJECT          |               |           |       |
| Seedling/sapling        | REVIEW          |               |           |       |
| Dense forest            | PASS            |               |           |       |
| Night image             | REJECT          |               |           |       |
| Tree + person           | PASS/REVIEW     |               |           |       |
| Corrupt file            | REJECT          |               |           |       |
| Very low resolution     | REJECT          |               |           |       |
| Multiple trees          | PASS            |               |           |       |
```

#### End of Day Checklist:
- [ ] All edge cases tested and results logged
- [ ] Thresholds adjusted and re-tested
- [ ] No crash bugs remaining
- [ ] Unit test suite passing

---

### DAY 8 — Documentation, Sample Outputs, and Submission
**Theme: Delivery**

#### Goals:
- Complete all documentation
- Prepare sample outputs for submission
- Final review and pull request submission

#### Tasks:

| # | Task | Owner | Status |
|---|------|-------|--------|
| 8.1 | Complete README.md with setup and running instructions | Lead | [ ] |
| 8.2 | Write docs/approach.md — model choices and reasoning | ML / Lead | [ ] |
| 8.3 | Document all known limitations | Lead | [ ] |
| 8.4 | Document all failure cases with examples | Lead | [ ] |
| 8.5 | Document assumptions made during development | Lead | [ ] |
| 8.6 | Document customization and scaling options | Lead | [ ] |
| 8.7 | Prepare sample output images (open-license only) | All | [ ] |
| 8.8 | Prepare sample JSON metadata outputs | All | [ ] |
| 8.9 | Verify no private geo-tagged images in repository | All | [ ] |
| 8.10 | Verify no credentials or API keys in code | All | [ ] |
| 8.11 | Verify no large model weight files committed | All | [ ] |
| 8.12 | Final code review and cleanup | All | [ ] |
| 8.13 | Confirm requirements.txt is complete and accurate | Backend | [ ] |
| 8.14 | Run full pipeline one final time end-to-end | QA | [ ] |
| 8.15 | Submit pull request with complete description | Lead | [ ] |

#### README.md Must Include:
```
1. Project Overview
2. Problem Statement
3. Approach and Model Choices
4. Folder Structure
5. Requirements and Installation Steps
6. How to Run the Pipeline
7. How to Run the API
8. How to Use the Dashboard
9. Sample Output Examples
10. Known Limitations
11. Failure Cases
12. Customization Options
13. Data Sources Used
14. License Information
```

#### Pull Request Checklist:
```
[ ] Code is clean and commented
[ ] README.md is complete
[ ] Sample outputs included (safe images only)
[ ] No private data committed
[ ] No credentials or keys committed
[ ] requirements.txt is accurate
[ ] Limitations and failure cases documented
[ ] Branch is up to date with main
[ ] PR description explains what was built and why
```

---

## 8-Day Summary Timeline

```
Day 1  │ ██████████ Project Setup + Research + Sample Images
Day 2  │ ██████████ Image Quality Checker Module
Day 3  │ ██████████ Tree Detection Module (YOLOv8)
Day 4  │ ██████████ Segmentation + Confidence Scoring
Day 5  │ ██████████ Full Pipeline Integration + Metadata Generator
Day 6  │ ██████████ API Layer + Review Dashboard
Day 7  │ ██████████ Testing + Edge Cases + Bug Fixes
Day 8  │ ██████████ Documentation + Sample Outputs + Submission
```

---

## Milestone Tracker

| Milestone | Target Day | Status |
|-----------|------------|--------|
| Environment setup complete | Day 1 | [ ] |
| Quality checker working | Day 2 | [ ] |
| Tree detection working | Day 3 | [ ] |
| Segmentation and scoring working | Day 4 | [ ] |
| Full pipeline running end-to-end | Day 5 | [ ] |
| API and dashboard live | Day 6 | [ ] |
| All edge cases tested | Day 7 | [ ] |
| Pull request submitted | Day 8 | [ ] |

---

## Risk and Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| COCO model does not detect outdoor trees well | High | Fine-tune on open tree datasets or use custom weights |
| SAM model too heavy for available compute | Medium | Fall back to YOLOv8-seg for segmentation |
| Not enough open-license test images | Medium | Use iNaturalist, Unsplash (open license), or synthetic images |
| API performance slow for large images | Low | Add image resize step before inference |
| Confidence thresholds too strict / too loose | High | Tune thresholds daily during Day 7 testing |

---

## Notes for Contributors

- Follow the day plan but adapt if blocked — document any deviations
- Prioritize Days 1–5 (core pipeline) over Days 6–8 (interface) if time is short
- A working pipeline with good documentation is better than a broken UI
- Do not commit private images, geo-tagged data, or model weights
- Ask maintainers for sample image packs if open-license images are insufficient
  Contact: abhijeet@366pitech.com

---

*Plan version: 1.0 | FloCard Tree Detection Challenge*
```