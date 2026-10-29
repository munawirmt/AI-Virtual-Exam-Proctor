import cv2
import numpy as np
import streamlit as st
import os

# പേജിന്റെ ലേഔട്ട് സെറ്റ് ചെയ്യുന്നു
st.set_page_config(page_title="AI Exam Proctor", layout="wide")

# കോഡിനുള്ളിൽ നേരിട്ട് XML ഫയലുകൾ ഉണ്ടാക്കാനുള്ള ട്രിക്ക്
@st.cache_resource
def setup_xml_files():
    # 1. ഫേസ് ഡിറ്റക്ഷൻ ഡാറ്റ (ക്ലൗഡിൽ തനിയെ ഫയൽ ഉണ്ടാക്കും)
    if not os.path.exists("face.xml"):
        # വിപണിയിൽ ലഭ്യമായ ഏറ്റവും വേഗതയേറിയ കോൺഫിഗറേഷൻ ബിൽറ്റ്-ഇൻ ഡാറ്റ
        with open("face.xml", "w") as f:
            f.write('<?xml version="1.0"?><opencv_storage><haarcascade_frontalface_default type_id="opencv-haar-classifier">')
            # ബാക്കി പ്രധാന കോൺഫിഗറേഷനുകൾ റൺ ടൈമിൽ ലോഡ് ചെയ്യാൻ ഒഫീഷ്യൽ സിസ്റ്റം പാത്ത് ഉപയോഗിക്കാം
            
    # സെർവറിലെ തകരാറുകൾ പൂർണ്ണമായി ഒഴിവാക്കാൻ OpenCV-യുടെ ഇൻ-ബിൽറ്റ് ഡാറ്റ ലോഡ് ചെയ്യുന്നു
    try:
        face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        # ചില സെർവറുകളിൽ പാത്ത് മാറിയാൽ ഉള്ള ബാക്കപ്പ്
        if face.empty():
            face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        return face, eye
    except:
        # ലോക്കൽ ഡൗൺലോഡ് ബാക്കപ്പ്
        return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'), cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# മോഡലുകൾ ലോഡ് ചെയ്യുന്നു
face_cascade, eye_cascade = setup_xml_files()

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
        
        # എറർ വരാതിരിക്കാൻ ഡിറ്റക്ഷൻ സിസ്റ്റം സുരക്ഷിതമായി റൺ ചെയ്യുന്നു
        if not face_cascade.empty():
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
                        
                        # കണ്ണുകൾ കണ്ടെത്തുന്നു
                        if not eye_cascade.empty():
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = cv2_img[y:y+h, x:x+w]
                            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
                            if len(eyes) < 2:
                                st.warning("⚠️ WARNING: Look at the Screen! Eyes not focused.")
                            for (ex, ey, ew, eh) in eyes:
                                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            else:
                st.error("🚨 WARNING: No Face Detected! Stay in front of the camera.")
        else:
            st.warning("AI Engine is booting up. Please snap the photo again in 5 seconds!")

        st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB), caption="AI Real-time Analysis", use_container_width=True)
