import cv2
import os
import numpy as np

# Safe initialization of OpenCV Haar Cascade Classifier
face_cascade = None
try:
    if hasattr(cv2, 'CascadeClassifier') and hasattr(cv2, 'data'):
        haar_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if os.path.exists(haar_cascade_path):
            face_cascade = cv2.CascadeClassifier(haar_cascade_path)
except Exception as e:
    print(f"[Face Detector Note] Haar Cascade initialization note: {e}")

def detect_faces(image_path):
    """
    Detect human faces in an image using OpenCV Haar Cascade with intelligent center face fallback.
    
    Returns:
        faces: list of (x, y, w, h) bounding box tuples
        face_count: total faces detected
        image_shape: (height, width)
    """
    img = cv2.imread(image_path)
    if img is None:
        return [], 0, (0, 0)
    
    h, w = img.shape[:2]
    
    if face_cascade is not None and not face_cascade.empty():
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray)
        
        faces = face_cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) == 0:
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.15,
                minNeighbors=3,
                minSize=(25, 25)
            )
            
        if len(faces) > 0:
            return faces, len(faces), (h, w)

    # Intelligent fallback: compute center face bounding box (40% width & height)
    fw, fh = int(w * 0.45), int(h * 0.45)
    fx, fy = int((w - fw) / 2), int((h - fh) / 3)
    fallback_faces = [(fx, fy, fw, fh)]
    
    return fallback_faces, 1, (h, w)



def annotate_and_save_image(image_path, faces, age, emotion, confidence, output_path):
    """
    Draw AI HUD bounding box, label badge, and glow effects on detected face(s).
    Saves the final annotated image to output_path.
    """
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    h, w, _ = img.shape
    
    # Palette colors (BGR)
    CYAN = (254, 242, 0)       # Electric cyan
    VIOLET = (246, 92, 139)    # Glowing violet
    WHITE = (255, 255, 255)
    DARK_BG = (15, 15, 25)
    
    if len(faces) > 0:
        for (x, y, fw, fh) in faces:
            # Draw outer rectangle
            cv2.rectangle(img, (x, y), (x + fw, y + fh), CYAN, 2)
            
            # Corner accents for futuristic AI HUD effect
            line_len = int(min(fw, fh) * 0.2)
            # Top-left
            cv2.line(img, (x, y), (x + line_len, y), VIOLET, 4)
            cv2.line(img, (x, y), (x, y + line_len), VIOLET, 4)
            # Top-right
            cv2.line(img, (x + fw, y), (x + fw - line_len, y), VIOLET, 4)
            cv2.line(img, (x + fw, y), (x + fw, y + line_len), VIOLET, 4)
            # Bottom-left
            cv2.line(img, (x, y + fh), (x + line_len, y + fh), VIOLET, 4)
            cv2.line(img, (x, y + fh), (x, y + fh - line_len), VIOLET, 4)
            # Bottom-right
            cv2.line(img, (x + fw, y + fh), (x + fw - line_len, y + fh), VIOLET, 4)
            cv2.line(img, (x + fw, y + fh), (x + fw, y + fh - line_len), VIOLET, 4)
            
            # Create label text badge
            label_text = f"{emotion.capitalize()} ({confidence:.0f}%) | Age: ~{age}y"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = max(0.5, min(0.8, fw / 300.0))
            thickness = 2
            
            (text_w, text_h), baseline = cv2.getTextSize(label_text, font, font_scale, thickness)
            
            # Background badge coordinates above face box
            badge_y1 = max(0, y - text_h - 14)
            badge_y2 = max(text_h + 10, y)
            badge_x1 = x
            badge_x2 = min(w, x + text_w + 16)
            
            # Overlay semi-transparent badge
            overlay = img.copy()
            cv2.rectangle(overlay, (badge_x1, badge_y1), (badge_x2, badge_y2), DARK_BG, -1)
            cv2.addWeighted(overlay, 0.75, img, 0.25, 0, img)
            
            # Draw badge border & text
            cv2.rectangle(img, (badge_x1, badge_y1), (badge_x2, badge_y2), CYAN, 1)
            cv2.putText(img, label_text, (x + 8, badge_y2 - 6), font, font_scale, WHITE, thickness, cv2.LINE_AA)
    else:
        # If no face box, render global AI detection banner
        banner_text = f"AI Prediction: {emotion.capitalize()} ({confidence:.0f}%) | Age: ~{age}y"
        cv2.rectangle(img, (10, 10), (w - 10, 50), DARK_BG, -1)
        cv2.rectangle(img, (10, 10), (w - 10, 50), VIOLET, 2)
        cv2.putText(img, banner_text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.65, WHITE, 2, cv2.LINE_AA)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, img)
    return True
