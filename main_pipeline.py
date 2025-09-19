"""
Main Pipeline Script for Cattle/Buffalo Classification
Runs the complete pipeline from data preprocessing to model deployment
"""

import os
import sys
from pathlib import Path
import argparse
import time

def run_data_preprocessing():
    """Run data preprocessing"""
    print("=" * 60)
    print("STEP 1: DATA PREPROCESSING")
    print("=" * 60)
    
    try:
        from data_preprocessing import main as preprocess_main
        preprocess_main()
        print("✓ Data preprocessing completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Data preprocessing failed: {e}")
        return False

def run_model_training():
    """Run model training"""
    print("=" * 60)
    print("STEP 2: MODEL TRAINING")
    print("=" * 60)
    
    try:
        from model_training import main as train_main
        train_main()
        print("✓ Model training completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Model training failed: {e}")
        return False

def run_model_evaluation():
    """Run model evaluation"""
    print("=" * 60)
    print("STEP 3: MODEL EVALUATION")
    print("=" * 60)
    
    try:
        from model_evaluation import main as eval_main
        eval_main()
        print("✓ Model evaluation completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Model evaluation failed: {e}")
        return False

def run_tflite_conversion():
    """Run TFLite conversion"""
    print("=" * 60)
    print("STEP 4: TFLITE CONVERSION")
    print("=" * 60)
    
    try:
        from tflite_converter import main as tflite_main
        tflite_main()
        print("✓ TFLite conversion completed successfully!")
        return True
    except Exception as e:
        print(f"✗ TFLite conversion failed: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("=" * 60)
    print("CHECKING DEPENDENCIES")
    print("=" * 60)
    
    required_packages = [
        'tensorflow', 'opencv-python', 'pandas', 'numpy', 
        'matplotlib', 'seaborn', 'scikit-learn', 'albumentations'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies are installed!")
    return True

def check_data():
    """Check if training data exists"""
    print("=" * 60)
    print("CHECKING TRAINING DATA")
    print("=" * 60)
    
    data_dir = Path("train")
    images_dir = data_dir / "images"
    labels_dir = data_dir / "labels"
    
    if not data_dir.exists():
        print("✗ Training data directory 'train' not found!")
        return False
    
    if not images_dir.exists():
        print("✗ Images directory 'train/images' not found!")
        return False
    
    if not labels_dir.exists():
        print("✗ Labels directory 'train/labels' not found!")
        return False
    
    # Count files
    image_count = len(list(images_dir.glob("*.jpg")))
    label_count = len(list(labels_dir.glob("*.txt")))
    
    print(f"✓ Found {image_count} images")
    print(f"✓ Found {label_count} labels")
    
    if image_count == 0:
        print("✗ No images found in train/images!")
        return False
    
    if label_count == 0:
        print("✗ No labels found in train/labels!")
        return False
    
    print("✓ Training data is ready!")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "processed_data", "models", "evaluation_results", 
        "mobile_models", "notebooks", "scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✓ Created necessary directories")

def run_complete_pipeline():
    """Run the complete pipeline"""
    print("🚀 STARTING CATTLE/BUFFALO CLASSIFICATION PIPELINE")
    print("=" * 80)
    
    start_time = time.time()
    
    # Check prerequisites
    if not check_dependencies():
        return False
    
    if not check_data():
        return False
    
    create_directories()
    
    # Run pipeline steps
    steps = [
        ("Data Preprocessing", run_data_preprocessing),
        ("Model Training", run_model_training),
        ("Model Evaluation", run_model_evaluation),
        ("TFLite Conversion", run_tflite_conversion)
    ]
    
    results = []
    
    for step_name, step_function in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        success = step_function()
        results.append((step_name, success))
        
        if not success:
            print(f"\n❌ Pipeline failed at step: {step_name}")
            break
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 80)
    print("PIPELINE SUMMARY")
    print("=" * 80)
    
    for step_name, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{step_name:.<50} {status}")
    
    print(f"\nTotal execution time: {total_time/60:.2f} minutes")
    
    if all(success for _, success in results):
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("\nGenerated files:")
        print("- processed_data/: Preprocessed dataset")
        print("- models/: Trained models")
        print("- evaluation_results/: Evaluation metrics and visualizations")
        print("- mobile_models/: TFLite models for mobile deployment")
        
        print("\nNext steps:")
        print("1. Review evaluation results in evaluation_results/")
        print("2. Test mobile inference: python mobile_models/mobile_inference.py <image_path>")
        print("3. Deploy TFLite model to mobile app")
        
        return True
    else:
        print("\n❌ PIPELINE FAILED!")
        return False

def run_specific_step(step):
    """Run a specific pipeline step"""
    steps = {
        'preprocess': run_data_preprocessing,
        'train': run_model_training,
        'evaluate': run_model_evaluation,
        'convert': run_tflite_conversion
    }
    
    if step not in steps:
        print(f"Unknown step: {step}")
        print(f"Available steps: {', '.join(steps.keys())}")
        return False
    
    return steps[step]()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Cattle/Buffalo Classification Pipeline')
    parser.add_argument('--step', choices=['preprocess', 'train', 'evaluate', 'convert'],
                       help='Run specific step only')
    parser.add_argument('--check', action='store_true',
                       help='Check dependencies and data only')
    
    args = parser.parse_args()
    
    if args.check:
        check_dependencies()
        check_data()
        return
    
    if args.step:
        success = run_specific_step(args.step)
        sys.exit(0 if success else 1)
    else:
        success = run_complete_pipeline()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

