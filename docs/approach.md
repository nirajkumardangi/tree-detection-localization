# Technical Approach — Tree Detection & Localization

## 1. Approach Overview

This solution uses a **hybrid two-stage detection + segmentation pipeline** combining:

1. **YOLO11** — for fast, accurate tree detection (bounding boxes + confidence)
2. **SAM2 (Segment Anything Model 2)** — for pixel-level tree segmentation using YOLO boxes as prompts

This hybrid approach was chosen because:

- **YOLO alone** provides fast detection with bounding boxes but cannot delineate exact tree boundaries
- **SAM2 alone** is a class-agnostic segmenter — it does not know what a "tree" is without a prompt
- **Combined**, YOLO identifies *where* trees are, and SAM2 produces *precise masks* for each detection

This is superior to a single-model approach because it separates the "what" (YOLO) from the "where exactly" (SAM2), allowing each model to do what it does best.

---

## 2. Why YOLO11?

| Reason | Detail |
|---|---|
| **Speed** | Real-time inference (~10-50ms per image on GPU) |
| **Accuracy** | State-of-the-art single-stage detector |
| **Custom training** | Easy to fine-tune on domain-specific tree datasets |
| **Single class** | Efficient for binary tree/no-tree detection |
| **Ultralytics ecosystem** | Well-maintained, production-ready framework |

The model was trained on **~55,000 images** (50k tree positives + 5k hard negatives) to achieve **94% precision** and **89% recall**.

### Why hard negatives matter

Without negative samples, YOLO models trained only on trees frequently produce false positives on:
- Bushes and shrubs (visually similar to tree canopies)
- Grass and agricultural fields (green background confusion)
- Indoor plants (similar leaf patterns)
- People standing near vegetation

The 5,000+ hard negative dataset specifically targets these confusion categories.

---

## 3. Why SAM2?

Meta's Segment Anything Model 2 (SAM2.1, `hiera_small` variant) provides:

- **Pixel-level masks** — precise tree boundaries rather than rectangular boxes
- **Prompt-based** — accepts bounding boxes from YOLO as input prompts
- **Zero-shot generalization** — works on any object without tree-specific training
- **Graceful fallback** — if SAM2 fails to load, the system falls back to bounding-box masks

### SAM2 integration strategy

Rather than running SAM2 on the entire image (expensive and noisy), we:

1. Run YOLO first to get bounding box coordinates
2. Feed each bounding box as a **box prompt** to SAM2
3. SAM2 generates a binary mask only within/around each box

This is significantly faster and more accurate than full-image segmentation.

---

## 4. Image Quality Pre-Check

Before running AI inference, images are validated for quality to:
- Avoid wasting GPU compute on unusable images
- Catch common field capture issues early
- Provide actionable feedback to the user

### Quality checks performed

| Check | Method | Why |
|---|---|---|
| **Blur detection** | Laplacian variance | Blurry images produce unreliable detections |
| **Brightness** | Grayscale mean | Too dark/bright images reduce model accuracy |
| **Contrast** | Grayscale std deviation | Low contrast makes trees hard to distinguish |
| **Resolution** | Pixel dimensions | Small images lack detail for accurate detection |
| **File format** | Extension validation | Only process supported formats |
| **File corruption** | OpenCV read test | Reject unreadable files immediately |

---

## 5. Confidence Scoring Logic

The final validation verdict combines multiple signals:

```
IF no tree detected → REJECT
IF quality = FAIL → flag "poor_image_quality"
IF tree_area < 5% → flag "tree_too_small"
IF multiple trees → flag "multiple_trees_detected"

IF confidence >= 0.60 AND quality = PASS AND no flags → PASS
IF confidence >= 0.30 → REVIEW
ELSE → REJECT
```

This tri-state system (PASS/REVIEW/REJECT) is designed for a human-in-the-loop workflow where:
- **PASS** images can be auto-approved
- **REVIEW** images require manual verification
- **REJECT** images are automatically filtered out

---

## 6. Assumptions

1. **Single-class detection** — The model only detects "tree" as a class. It does not differentiate species, age, or health.
2. **Outdoor images** — The model was trained primarily on outdoor field photos. Indoor plant images may not be detected reliably.
3. **Standard orientations** — Images are assumed to be right-side-up. Heavy rotation may affect detection.
4. **Reasonable image quality** — While the quality checker flags issues, the model works best on clear, well-lit photos.
5. **Single image per request** — The API processes one image at a time.

---

## 7. Known Limitations & Failure Cases

### Detection limitations

| Scenario | Behavior |
|---|---|
| **Dense forests** | Overlapping detections with lower individual confidence |
| **Small saplings** | May not be detected if below confidence threshold |
| **Night photos** | Significantly reduced detection accuracy |
| **Heavy shadows** | Tree canopy may blend with shadows |
| **Aerial / drone images** | Model trained on ground-level photos; aerial views may underperform |
| **Heavily occluded trees** | Partial visibility reduces confidence |

### Segmentation limitations

| Scenario | Behavior |
|---|---|
| **Overlapping tree canopies** | SAM2 may merge adjacent trees into one mask |
| **Trees against green background** | Mask boundaries may be imprecise |
| **Very small trees in large images** | Mask resolution may be insufficient |

### System limitations

| Limitation | Impact |
|---|---|
| **No batch processing** | One image per API request |
| **No species classification** | Only binary tree/no-tree |
| **GPU recommended** | CPU inference is significantly slower (~5-15s per image) |
| **Model weights not included** | Must be downloaded separately |

---

## 8. Customization & Scaling

### Configuration

All thresholds are centralized in `src/config.py`:
- Detection confidence thresholds
- Quality check thresholds
- Model paths
- Output directories

### Scaling options

1. **Horizontal scaling** — Run multiple API instances behind a load balancer
2. **GPU acceleration** — Deploy on CUDA-enabled instances for ~10x speedup
3. **Batch endpoint** — Add a `/detect/batch` endpoint for multiple images
4. **Model optimization** — Export to ONNX/TensorRT for faster inference
5. **Edge deployment** — Convert to TFLite/CoreML for on-device inference
6. **Async processing** — Add a job queue (Celery/Redis) for background processing

---

## 9. Data Gaps

- **Species diversity** — More training data needed for tropical/subtropical tree species
- **Seasonal variation** — Limited winter/deciduous tree images in training set
- **Geographic diversity** — Model may underperform in regions not represented in training data
- **Altitude variation** — Mountain/highland tree morphology differs from lowland trees
