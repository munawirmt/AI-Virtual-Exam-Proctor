import cv2
import numpy as np
import streamlit as st
import os

# പേജിന്റെ ലേഔട്ട് സെറ്റ് ചെയ്യുന്നു
st.set_page_config(page_title="AI Exam Proctor", layout="wide")

# കറന്റ് ഫോൾഡറിലെ XML ഫയലുകളുടെ കൃത്യമായ പാത്ത് കണ്ടുപിടിക്കുന്നു
current_dir = os.path.dirname(os.path.abspath(__file__))
face_path = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')
eye_path = os.path.join(current_dir, 'haarcascade_eye.xml')

# ഗിറ്റ്‌ഹബ്ബിൽ അപ്‌ലോഡ് ചെയ്ത ഫയലുകൾ നേരിട്ട് ലോഡ് ചെയ്യുന്നു
face_cascade = cv2.CascadeClassifier(face_path)
eye_cascade = cv2.CascadeClassifier(eye_path)

st.title("🎓 Smart AI Virtual Exam Proctoring System")
st.write("---")

col1, col2 = st.columns([2, 1.5])

with col1:
    st.subheader("📝 Online Examination Paper")
    st.info("⚠️ Note: AI is monitoring your integrity. Please allow camera access.")
    st.text_area("Question 1: Explain the difference between Supervised and Unsupervised Learning.", height=100)
    st.text_area("Question 2: Write a Python code snippet to reverse a string without using built-in functions.", height=100)
    if st.button("Submit Exam"):
        st.success("Exam submitted successfully!")

with col2:
    st.subheader("📹 Live AI Security Check")
    st.write("Click below to snap a photo and let AI check your presence:")
    
    img_file_buffer = st.camera_input("Verify your identity & screen presence")

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        
        # ഫയലുകൾ ശരിയായി ലോഡ് ആയിട്ടുണ്ടെന്ന് ഉറപ്പുവരുത്തുന്നു
        if face_cascade.empty() or face_cascade is None:
            st.error("Error: Face detection file missing or corrupted in GitHub repo!")
        else:
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                face_count = len(faces)
                if face_count > 1:
                    st.error(f"🚨 WARNING: {face_count} People Detected in Frame!")
                    for (x, y, w, h) in faces:
                        cv2.rectangle(cv2_img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                else:
                    st.success("Status: Normal (Face Detected)")
                    for (x, y, w, h) in faces:
                        cv2.rectangle(cv2_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # കണ്ണ് കണ്ടെത്തൽ
                        if not eye_cascade.empty() and eye_cascade is not None:
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = cv2_img[y:y+h, x:x+w]
                            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
                            if len(eyes) < 2:
                                st.warning("⚠️ WARNING: Look at the Screen! Eyes not focused.")
                            for (ex, ey, ew, eh) in eyes:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            else:
                st.error("🚨 WARNING: No Face Detected! Stay in front of the camera.")

        st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB), caption="AI Real-time Analysis", use_container_width=True)
