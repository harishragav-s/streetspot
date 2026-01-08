# STREETSPOT  
## Smart Street Parking Management System using Machine Learning and Computer Vision

## Overview
STREETSPOT is a smart street parking management system that automatically detects empty and occupied parking slots from images and video feeds. The system combines computer vision techniques with machine learning models to provide real time parking availability information, reducing manual monitoring and improving urban traffic management.

The project is designed as a practical prototype for smart city applications where efficient parking utilization is critical.

---

## Key Features
- Automatic detection of parking slot occupancy  
- Real time video processing using OpenCV  
- Green bounding boxes for empty slots and red for occupied slots  
- Machine learning based parking slot classification  
- Mask based parking slot localization  
- User authentication using SQLite and Flask  

---

## Tech Stack
- **Programming Language:** Python  
- **Computer Vision:** OpenCV  
- **Machine Learning:** Scikit learn, TensorFlow, Keras  
- **Web Framework:** Flask  
- **Database:** SQLite  
- **Version Control:** Git, GitHub  

---

## Dataset Details
- **Total images:** 843  
- **Training images:** 743  
- **Validation images:** 100  
- **Classes:** Empty, Not Empty  
- **Train to validation split:** ~7:1  

The dataset consists of labeled parking slot images used to train and evaluate the classification models.

---
## Model Performance
- **CNN training accuracy:** **98.80%**  
- **CNN validation accuracy:** ~65–70%  
- The difference between training and validation accuracy is due to limited dataset size and model complexity.  
- The deployed application uses a lightweight classical machine learning model for faster real time inference.

---
## Parking Slot Detection Workflow
1. A binary mask image is used to identify parking slot regions  
2. OpenCV connected component analysis extracts slot bounding boxes  
3. Each slot region is cropped from the video frame  
4. The ML model classifies the slot as empty or occupied  
5. Green or red bounding boxes are drawn on the video frame  
6. The total number of available slots is displayed in real time  

---

## System Architecture
<img width="682" height="558" alt="System Architecture" src="https://github.com/user-attachments/assets/714a3e3f-1dfe-4979-9076-bebd77e54844" />

---

## Output Screenshots
<img width="1920" height="1080" alt="Output Screenshot 1" src="https://github.com/user-attachments/assets/67defb41-ecf0-43f2-96b1-834917516493" />

<img width="1920" height="1080" alt="Output Screenshot 2" src="https://github.com/user-attachments/assets/0813d6a5-73b1-40c0-b99b-220869bd07c3" />

---

