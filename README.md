# Digital Forensics Tampering Detector

## Project Title

**Digital Forensics Image Tampering Detection System using Machine Learning**

---

## Project Description

The **Digital Forensics Tampering Detector** is a web-based application developed using **Machine Learning**, **Computer Vision**, and **Streamlit**. The system analyzes digital images to detect whether they are **Authentic** or **Tampered**.

With the increasing threat of image manipulation, deepfakes, and digital fraud, this project provides an automated solution for forensic image verification. The application extracts image features and uses a trained **Random Forest classifier** to make predictions with confidence scores.

All prediction results are stored in a local **SQLite database**, and users can view or delete previous prediction history directly from the dashboard.

---

## Objectives

- Detect image tampering using machine learning
- Extract forensic features from images
- Provide prediction results with confidence scores
- Store prediction history in a database
- Build an interactive web dashboard using Streamlit

---

## Technologies Used

- Python
- Streamlit
- Machine Learning (Random Forest)
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- Scikit-image
- Pillow (PIL)
- SQLite Database

---

## Machine Learning Workflow

1. Data Collection
2. Data Preprocessing
3. Feature Extraction
4. Model Training
5. Model Evaluation
6. Deployment using Streamlit
7. Database Integration using SQLite

---

## Feature Extraction Techniques

The system uses the following image processing techniques:

- Local Binary Pattern (LBP)
- Gray Level Co-occurrence Matrix (GLCM)
- Texture Feature Analysis

These features help identify inconsistencies in image textures that indicate tampering.

---

## System Features

- Upload image for analysis
- Detect whether image is Authentic or Tampered
- Display prediction confidence score
- Save prediction results
- View prediction history
- Delete records from history
- Automatic database creation
- User-friendly Streamlit interface

##

## Installation Instructions

Follow these steps to run the project on your system:

### Step 1: Install Python

Install Python 3.9 or later.

### Step 2: Install Required Libraries

Run the following command in the terminal:

```
pip install -r requirements.txt
```

### Step 3: Run the Application

```
streamlit run app.py
```

The application will open automatically in your web browser.

---

## Database Information

- Database Type: SQLite
- Database File: `forensics.db`
- Table Name: `prediction`

The database is created automatically when the application runs. No manual setup is required.

---

## Output Example

The system provides:

- Prediction Result (Authentic or Tampered)
- Confidence Percentage
- Prediction Time
- Saved Image Record

---

## Use Cases

- Digital Forensics Investigation
- Cybersecurity Analysis
- Image Verification
- Academic Research Projects
- Fraud Detection Systems

---

## Future Enhancements

- Support for video tampering detection
- Deep learning model integration
- Cloud deployment
- User authentication system
- Real-time analysis

---

## Author

**Student Name:** Vansh Prajapati

**Course:** .B.Tech\
**Project Title:** Digital Forensics Tampering Detector\
**Year:** 2026

---

## Note

This project is developed for academic and educational purposes in the field of **Digital Forensics and Machine Learning**.

