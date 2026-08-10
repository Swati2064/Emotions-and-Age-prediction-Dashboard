# 🧠 EmotionAI Dashboard

An AI-powered **Emotion & Age Detection Platform** with mood-tailored **Spotify & YouTube Music Recommendations**, built with Python, Flask, OpenCV, DeepFace, SQLite, and Bootstrap 5.

---

## 🌟 Key Features

1. **User Authentication System**:
   - Secure Signup, Login, and Session Logout with password hashing (`werkzeug.security`).
2. **AI Face Detection**:
   - Multi-scale OpenCV Haar Cascade scanner detects facial geometry and overlays HUD bounding boxes with corner accents.
3. **AI Age Prediction**:
   - DeepFace deep learning neural network & computer vision texture analyzer.
4. **AI Emotion Classifier**:
   - Detects 7 core emotions: `Happy`, `Sad`, `Angry`, `Neutral`, `Fear`, `Surprise`, and `Disgust` along with confidence percentage metrics.
5. **Emotion-Driven Music Recommendation**:
   - Generates curated songs (Bollywood Motivational, Upbeat Pop, Calm Acoustics, Peaceful Ambient, Lo-Fi Chill) with direct quick-links to Spotify & YouTube.
6. **Detection History**:
   - Saves predictions per user in SQLite database for tracking previous uploads.
7. **Modern Dark SaaS UI**:
   - Built with Bootstrap 5, FontAwesome 6, CSS glassmorphism, file drag-and-drop zone, live image preview, and laser scanner loading overlay.

---

## 📁 Directory Structure & File Map

Create the project directory structure as follows:

```text
EmotionAI/
│
├── app.py                   # Main Flask server & REST API controller
├── config.py                # Database & Flask application configuration
├── database.py              # SQLAlchemy initialization & DB context helper
├── models.py                # User & DetectionHistory database models
├── requirements.txt         # Required Python packages specification
├── .env.example             # Environment variables template
├── README.md                # Full setup, run & deployment documentation
│
├── ai_models/               # Computer Vision & Deep Learning Package
│   ├── __init__.py
│   ├── face_detector.py     # OpenCV Haar Cascade & HUD bounding box drawer
│   ├── emotion.py           # DeepFace & ML emotion classifier
│   └── age_detection.py     # DeepFace & ML age predictor
│
├── music/                   # Music Recommendation Engine Package
│   ├── __init__.py
│   └── recommendation.py    # Curated Spotify & YouTube links by emotion
│
├── static/                  # Static Web Assets
│   ├── css/
│   │   └── style.css        # Custom Glassmorphism & SaaS Dark theme CSS
│   ├── js/
│   │   └── main.js          # File dropzone, AJAX AI API calls, dynamic rendering
│   └── uploads/             # Directory for saved raw & annotated images
│
└── templates/               # Jinja2 HTML Templates
    ├── base.html            # Core layout shell with head & script tags
    ├── index.html           # Landing page with hero & features
    ├── login.html           # User login page
    ├── signup.html          # Registration page
    └── dashboard.html       # AI Dashboard (Upload, Preview, Results, Songs, History)
```

---

## 🚀 Step-by-Step VS Code Setup & Run Instructions

### Step 1: Open Project in VS Code
Open VS Code and navigate to the project directory:
```bash
cd EmotionAI
```

### Step 2: Create Python Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Flask Server
```bash
python app.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🧪 How to Test Image Upload & AI Analysis

1. Open `http://127.0.0.1:5000` in your web browser.
2. Click **"Get Started Free"** or **"Signup"** and create a new user account.
3. Sign in to access the **AI Dashboard**.
4. Drag and drop any face photo (JPG or PNG) into **Card 1: Upload Image** or click to browse.
5. Watch the live image preview render in **Card 2**.
6. Click **"Run AI Analysis"**.
7. Observe:
   - Animated laser scanner line while model runs.
   - **Card 2**: Annotated output image with cyan HUD face bounding box and label badge.
   - **Card 3**: Face Detected status (`YES`), predicted age (e.g. `25 years`), detected emotion pill (e.g. `Happy`), and confidence score bar (`98%`).
   - **Card 4**: Emotion-matched song recommendation cards with clickable **Spotify** and **YouTube** buttons.
   - **Detection History Table**: Automatically updates with your prediction timestamp and thumbnail.

---

---

## 🛡️ License
This project is open-source and available under the MIT License.
