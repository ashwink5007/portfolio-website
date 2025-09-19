# 🐄 Cattle/Buffalo Breed Classification System

A complete machine learning pipeline for classifying cattle and buffalo breeds from images, optimized for mobile deployment using TensorFlow Lite.

## 🚀 Features

- **Automated Data Preprocessing**: Processes YOLO format annotations and crops animals from bounding boxes
- **Mobile-Optimized Training**: Uses MobileNetV2 for efficient mobile deployment
- **Comprehensive Evaluation**: Detailed metrics, confusion matrices, and failure case analysis
- **TFLite Conversion**: Multiple optimization levels for mobile deployment
- **Interactive Demo**: Streamlit web interface for testing
- **Android Integration**: Ready-to-use Android integration guide

## 📁 Project Structure

```
SIH/
├── train/                          # Original training data
│   ├── images/                     # 1,747 cow/buffalo images
│   └── labels/                     # YOLO format annotations
├── requirements.txt                # Python dependencies
├── data_preprocessing.py           # Data preprocessing script
├── model_training.py               # Model training script
├── model_evaluation.py             # Model evaluation script
├── tflite_converter.py             # TFLite conversion script
├── main_pipeline.py                # Complete pipeline runner
├── streamlit_app.py                # Interactive web demo
└── README.md                       # This file
```

## 🛠️ Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Quick Start

### Option 1: Run Complete Pipeline
```bash
python main_pipeline.py
```

### Option 2: Run Individual Steps
```bash
# Check dependencies and data
python main_pipeline.py --check

# Run specific step
python main_pipeline.py --step preprocess
python main_pipeline.py --step train
python main_pipeline.py --step evaluate
python main_pipeline.py --step convert
```

## 📊 Pipeline Steps

### 1. Data Preprocessing (`data_preprocessing.py`)
- Crops animals from YOLO bounding boxes
- Filters blurry and low-quality images
- Splits data into train/validation/test sets
- Creates balanced dataset with metadata

**Output**: `processed_data/` directory with organized images and CSV metadata

### 2. Model Training (`model_training.py`)
- Uses MobileNetV2 with transfer learning
- Implements data augmentation
- Fine-tuning with unfrozen layers
- Saves best model based on validation accuracy

**Output**: `models/final_model.h5`

### 3. Model Evaluation (`model_evaluation.py`)
- Comprehensive evaluation metrics
- Confusion matrix and ROC curve
- Failure case analysis
- Detailed classification report

**Output**: `evaluation_results/` directory with metrics and visualizations

### 4. TFLite Conversion (`tflite_converter.py`)
- Converts to multiple optimization levels:
  - DEFAULT: Balanced size and accuracy
  - FLOAT16: Smaller size, slight accuracy reduction
  - FULL_INTEGER: Smallest size (requires quantization-aware training)
- Performance benchmarking
- Mobile inference script generation

**Output**: `mobile_models/` directory with TFLite models and integration guides

## 🌐 Interactive Demo

Run the Streamlit web interface:

```bash
streamlit run streamlit_app.py
```

Features:
- Upload and classify images
- View model performance metrics
- Explore dataset statistics
- Interactive visualizations

## 📱 Mobile Deployment

### Python Inference
```bash
python mobile_models/mobile_inference.py <image_path>
```

### Android Integration
1. Follow the guide in `mobile_models/android_integration_guide.md`
2. Copy `model_default.tflite` to your Android app's assets folder
3. Use the provided Java/Kotlin code for inference

## 📈 Expected Performance

Based on the dataset characteristics:
- **Training Images**: ~1,400 (80% of 1,747)
- **Validation Images**: ~175 (10% of 1,747)
- **Test Images**: ~175 (10% of 1,747)
- **Target Accuracy**: 85%+ on binary classification (cow vs buffalo)

## 🔧 Customization

### Adding More Classes
To extend to breed classification:
1. Modify the data preprocessing to handle multiple breeds
2. Update the model architecture for multi-class classification
3. Adjust the loss function and metrics

### Improving Performance
1. **Data Augmentation**: Add more augmentation techniques
2. **Model Architecture**: Try EfficientNet or ResNet variants
3. **Ensemble Methods**: Combine multiple models
4. **Active Learning**: Add more labeled data based on failure cases

## 🐛 Troubleshooting

### Common Issues

1. **CUDA/GPU Issues**:
   ```bash
   # Force CPU usage
   export CUDA_VISIBLE_DEVICES=""
   ```

2. **Memory Issues**:
   - Reduce batch size in `model_training.py`
   - Use smaller image size (e.g., 128x128)

3. **Data Not Found**:
   - Ensure `train/images/` and `train/labels/` directories exist
   - Check that image and label filenames match

4. **Model Loading Errors**:
   - Ensure model training completed successfully
   - Check file paths in scripts

## 📋 Requirements

- Python 3.8+
- TensorFlow 2.15+
- OpenCV 4.8+
- 8GB+ RAM recommended
- GPU optional but recommended for faster training

## 🎯 SIH Hackathon Deliverables

This implementation provides:

1. ✅ **Complete ML Pipeline**: End-to-end solution from data to deployment
2. ✅ **Mobile Optimization**: TFLite models ready for mobile apps
3. ✅ **Reproducible Results**: All scripts and dependencies included
4. ✅ **Performance Metrics**: Comprehensive evaluation and reporting
5. ✅ **Interactive Demo**: Streamlit app for testing and demonstration
6. ✅ **Documentation**: Complete setup and usage instructions

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in the terminal output
3. Ensure all dependencies are properly installed

## 🏆 Next Steps

1. **Deploy to Production**: Use the TFLite models in a mobile app
2. **Expand Dataset**: Add more breeds and species
3. **Body Condition Scoring**: Extend to predict animal health metrics
4. **Real-time Detection**: Integrate with camera feeds for live classification

---

**Built for SIH 2024** 🚀

