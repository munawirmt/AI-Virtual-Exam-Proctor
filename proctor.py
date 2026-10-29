import cv2
import numpy as np
import streamlit as st

# പേജിന്റെ ലേഔട്ട് സെറ്റ് ചെയ്യുന്നു
st.set_page_config(page_title="AI Exam Proctor", layout="wide")

# OpenCV-യുടെ സ്വന്തം ഡാറ്റാ പാത്തിൽ നിന്നും ഫയലുകൾ നേരിട്ട് ലോഡ് ചെയ്യുന്നു
# ഇത് ചെയ്യുന്നതിലൂടെ XML ഫയലുകൾ കാണാനില്ലെന്ന എറർ പൂർണ്ണമായും മാറും!
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

st.title("🎓 Smart AI Virtual Exam Proctoring System")
st.write("---")

# വെബ്‌സൈറ്റിനെ രണ്ട് കോളങ്ങളായി തിരിക്കുന്നു (ഇടതുവശത്ത് ചോദ്യങ്ങൾ, വലതുവശത്ത് ക്യാമറ)
col1, col2 = st.columns([2, 1.5])

with col1:
    st.subheader("📝 Online Examination Paper")
    st.info("⚠️ Note: AI is monitoring your integrity. Please allow camera access.")
    
    # മാതൃക ചോദ്യങ്ങൾ
    st.text_area("Question 1: Explain the difference between Supervised and Unsupervised Learning.", height=100)
    st.text_area("Question 2: Write a Python code snippet to reverse a string without using built-in functions.", height=100)
    if st.button("Submit Exam"):
        st.success("Exam submitted successfully!")

with col2:
    st.subheader("📹 Live AI Security Check")
    st.write("Click below to snap a photo and let AI check your presence:")
    
    # Streamlit Cloud-ൽ ക്യാമറ ഇൻപുട്ട് ടൂൾ
    img_file_buffer = st.camera_input("Verify your identity & screen presence")

    if img_file_buffer is not None:
        # ബഫറിൽ നിന്നുള്ള ചിത്രത്തെ OpenCV ഫോർമാറ്റിലേക്ക് മാറ്റുന്നു
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # പ്രോസസ്സിംഗ് വേഗത്തിലാക്കാൻ ഗ്രേസ്കെയിലിലേക്ക് മാറ്റുന്നു
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        
        # മുഖങ്ങൾ കണ്ടെത്തുന്നു
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            face_count = len(faces)
            
            # ഒന്നിൽ കൂടുതൽ ആളുകൾ ഉണ്ടോ എന്ന് നോക്കുന്നു
            if face_count > 1:
                st.error(f"🚨 WARNING: {face_count} People Detected in Frame!")
                for (x, y, w, h) in faces:
                    cv2.rectangle(cv2_img, (x, y), (x+w, y+h), (0, 0, 255), 3)
            else:
                st.success("Status: Normal (Face Detected)")
                
                for (x, y, w, h) in faces:
                    # മുഖത്തിന് ചുറ്റും പച്ച ബോക്സ്
                    cv2.rectangle(cv2_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = cv2_img[y:y+h, x:x+w]
                    
                    # കണ്ണുകൾ കണ്ടെത്തുന്നു
                    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
                    
                    # കണ്ണ് കാണുന്നില്ലെങ്കിൽ (മാറി നോക്കുകയോ അടയ്ക്കുകയോ ചെയ്താൽ)
                    if len(eyes) < 2:
                        st.warning("⚠️ WARNING: Look at the Screen! Eyes not focused.")
                    
                    # കണ്ണുകൾക്ക് ചുറ്റും ചെറിയ നീല ബോക്സ്
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
        else:
            st.error("🚨 WARNING: No Face Detected! Stay in front of the camera.")

        # ഫൈനൽ ഔട്ട്പുട്ട് ഇമേജ് വെബ്‌സൈറ്റിൽ കാണിക്കുന്നു
        st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB), caption="AI Real-time Analysis", use_container_width=True)
