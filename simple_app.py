"""
Simple Cattle/Buffalo Classification App
A lightweight version that works with basic dependencies
"""

import os
import cv2
import numpy as np
from pathlib import Path
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

class SimpleCattleClassifier:
    def __init__(self):
        self.data_dir = Path("train")
        self.images_dir = self.data_dir / "images"
        self.labels_dir = self.data_dir / "labels"
        self.model = None
        self.class_names = ['cow', 'buffalo']
        
    def extract_features(self, image_path):
        """Extract simple features from image"""
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return None
            
            # Resize to standard size
            img = cv2.resize(img, (64, 64))
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Extract simple features
            features = []
            
            # Histogram features
            hist = cv2.calcHist([gray], [0], None, [16], [0, 256])
            features.extend(hist.flatten())
            
            # Texture features (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            features.append(laplacian.var())
            
            # Color features (mean and std of RGB channels)
            for i in range(3):
                channel = img[:, :, i]
                features.extend([channel.mean(), channel.std()])
            
            return np.array(features)
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def load_data(self, max_samples=500):
        """Load and process data"""
        print("Loading data...")
        
        # Get all image files
        image_files = list(self.images_dir.glob("*.jpg"))
        
        # Limit samples for faster processing
        if len(image_files) > max_samples:
            image_files = random.sample(image_files, max_samples)
        
        print(f"Processing {len(image_files)} images...")
        
        features = []
        labels = []
        
        for img_path in image_files:
            # Find corresponding label
            label_path = self.labels_dir / (img_path.stem + ".txt")
            
            if not label_path.exists():
                continue
            
            # Read label (class 0 = cow, class 1 = buffalo)
            try:
                with open(label_path, 'r') as f:
                    line = f.readline().strip()
                    if line:
                        class_id = int(line.split()[0])
                        # Convert to binary: 0 = cow, 1 = buffalo
                        binary_label = class_id
                        
                        # Extract features
                        feature_vector = self.extract_features(img_path)
                        
                        if feature_vector is not None:
                            features.append(feature_vector)
                            labels.append(binary_label)
                            
            except Exception as e:
                print(f"Error reading label {label_path}: {e}")
                continue
        
        print(f"Extracted features from {len(features)} images")
        return np.array(features), np.array(labels)
    
    def train_model(self):
        """Train a simple Random Forest model"""
        print("Training model...")
        
        # Load data
        X, y = self.load_data(max_samples=300)  # Limit for speed
        
        if len(X) == 0:
            print("No data loaded!")
            return False
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.class_names))
        
        # Save model
        with open('simple_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        print("Model saved as 'simple_model.pkl'")
        return True
    
    def predict_image(self, image_path):
        """Predict class of a single image"""
        if self.model is None:
            print("Model not trained!")
            return None
        
        # Extract features
        features = self.extract_features(image_path)
        
        if features is None:
            return None
        
        # Make prediction
        features = features.reshape(1, -1)
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        
        return {
            'class': self.class_names[prediction],
            'confidence': max(probability),
            'probabilities': {
                'cow': probability[0],
                'buffalo': probability[1]
            }
        }
    
    def test_random_images(self, num_images=5):
        """Test the model on random images"""
        if self.model is None:
            print("Model not trained!")
            return
        
        print(f"Testing on {num_images} random images...")
        
        # Get random images
        image_files = list(self.images_dir.glob("*.jpg"))
        test_images = random.sample(image_files, min(num_images, len(image_files)))
        
        for img_path in test_images:
            print(f"\nImage: {img_path.name}")
            
            # Get true label
            label_path = self.labels_dir / (img_path.stem + ".txt")
            try:
                with open(label_path, 'r') as f:
                    line = f.readline().strip()
                    if line:
                        true_class = int(line.split()[0])
                        true_label = self.class_names[true_class]
            except:
                true_label = "Unknown"
            
            # Make prediction
            result = self.predict_image(img_path)
            
            if result:
                print(f"True: {true_label}")
                print(f"Predicted: {result['class']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Probabilities: Cow={result['probabilities']['cow']:.3f}, Buffalo={result['probabilities']['buffalo']:.3f}")
            else:
                print("Failed to process image")

def main():
    """Main function"""
    print("🐄 Simple Cattle/Buffalo Classifier")
    print("=" * 50)
    
    # Create classifier
    classifier = SimpleCattleClassifier()
    
    # Check if model exists
    if Path('simple_model.pkl').exists():
        print("Loading existing model...")
        with open('simple_model.pkl', 'rb') as f:
            classifier.model = pickle.load(f)
        print("Model loaded!")
    else:
        print("No existing model found. Training new model...")
        if not classifier.train_model():
            print("Training failed!")
            return
    
    # Test on random images
    classifier.test_random_images(num_images=10)
    
    print("\n" + "=" * 50)
    print("✅ App completed successfully!")
    print("\nTo test individual images, use:")
    print("result = classifier.predict_image('path/to/image.jpg')")

if __name__ == "__main__":
    main()
