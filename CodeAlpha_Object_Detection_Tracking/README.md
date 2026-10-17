
# Object Detection and Tracking

## Overview

This project detects objects in real-time webcam streams or video files using YOLOv8 and tracks detected objects across frames using Deep SORT. OpenCV is used to process video frames and display bounding boxes, object labels, confidence scores, and tracking IDs.

## Features

- Supports webcam and video-file input.
- Detects common objects using a pretrained YOLOv8 model.
- Tracks objects across video frames using Deep SORT.
- Displays bounding boxes and object labels.
- Shows tracking IDs and detection confidence scores when available.
- Allows adjustment of the confidence threshold and frame width.
- Supports CPU execution and compatible CUDA-enabled GPUs.

## Technologies Used

- Python
- OpenCV
- Ultralytics YOLOv8
- PyTorch
- Deep SORT Realtime

## Project Structure

```text
object_detection_tracking/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd object_detection_tracking
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## How to Run

### Webcam

```powershell
python main.py
```

### Video file

```powershell
python main.py --source "path\to\your\video.mp4"
```

### Use a larger YOLOv8 model

```powershell
python main.py --model yolov8s.pt --conf 0.25 --width 960
```

The pretrained model weights may download automatically on the first run. The larger model may improve detection accuracy but can run more slowly.

Press `q` in the video window to stop the application.

## How It Works

1. OpenCV captures frames from the webcam or reads them from a video file.
2. YOLOv8 detects objects and returns bounding boxes, class labels, and confidence scores.
3. Detection results are passed to Deep SORT.
4. Deep SORT associates objects across frames and assigns tracking IDs.
5. OpenCV displays the processed video with detection and tracking information.

## Limitations

- The pretrained YOLOv8 model recognises its trained categories and may confuse visually similar objects.
- Tracking IDs may change when objects disappear, overlap, or become obscured.
- Processing speed depends on hardware, model size, and video resolution.

## Purpose

This project demonstrates object detection and multi-object tracking using Python and computer vision.
