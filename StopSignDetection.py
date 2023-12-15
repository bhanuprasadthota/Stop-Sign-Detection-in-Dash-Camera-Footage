#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 04:38:39 2023

@author: bhanuprasadthota
"""

import cv2
import numpy as np
import pygame
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import webbrowser

# Initialize pygame mixer
pygame.mixer.init()

# Load YOLO
net = cv2.dnn.readNet('/Users/bhanuprasadthota/Downloads/yolov3.weights', '/Users/bhanuprasadthota/Downloads/yolov3.cfg')

# Load COCO class labels
classes = []
with open('/Users/bhanuprasadthota/Downloads/coco.names', 'r') as f:
    classes = f.read().strip().split('\n')

# Create the main Tkinter window
root = tk.Tk()
root.title("STOP SIGN DETECTION PROJECT")

# Heading for the project title
title_label = ttk.Label(root, text="CIS 530 PROJECT - STOP SIGN DETECTION IN DASH CAMERA FOOTAGE", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Variables
cap = None
buzzer_sound = pygame.mixer.Sound('/Users/bhanuprasadthota/Downloads/alarm.mp3')  

# Create frames for original and stop sign footage
original_frame = ttk.Frame(root)
original_frame.grid(row=1, column=0, padx=10, pady=10)

stop_sign_frame = ttk.Frame(root)
stop_sign_frame.grid(row=1, column=1, padx=10, pady=10)

# Label for original footage
original_label = ttk.Label(original_frame, text="Original Footage")
original_label.pack()

# Canvas for original footage
original_canvas = tk.Canvas(original_frame, width=640, height=480)
original_canvas.pack()

# Label for stop sign footage
stop_sign_label = ttk.Label(stop_sign_frame, text="Stop Sign detected Footage")
stop_sign_label.pack()

# Canvas for stop sign footage
stop_sign_canvas = tk.Canvas(stop_sign_frame, width=640, height=480)
stop_sign_canvas.pack()

# Label for description
description_label = ttk.Label(root, text="Object Detection with Stop Sign Recognition:\n\nThis program uses YOLO model to identify objects in dash cam video footage. "
                                         "It detects stop signs in the video feed and plays a buzzer sound when detected. \n"
                                         "The focus is on recognizing stop signs, with the added feature of playing a buzzer sound when a stop sign is detected.")
description_label.grid(row=2, column=0, columnspan=2, pady=10)

# Entry widget to get the video path
video_path_var = tk.StringVar()
video_path_label = ttk.Label(root, text="Enter Dash Cam Footage Path:")
video_path_label.grid(row=3, column=0, pady=5)
video_path_entry = ttk.Entry(root, textvariable=video_path_var, width=70)
video_path_entry.grid(row=3, column=1, pady=3)

# Label for messages
message_label = ttk.Label(root, text="")
message_label.grid(row=4, column=0, columnspan=2, pady=5)

# Context menu for the entry widget
entry_menu = tk.Menu(root, tearoff=0)
entry_menu.add_command(label="Cut")
entry_menu.add_command(label="Copy")
entry_menu.add_command(label="Paste", command=lambda: video_path_entry.event_generate('<<Paste>>'))
entry_menu.add_command(label="Select All", command=lambda: video_path_entry.select_range(0, tk.END))
video_path_entry.bind("<Button-3>", lambda e: entry_menu.post(e.x_root, e.y_root))

# Button to start sign detection
def start_detection():
    global cap
    video_path = video_path_var.get()

    if video_path:
        cap = cv2.VideoCapture(video_path)
        update_frames()
        # Clear any previous message
        message_label.config(text="")
    else:
        # Display a message if the video path is not provided
        message_label.config(text="Please enter the dash cam footage path.")

start_button = ttk.Button(root, text="Start Detection", command=start_detection)
start_button.grid(row=5, column=0, pady=10)

# Button to stop detection
def stop_detection():
    global cap
    if cap is not None:
        cap.release()

stop_button = ttk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.grid(row=5, column=1, pady=10)

# Button to open GitHub repository
def open_github():
    webbrowser.open_new("https://github.com/bhanuprasadthota/Stop-Sign-Detection-in-Dash-Camera-Footage.git")  

github_button = ttk.Button(root, text="View Code on GitHub", command=open_github)
github_button.grid(row=6, column=0, columnspan=2, pady=10)

# Team members section
team_label = ttk.Label(root, text="Team Members:")
team_label.grid(row=7, column=0, columnspan=2, pady=6)

# Team members' names
team_members_label = ttk.Label(root, text="Bhanu Prasad Thota(02049790)\nHarshadeep Nallamothu(02079359)\nParvash Choudhary Talluri(02078151)")
team_members_label.grid(row=8, column=0, columnspan=2, pady=5)

# Function to update frames
def update_frames():
    ret, frame = cap.read()

    if ret:
        # Detecting objects in the frame
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(net.getUnconnectedOutLayersNames())

        # Processing detected objects
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:  # You can adjust this threshold
                    # Object detected
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    w = int(detection[2] * frame.shape[1])
                    h = int(detection[3] * frame.shape[0])

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Non-maximum suppression to eliminate duplicate detections
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Update original footage canvas
        original_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_img = Image.fromarray(original_img)
        original_img = ImageTk.PhotoImage(original_img)
        original_canvas.create_image(0, 0, anchor=tk.NW, image=original_img)
        original_canvas.image = original_img

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])

                if label == 'stop sign':
                    # Play buzzer sound
                    buzzer_sound.play()

                    # Draw rectangle and label on the original frame
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Update stop sign footage canvas
        stop_sign_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stop_sign_img = Image.fromarray(stop_sign_img)
        stop_sign_img = ImageTk.PhotoImage(stop_sign_img)
        stop_sign_canvas.create_image(0, 0, anchor=tk.NW, image=stop_sign_img)
        stop_sign_canvas.image = stop_sign_img

        # Schedule the function to be called after a delay
        root.after(10, update_frames)
    else:
        # Release the video capture when the video ends
        cap.release()

# Run the Tkinter event loop
root.mainloop()
