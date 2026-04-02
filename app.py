import streamlit as st
import pickle as pkl
import cv2
from PIL import Image
import numpy as np
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
import pandas as pd
import os
import sqlite3


# ---------------- DATABASE CONNECTION (SQLite) ----------------


conn = sqlite3.connect("forensics.db", check_same_thread=False)
cursor = conn.cursor()

# Create table automatically
cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT,
    prediction_result TEXT,
    confidence REAL,
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# ---------------- DELETE FUNCTION ----------------

def delete_record(record_id):

    cursor.execute(
        "DELETE FROM prediction WHERE id = ?",
        (record_id,)
    )

    conn.commit()

#  ----------------- Extract features ---------------

def extract_features(img_path):

    # Load Image in cv2:-
    img_pil = Image.open(img_path)
    img = np.array(img_pil)
    
    # convert into gray scale:-
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Feature 01:- LOCAL BINARY PATTERN(TEXTURE ANALYSIS)

    lbp = local_binary_pattern(gray,P=8,R=1,method='uniform')
    lbp_hist,_ = np.histogram(lbp.ravel(),bins=10,range=(0,10))
    lbp_hist = lbp_hist/np.sum(lbp_hist)

    #  Feature 02:-GRAY LEVEL CO-OCUURANCE MATRIX (TEXTURE STATISTICS)

    glcm = graycomatrix(gray,distances=[1],angles=[0],symmetric=True,normed=True,levels=256)
    contrast = graycoprops(glcm,'contrast')[0,0]
    homogeneity = graycoprops(glcm,'homogeneity')[0,0]
    energy = graycoprops(glcm,'energy')[0,0]
    correlation = graycoprops(glcm,'correlation')[0,0]

    # Feature 03:- EDGE FEATURE(BOUNDRY DETECTION)
    edge = cv2.Canny(gray,100,200)
    edge_density = np.sum(edge>0)/edge.size

    # Feature 04:-BLUR DETECTION
    blur = cv2.Laplacian(gray,cv2.CV_64F).var()

    # Feature 05 : METADATA
    try:
        img_pil = Image.open(img_path)
        has_exif = 1 if img_pil.getexif() else 0
    except:
        has_exif = 0

    features = np.hstack([lbp_hist, contrast, homogeneity, energy, 
                          correlation, edge_density, blur,has_exif])
    
    return features
# ---------------- LOAD MODEL ----------------

model = pkl.load(open("randomforest_model_01.pkl", "rb"))

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Digital Forensics Tampering Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- NAVIGATION ----------------

st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select a page",
    ["Home", "Detector", "Prediction History"]
)

# ---------------- HOME PAGE ----------------

def home():

    st.title("🕵️ Digital Forensics Tampering Detector")

    st.caption(
        "AI-Powered Image Forgery Detection Dashboard"
    )

    st.divider()

    st.subheader("📌 About This Application")

    st.write("""
    The **Digital Forensics Tampering Detector** is an intelligent web-based system designed
    to analyze digital images and detect possible manipulation or forgery using advanced
    **machine learning and computer vision techniques**.

    With the growing threat of **deepfakes, image fraud, and digital misinformation**, this
    application provides a **fast, reliable, and automated solution** for forensic image
    authentication and analysis.
    """)


# ---------------- DETECTOR PAGE ----------------

def detector():

    st.title("Main Dashboard")

    img = st.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg"]
    )

    if img is not None:

        features = extract_features(img)
        features = features.reshape(1, -1)

        st.image(img, use_container_width=True)

        # Prediction

        y_pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0]

        if y_pred == 1:

            label = "Authentic"
            confidence = prob[1] * 100

        else:

            label = "Tampered"
            confidence = prob[0] * 100

        st.divider()

        st.subheader("🔍 Forensic Analysis Result")

        col1, col2 = st.columns([1, 2])

        with col1:

            if label == "Authentic":
                st.success("✅ AUTHENTIC")
            else:
                st.error("⚠ TAMPERED")

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

            st.progress(confidence / 100)

        with col2:

            st.info(f"""
            Final Prediction: {label}
            Confidence: {confidence:.2f}%
            Risk Level: {"Low" if label=="Authentic" else "High"}
            """)

        # -------- SAVE RESULT --------

        if st.button("Save Result"):

            os.makedirs(
                "uploaded_images",
                exist_ok=True
            )

            img_path = os.path.join(
                "uploaded_images",
                img.name
            )

            with open(img_path, "wb") as f:

                f.write(img.getbuffer())

            query = """
            INSERT INTO prediction
            (image_name, prediction_result, confidence)
            VALUES (?,?,?)
            """

            cursor.execute(
                query,
                (img.name, label, confidence)
            )

            conn.commit()

            st.success("Result saved successfully")

# ---------------- HISTORY PAGE ----------------

def history():

    st.title("📊 Prediction History")

    query = """
    SELECT *
    FROM prediction
    ORDER BY prediction_time DESC
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:

        st.warning("No data found")

        return

    for index, row in df.iterrows():

        st.divider()

        col1, col2, col3 = st.columns(
            [1, 2, 0.5]
        )

        # -------- IMAGE --------

        with col1:

            image_path = os.path.join(
                "uploaded_images",
                row["image_name"]
            )

            if os.path.exists(image_path):

                image = Image.open(
                    image_path
                )

                st.image(
                    image,
                    use_container_width=True
                )

            else:

                st.warning("Image not found")

        # -------- DETAILS --------

        with col2:

            if row["prediction_result"] == "Authentic":

                st.success("✅ AUTHENTIC")

            else:

                st.error("⚠ TAMPERED")

            st.write(
                f"Image Name: {row['image_name']}"
            )

            st.write(
                f"Confidence: {row['confidence']:.2f}%"
            )

            st.write(
                f"Time: {row['prediction_time']}"
            )

        # -------- DELETE BUTTON --------

        with col3:

            if st.button(
                "🗑 Delete",
                key=f"delete_{row['id']}"
            ):

                image_path = os.path.join(
                    "uploaded_images",
                    row["image_name"]
                )

                if os.path.exists(image_path):
                    os.remove(image_path)

                delete_record(row["id"])

                st.success(
                    "Deleted successfully"
                )

                st.rerun()

# ---------------- PAGE ROUTING ----------------

if page == "Home":
    home()

elif page == "Detector":
    detector()

elif page == "Prediction History":
    history()
