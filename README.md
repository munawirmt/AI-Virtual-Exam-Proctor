# 🎓 Smart AI Virtual Exam Proctoring System

An advanced, lightweight, and end-to-end cloud-based web application built to automate online examination invigilation using Computer Vision and Machine Learning.

[![Streamlit App](https://streamlit.io)](https://ai-virtual-exam-proctor-mvyvk3ydzdvjhstfnm3gyj.streamlit.app/)

---

## 🚀 Live Demo

You can test the live working application directly in your browser without any installation:

[👉 Click Here to Launch Live AI Proctoring App](https://ai-virtual-exam-proctor-mvyvk3ydzdvjhstfnm3gyj.streamlit.app/)

---

## 🎯 Key Features

- **🧑‍💻 Real-time Face Tracking:** Detects the presence or absence of the examinee and triggers instant warnings if the student leaves the screen.
- **👥 Multi-Person Detection:** Identifies if more than one individual enters the camera frame to prevent collusion.
- **👁️ Gaze & Focus Monitoring (Eye Tracking):** Monitors eye presence and movement to detect if the student is continuously looking away from the screen to copy.
- **📝 Integrated Exam Portal:** A split-screen layout featuring the exam question paper on the left and the live AI security check on the right.

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 3.12+
- **Computer Vision:** OpenCV (Optimized Haar Cascade Classifiers for Low Latency)
- **Web Interface:** Streamlit Framework
- **Deployment:** Streamlit Cloud Architecture

---

## 📦 Local Installation & Setup

If you want to run this project on your local machine using **VS Code**, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd YOUR_REPO_NAME
   ```

2. **Install required dependencies:**
   ```bash
   pip install opencv-contrib-python-headless streamlit
   ```

3. **Run the application:**
   ```bash
   streamlit run proctor.py
   ```

---

## 💡 Why This Architecture?

Unlike heavy Deep Learning models (like YOLO or ResNet) which require expensive GPU servers, this system uses highly optimized **Haar Cascade Classifiers**. This allows the application to deliver **ultra-low latency performance** even on basic laptops and standard cloud servers, making online exams accessible to students with minimal hardware resources.
