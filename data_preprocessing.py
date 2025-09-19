"""
Data Preprocessing Script for Cattle/Buffalo Classification
Processes YOLO format data and prepares it for training
"""

import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import shutil
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

class DataPreprocessor:
    def __init__(self, data_dir="train"):
        self.data_dir = Path(data_dir)
        self.images_dir = self.data_dir / "images"
        self.labels_dir = self.data_dir / "labels"
        self.output_dir = Path("processed_data")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create output directories
        for split in ['train', 'val', 'test']:
            for class_name in ['cow', 'buffalo']:
                (self.output_dir / split / class_name).mkdir(parents=True, exist_ok=True)
    
    def is_blurry(self, img_path, threshold=100):
        """Check if image is blurry using Laplacian variance"""
        try:
            img = cv2.imread(str(img_path))
            if img is None:
                return True
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            return laplacian_var < threshold
        except:
            return True
    
    def crop_animal_from_bbox(self, img_path, label_path):
        """Crop animal from image using bounding box"""
        try:
            img = cv2.imread(str(img_path))
            if img is None:
                return None
                
            h, w = img.shape[:2]
            
            # Read YOLO format label
            if not label_path.exists():
                return None
                
            with open(label_path, 'r') as f:
                lines = f.readlines()
            
            if not lines:
                return None
                
            # Get first bounding box (class 0 = cow, class 1 = buffalo)
            line = lines[0].strip().split()
            if len(line) < 5:
                return None
                
            class_id = int(line[0])
            x_center, y_center, width, height = map(float, line[1:5])
            
            # Convert YOLO format to pixel coordinates
            x_center *= w
            y_center *= h
            width *= w
            height *= h
            
            x_min = int(x_center - width/2)
            y_min = int(y_center - height/2)
            x_max = int(x_center + width/2)
            y_max = int(y_center + height/2)
            
            # Ensure coordinates are within image bounds
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(w, x_max)
            y_max = min(h, y_max)
            
            # Crop the animal
            cropped = img[y_min:y_max, x_min:x_max]
            
            if cropped.size == 0:
                return None
                
            # Resize to standard size
            cropped = cv2.resize(cropped, (224, 224))
            
            return cropped, class_id
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            return None
    
    def process_images(self):
        """Process all images and create dataset"""
        print("Processing images...")
        
        # Get all image files
        image_files = list(self.images_dir.glob("*.jpg"))
        print(f"Found {len(image_files)} images")
        
        processed_data = []
        rejected_count = 0
        
        for img_path in tqdm(image_files, desc="Processing images"):
            # Find corresponding label file
            label_path = self.labels_dir / (img_path.stem + ".txt")
            
            if not label_path.exists():
                rejected_count += 1
                continue
            
            # Check image quality
            if self.is_blurry(img_path):
                rejected_count += 1
                continue
            
            # Crop animal from bounding box
            result = self.crop_animal_from_bbox(img_path, label_path)
            if result is None:
                rejected_count += 1
                continue
                
            cropped_img, class_id = result
            
            # Determine class name
            class_name = "buffalo" if class_id == 1 else "cow"
            
            # Save cropped image
            output_path = self.output_dir / "raw" / class_name / f"{img_path.stem}.jpg"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(output_path), cropped_img)
            
            processed_data.append({
                'image_path': str(output_path),
                'class_name': class_name,
                'class_id': class_id,
                'original_path': str(img_path)
            })
        
        print(f"Processed {len(processed_data)} images, rejected {rejected_count}")
        
        # Create DataFrame
        df = pd.DataFrame(processed_data)
        
        # Split data
        train_df, temp_df = train_test_split(df, test_size=0.3, stratify=df['class_name'], random_state=42)
        val_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df['class_name'], random_state=42)
        
        # Move files to appropriate splits
        for split, split_df in [('train', train_df), ('val', val_df), ('test', test_df)]:
            for _, row in split_df.iterrows():
                src_path = Path(row['image_path'])
                dst_path = self.output_dir / split / row['class_name'] / src_path.name
                shutil.move(str(src_path), str(dst_path))
        
        # Save metadata
        df.to_csv(self.output_dir / 'metadata.csv', index=False)
        train_df.to_csv(self.output_dir / 'train_metadata.csv', index=False)
        val_df.to_csv(self.output_dir / 'val_metadata.csv', index=False)
        test_df.to_csv(self.output_dir / 'test_metadata.csv', index=False)
        
        print(f"Data split completed:")
        print(f"Train: {len(train_df)} images")
        print(f"Validation: {len(val_df)} images")
        print(f"Test: {len(test_df)} images")
        
        # Show class distribution
        self.show_class_distribution(train_df, val_df, test_df)
        
        return train_df, val_df, test_df
    
    def show_class_distribution(self, train_df, val_df, test_df):
        """Show class distribution across splits"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        for i, (df, title) in enumerate([(train_df, 'Train'), (val_df, 'Validation'), (test_df, 'Test')]):
            class_counts = df['class_name'].value_counts()
            axes[i].pie(class_counts.values, labels=class_counts.index, autopct='%1.1f%%')
            axes[i].set_title(f'{title} Distribution\n({len(df)} images)')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'class_distribution.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("\nClass Distribution:")
        for df, title in [(train_df, 'Train'), (val_df, 'Validation'), (test_df, 'Test')]:
            print(f"\n{title}:")
            print(df['class_name'].value_counts())

def main():
    """Main function to run data preprocessing"""
    print("Starting data preprocessing...")
    
    preprocessor = DataPreprocessor()
    train_df, val_df, test_df = preprocessor.process_images()
    
    print("\nData preprocessing completed successfully!")
    print(f"Processed data saved to: {preprocessor.output_dir}")

if __name__ == "__main__":
    main()

