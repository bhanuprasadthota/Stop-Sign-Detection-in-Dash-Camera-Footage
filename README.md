
Stop Sign Detection in Dash Camera Footage

Overview

This project implements object detection in dash camera footage with a focus on recognizing stop signs using the YOLO (You Only Look Once) model. When a stop sign is detected in the video feed, a buzzer sound is played. The project is designed as a graphical user interface (GUI) using Tkinter and OpenCV.

Table of Contents

- Prerequisites
- Installation
- Usage
- Functionality
- Team Members
- Code Structure
- Contributing
- Acknowledgments

Prerequisites

- Python 3
- OpenCV (`cv2`)
- pygame
- Tkinter
- PIL (Python Imaging Library)
- YOLO model files (`yolov3.weights`, `yolov3.cfg`, and `coco.names`)

Installation

1. Clone the repository:

```bash
git clone https://github.com/bhanuprasadthota/Stop-Sign-Detection-in-Dash-Camera-Footage.git
```

2. Install dependencies:

```bash
pip install opencv-python pygame Pillow
```

3. Download the YOLO model files (`yolov3.weights`, `yolov3.cfg`, and `coco.names`) and place them in the specified paths in the code.

Usage

Run the Python script `StopSignDetection.py`:

```bash
python stop_sign_detection.py
```

The GUI will appear, allowing you to input the path to dash camera footage. Click "Start Detection" to begin the object detection process. The program will identify stop signs and play a buzzer sound when detected.

Functionality

- Object detection using YOLO model
- Stop sign recognition
- Buzzer sound when a stop sign is detected
- GUI for user interaction

Team Members

- Bhanu Prasad Thota 
- Harshadeep Nallamothu 
- Parvash Choudhary Talluri 

Code Structure

- `StopSignDetection.py`: Main Python script containing the GUI and object detection logic.
- `alarm.mp3`: Buzzer sound file.
- `README.md`: Documentation file.

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

Acknowledgments

- YOLO: https://pjreddie.com/darknet/yolo/
- OpenCV: https://opencv.org/
- Tkinter: https://docs.python.org/3/library/tkinter.html
- pygame: https://www.pygame.org/
- PIL (Python Imaging Library): https://pillow.readthedocs.io/en/stable/


![image](https://github.com/bhanuprasadthota/Stop-Sign-Detection-in-Dash-Camera-Footage/assets/108273338/1f8358b4-73aa-4d35-8e2d-6656c96d0732)
