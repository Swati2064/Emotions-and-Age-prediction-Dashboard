# 🧠 EmotionAI – Emotion & Age Detection Dashboard

An AI-powered web application that detects facial emotions and approximate age from uploaded images and provides emotion-based music recommendations.
---
## 🚀 Features

- 🔐 User Signup & Login
- 👤 Face Detection
- 🎂 Age Prediction
- 😊 Emotion Detection
- 🎵 Emotion-Based Music Recommendation
- 📊 Detection History
- 🖼️ Image Upload & Annotation
- 🗄️ SQLite Database
- 🌙 Modern Dashboard UI
---
## 🎭 Supported Emotions

😊 Happy | 😢 Sad | 😠 Angry | 😐 Neutral | 😨 Fear | 😲 Surprise | 🤢 Disgust
---
## 🛠️ Technologies Used

Python, Flask, OpenCV, DeepFace, Flask-SQLAlchemy, SQLite, NumPy, Pandas, Scikit-learn, Pillow, HTML, CSS, JavaScript, Bootstrap 5
--
## 📁 Project Structure

EmotionAI/
│
├── ai_models/
│   ├── age_detection.py
│   ├── emotion.py
│   └── face_detector.py
│
├── music/
│   └── recommendation.py
│
├── static/
│   ├── audio/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   └── signup.html
│
├── app.py
├── config.py
├── create_audio_samples.py
├── database.py
├── download_original_songs.py
├── models.py
├── requirements.txt
└── README.md

## ⚙️ Installation

1. Clone the repository:

git clone https://github.com/YOUR-USERNAME/EmotionAI.git

2. Open the project:

cd EmotionAI

3. Create virtual environment:

python -m venv venv

4. Activate virtual environment:

Windows:
venv\Scripts\activate

5. Install dependencies:

pip install -r requirements.txt

6. Run the application:

python app.py

Open your browser and visit:

http://127.0.0.1:5000

## 🔄 Working Flow

Upload Image
      ↓
Face Detection
      ↓
Age Prediction + Emotion Detection
      ↓
Display Results
      ↓
Save Detection History
      ↓
Recommend Music

## 🎯 Project Objective

The main objective of EmotionAI is to combine computer vision and deep learning to analyze facial expressions, estimate age, and provide personalized music recommendations according to the detected emotional state.

## 📸 Screenshot

<img width="1902" height="945" alt="Screenshot 2026-08-10 220215" src="https://github.com/user-attachments/assets/dc616aa5-f7e3-40e7-a395-b8aa236b328f" />


## 👩‍💻 Author

Swati Jadhav
B.Tech – Artificial Intelligence & Data Science



