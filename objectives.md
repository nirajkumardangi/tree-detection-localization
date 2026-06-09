# Tree Detection and Localization Challenge

## Background

[FloCard](https://flocard.app) is a sustainability-focused digital platform that combines digital identity, community engagement, climate action, and nature-based project tools. The platform supports businesses, communities, and sustainability initiatives through features such as digital business cards, sustainability profiles, carbon offsetting, project development, and tools aligned with climate and SDG goals.

FloCard also has a Tree Planters App used by communities, planters, and farms working on afforestation projects.

The app helps users digitally tag and trace trees using:

- geo-tagged single tree images
- Google Map based boundary tagging for clusters of trees or forest areas
- mobile app or mobile browser based field capture
- offline capture support for areas with low or no internet connectivity

Tree tagging usually happens in remote or low-connectivity areas. Users capture the tree image and location first. Later, when internet connectivity is available, the captured assets are synced and edited with details such as species, age, date of plantation, and related information. After review and approval, the tree record becomes a blockchain-based tree asset.

## Current Tree Tagging Flow

The tree asset creation process broadly follows three steps:

1. A user captures a tree image and geo-tag in the mobile app or mobile browser, often in offline mode.
2. The asset is synced later and edited with details such as species, age, plantation date, and other metadata.
3. The asset goes through an approval step before becoming a blockchain-based asset.

This process works, but it depends heavily on the quality of the image and whether the captured image actually contains a valid tree.

## Problem Statement

During tree tagging, users may accidentally capture non-tree images, unclear images, partial tree images, or images where multiple trees and background objects are mixed together.

If a non-tree image or poor-quality image passes through the tagging and approval process, it can become an incorrect tree asset. This affects asset quality and can also affect downstream carbon or GHG offset estimates.

FloCard is exploring an AI-assisted workflow where tree images captured during the tagging process can be checked to confirm whether a tree is present and where the tree appears in the image.

## Challenge Objective

Build a solution that can detect and localize visible trees in uploaded images.

The solution should help identify whether a submitted image contains one or more trees and provide a reviewable location output such as a bounding box or segmentation mask.

## Expected Outcome

A useful solution should be able to:

- accept tree tagging images as input
- identify whether one or more trees are visible
- localize detected trees using bounding boxes, masks, or another reviewable format
- flag unclear or low-confidence images
- generate metadata for each detection
- provide a simple way to review detected outputs
- document the approach, assumptions, limitations, and failure cases

## Suggested Approach

Contributors are free to propose their own approach.

Possible approaches may include:

- object detection models
- image segmentation models
- vision transformer based detection
- YOLO-style models
- Segment Anything style workflows
- hybrid detection and quality-check workflows

The solution should explain why the selected approach is suitable and what kinds of images it may fail on.

## Suggested Stack

Preferred languages:

- Python
- C#

Possible libraries and tools:

- OpenCV
- Pillow
- PyTorch
- TensorFlow
- YOLO
- Detectron2
- Segment Anything
- ONNX Runtime
- ML.NET where applicable

Contributors may use other tools if they explain the reasoning.

## Data Access

Images are not included publicly in this repository unless they are open, synthetic, or approved for public use.

Contributors may use:

- open-license tree images
- contributor-created tree images
- approved sample image packs provided by the maintainers

Contributors who need access to image samples can contact the maintainers by email. Contact [abhijeet@366pitech.com]

Do not commit private geo-tagged images, precise location data, private farm or project data, credentials, or restricted-license imagery to the repository.

## Contribution Guidelines

- Fork the repository.
- Create a feature branch.
- Submit your Contribution through a pull request.
- Keep the implementation focused on this challenge.
- Do not commit private images, precise location data, credentials, or large generated datasets.
- Include setup and running instructions.
- Include sample output using safe, open, synthetic, or approved images.
- Explain your assumptions and known limitations.
- Mention any additional data you needed or data gaps you found.
- Document how the solution can be customized and scaled.

