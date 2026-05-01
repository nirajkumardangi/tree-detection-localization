# Tree Detection and Localization Scenario

## Overview

Build a self-contained tree detection and localization prototype using open, synthetic, or contributor-created imagery.

This scenario should identify visible trees in images and produce reviewable localization outputs such as bounding boxes or segmentation masks. It should not depend on any internal Canopy system, private field imagery, or proprietary model pipeline.

## What Problem It Solves

Tree analytics workflows often need to isolate individual trees before any downstream species, health, condition, or inventory analysis can happen. This scenario explores a practical public-safe pipeline for detecting and localizing trees in single-tree and multi-tree images.

The goal is not to build a production forestry inventory system. The goal is to create a limited-scope reference implementation for tree detection, localization metadata, visual review, and evaluation on open or contributor-created data.

## Scope

The implementation should include:

- local upload or folder-based ingestion of tree images
- support for open, synthetic, or contributor-created images
- tree detection in single-tree and multi-tree scenes
- bounding box and/or segmentation mask output
- confidence scores for detections where supported
- output metadata per image and per detected tree
- visual output generation showing detected trees
- lightweight review UI, static gallery, or notebook for inspection
- evaluation script using labeled examples where available
- documentation for setup, usage, assumptions, and limitations

## Non-Goals

This work packet is not intended to cover:

- private field imagery or customer datasets
- production forestry inventory accuracy
- internal Canopy architecture or roadmap implementation
- species identification
- health classification
- tree re-identification across visits
- carbon estimation or ESG reporting
- broad geospatial analytics platform work

## Expected Deliverables

A complete contribution should include:

- working local detection pipeline or notebook
- sample open/synthetic/contributor-created images or download instructions
- detection output schema
- generated sample detections
- visual review gallery, notebook, or lightweight UI
- evaluation script and sample evaluation output where labels exist
- setup and running documentation
- notes on assumptions, failure cases, and limitations
- notes on how the output could later be consumed by other tree analytics workflows

## Success Criteria

A submission will be considered successful if:

- it runs locally without private internal APIs
- it uses open, synthetic, or contributor-created imagery only
- it detects visible trees in sample images
- it produces bounding boxes and/or masks with traceable metadata
- visual outputs can be reviewed by a human
- evaluation metrics are reported when labeled data is available
- failures and uncertain detections are documented honestly

## Suggested Stack

Preferred stack:

- Python
- OpenCV / Pillow
- YOLO, Detectron2, MMDetection, Segment Anything, or similar open tooling
- COCO-style annotations where useful
- Streamlit, Gradio, static HTML, or notebook-based review where useful
- JSON, JSONL, or CSV for detection outputs

## Output Contract

The implementation should export detection results in a documented format. A useful minimal shape is:

```json
{
  "image_id": "string",
  "source_file": "string",
  "method": "tree_detection_localization",
  "detections": [
    {
      "tree_instance_id": "string",
      "label": "tree",
      "confidence": 0.0,
      "bbox_xyxy": [0, 0, 0, 0],
      "mask_file": "string",
      "review_status": "pending | accepted | rejected | edited"
    }
  ],
  "run_metadata": {
    "model_name": "string",
    "model_version": "string",
    "runtime": "local | hosted",
    "latency_ms": 0
  }
}
```

## Design Notes

This packet should remain independent. It may export tree crops or region metadata, but it should not require a separate species identification or re-identification project to be useful.

The intended flow is:

```text
Tree image
-> local ingestion
-> detection or segmentation model
-> bounding boxes or masks
-> visual review
-> detection metadata export
```

## Safety and Data Notes

Do not include private field imagery, private location data, customer imagery, restricted-license datasets, or internal Canopy data.

If using public imagery, document the source and license. If using contributor-created imagery, state that it is contributor-created and safe to redistribute.

## Submission Guidelines

- Fork the repository and create a feature branch for your contribution.
- Submit your work through a pull request against the main repository. Do not submit code, imagery, annotations, or datasets through email, chat, or shared drives.
- Open an issue first if your proposed approach changes the scope materially, introduces a major dependency, requires a hosted service by default, or needs a different runtime than the one described in this README.
- Include a short solution approach in the pull request that explains the detection method, model choice, annotation format, design tradeoffs, and known limitations.
- Include architecture documentation that shows the main components, data flow, configuration files, local storage, and output artifacts. A simple diagram is preferred where useful.
- Include setup and running instructions that allow a reviewer to run the project from a clean checkout.
- Include deployment notes, even if the project only runs locally. State the expected runtime, environment variables, model setup, storage paths, and optional services.
- Include scaling notes that explain what would need to change for larger image sets, batch inference, GPU execution, cloud storage, queues, or managed compute.
- Include integration notes describing how detection outputs could later feed other tree analytics workflows without depending on hidden internal APIs.
- Include code documentation for public functions, configuration options, CLI commands, model inputs, data formats, review states, and export formats.
- Include sample inputs and outputs using open, synthetic, or contributor-created imagery only.
- Include tests or validation checks for core behavior, such as output schema validation, image loading, detection export, review state handling, and error handling.
- Include a short quality report or evidence section showing sample runs, known failure cases, and how reviewers should inspect outputs.
- Keep secrets, credentials, API keys, generated caches, local model files, large generated outputs, and local environment files out of the repository.
- Add or update `.gitignore` where needed to prevent accidental submission of local data, model artifacts, generated files, or credentials.
- Use clear commit messages and keep unrelated refactors out of the pull request.
- The pull request should be reviewable as a standalone contribution: reviewers should not need access to internal roadmaps, private datasets, or proprietary platform details to understand or run it.

