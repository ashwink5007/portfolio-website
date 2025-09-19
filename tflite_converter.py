"""
TensorFlow Lite Conversion Script
Converts trained model to TFLite format for mobile deployment
"""

import tensorflow as tf
import numpy as np
from pathlib import Path
import os

class TFLiteConverter:
    def __init__(self, model_path="models/final_model.h5"):
        self.model_path = Path(model_path)
        self.output_dir = Path("mobile_models")
        self.output_dir.mkdir(exist_ok=True)
        
        # Load the trained model
        self.model = tf.keras.models.load_model(str(self.model_path))
        print(f"Loaded model from: {self.model_path}")
        print(f"Model input shape: {self.model.input_shape}")
        print(f"Model output shape: {self.model.output_shape}")
    
    def convert_to_tflite(self, optimization='DEFAULT'):
        """Convert model to TFLite format"""
        print(f"Converting model to TFLite with optimization: {optimization}")
        
        # Create TFLite converter
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        
        # Set optimization
        if optimization == 'DEFAULT':
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
        elif optimization == 'FULL_INTEGER':
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
            converter.inference_input_type = tf.int8
            converter.inference_output_type = tf.int8
        elif optimization == 'FLOAT16':
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_types = [tf.float16]
        
        # Convert model
        try:
            tflite_model = converter.convert()
            
            # Save model
            output_path = self.output_dir / f'model_{optimization.lower()}.tflite'
            with open(output_path, 'wb') as f:
                f.write(tflite_model)
            
            print(f"TFLite model saved to: {output_path}")
            print(f"Model size: {len(tflite_model) / 1024:.2f} KB")
            
            return tflite_model, output_path
            
        except Exception as e:
            print(f"Error converting model: {e}")
            return None, None
    
    def test_tflite_model(self, tflite_model):
        """Test TFLite model with sample input"""
        print("Testing TFLite model...")
        
        # Create interpreter
        interpreter = tf.lite.Interpreter(model_content=tflite_model)
        interpreter.allocate_tensors()
        
        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        print(f"Input shape: {input_details[0]['shape']}")
        print(f"Input type: {input_details[0]['dtype']}")
        print(f"Output shape: {output_details[0]['shape']}")
        print(f"Output type: {output_details[0]['dtype']}")
        
        # Test with random input
        input_shape = input_details[0]['shape']
        test_input = np.random.random_sample(input_shape).astype(input_details[0]['dtype'])
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], test_input)
        interpreter.invoke()
        
        # Get output
        output_data = interpreter.get_tensor(output_details[0]['index'])
        print(f"Test prediction: {output_data[0][0]:.4f}")
        
        return True
    
    def benchmark_model(self, tflite_model, num_runs=100):
        """Benchmark TFLite model performance"""
        print(f"Benchmarking TFLite model with {num_runs} runs...")
        
        # Create interpreter
        interpreter = tf.lite.Interpreter(model_content=tflite_model)
        interpreter.allocate_tensors()
        
        # Get input details
        input_details = interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        
        # Prepare test data
        test_input = np.random.random_sample(input_shape).astype(input_details[0]['dtype'])
        
        # Warm up
        for _ in range(10):
            interpreter.set_tensor(input_details[0]['index'], test_input)
            interpreter.invoke()
        
        # Benchmark
        import time
        times = []
        
        for _ in range(num_runs):
            start_time = time.time()
            interpreter.set_tensor(input_details[0]['index'], test_input)
            interpreter.invoke()
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        
        print(f"Average inference time: {avg_time*1000:.2f} ± {std_time*1000:.2f} ms")
        print(f"FPS: {1/avg_time:.2f}")
        
        return {
            'avg_time': avg_time,
            'std_time': std_time,
            'fps': 1/avg_time
        }
    
    def create_mobile_inference_script(self):
        """Create Python script for mobile inference"""
        script_content = '''"""
Mobile Inference Script for Cattle/Buffalo Classification
Usage: python mobile_inference.py <image_path>
"""

import tensorflow as tf
import numpy as np
import cv2
import sys
from pathlib import Path

class MobileCattleClassifier:
    def __init__(self, model_path="mobile_models/model_default.tflite"):
        self.model_path = model_path
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        print(f"Loaded TFLite model: {model_path}")
        print(f"Input shape: {self.input_details[0]['shape']}")
        print(f"Output shape: {self.output_details[0]['shape']}")
    
    def preprocess_image(self, image_path):
        """Preprocess image for inference"""
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size
        img = cv2.resize(img, (224, 224))
        
        # Normalize
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def predict(self, image_path):
        """Make prediction on image"""
        # Preprocess image
        input_data = self.preprocess_image(image_path)
        
        # Run inference
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        # Get output
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        probability = output_data[0][0]
        
        # Convert to class
        prediction = "buffalo" if probability > 0.5 else "cow"
        confidence = max(probability, 1 - probability)
        
        return prediction, confidence, probability
    
    def classify_image(self, image_path):
        """Classify image and return results"""
        try:
            prediction, confidence, probability = self.predict(image_path)
            
            result = {
                'image_path': image_path,
                'prediction': prediction,
                'confidence': confidence,
                'probability': probability,
                'is_buffalo': prediction == "buffalo"
            }
            
            return result
            
        except Exception as e:
            return {
                'image_path': image_path,
                'error': str(e)
            }

def main():
    if len(sys.argv) != 2:
        print("Usage: python mobile_inference.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not Path(image_path).exists():
        print(f"Image not found: {image_path}")
        sys.exit(1)
    
    # Create classifier
    classifier = MobileCattleClassifier()
    
    # Classify image
    result = classifier.classify_image(image_path)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\\nClassification Result:")
        print(f"Image: {result['image_path']}")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Probability: {result['probability']:.3f}")
        print(f"Is Buffalo: {result['is_buffalo']}")

if __name__ == "__main__":
    main()
'''
        
        script_path = self.output_dir / 'mobile_inference.py'
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"Mobile inference script saved to: {script_path}")
    
    def create_android_integration_guide(self):
        """Create Android integration guide"""
        guide_content = '''# Android Integration Guide

## Prerequisites
- Android Studio
- TensorFlow Lite Android library

## Setup

### 1. Add TensorFlow Lite dependency to build.gradle (app level)
```gradle
dependencies {
    implementation 'org.tensorflow:tensorflow-lite:2.13.0'
    implementation 'org.tensorflow:tensorflow-lite-support:0.4.4'
}
```

### 2. Add model to assets folder
- Copy `model_default.tflite` to `app/src/main/assets/`

### 3. Java/Kotlin Implementation
```java
import org.tensorflow.lite.Interpreter;
import java.nio.MappedByteBuffer;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class CattleClassifier {
    private Interpreter tflite;
    
    public CattleClassifier(AssetManager assets, String modelPath) throws IOException {
        MappedByteBuffer modelBuffer = loadModelFile(assets, modelPath);
        tflite = new Interpreter(modelBuffer);
    }
    
    public float[] classify(Bitmap bitmap) {
        // Preprocess bitmap to 224x224
        Bitmap resized = Bitmap.createScaledBitmap(bitmap, 224, 224, true);
        
        // Convert to ByteBuffer
        ByteBuffer inputBuffer = convertBitmapToByteBuffer(resized);
        
        // Run inference
        float[][] output = new float[1][1];
        tflite.run(inputBuffer, output);
        
        return output[0];
    }
    
    private MappedByteBuffer loadModelFile(AssetManager assets, String modelPath) throws IOException {
        AssetFileDescriptor fileDescriptor = assets.openFd(modelPath);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }
}
```

## Usage Example
```java
// Initialize classifier
CattleClassifier classifier = new CattleClassifier(getAssets(), "model_default.tflite");

// Classify image
float[] result = classifier.classify(bitmap);
float probability = result[0];
String prediction = probability > 0.5 ? "Buffalo" : "Cow";
```

## Performance Tips
- Use GPU delegate for faster inference
- Quantize model for smaller size
- Preprocess images efficiently
'''
        
        guide_path = self.output_dir / 'android_integration_guide.md'
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        print(f"Android integration guide saved to: {guide_path}")
    
    def convert_all_optimizations(self):
        """Convert model with all optimization levels"""
        print("Converting model with all optimization levels...")
        
        optimizations = ['DEFAULT', 'FLOAT16', 'FULL_INTEGER']
        results = {}
        
        for opt in optimizations:
            print(f"\n--- Converting with {opt} optimization ---")
            tflite_model, output_path = self.convert_to_tflite(opt)
            
            if tflite_model is not None:
                # Test model
                self.test_tflite_model(tflite_model)
                
                # Benchmark
                benchmark_results = self.benchmark_model(tflite_model)
                
                results[opt] = {
                    'model_path': output_path,
                    'size_kb': len(tflite_model) / 1024,
                    'benchmark': benchmark_results
                }
        
        # Create summary
        self.create_conversion_summary(results)
        
        return results
    
    def create_conversion_summary(self, results):
        """Create summary of all conversions"""
        summary_path = self.output_dir / 'conversion_summary.md'
        
        with open(summary_path, 'w') as f:
            f.write("# TFLite Model Conversion Summary\n\n")
            
            for opt, data in results.items():
                f.write(f"## {opt} Optimization\n")
                f.write(f"- Model size: {data['size_kb']:.2f} KB\n")
                f.write(f"- Average inference time: {data['benchmark']['avg_time']*1000:.2f} ms\n")
                f.write(f"- FPS: {data['benchmark']['fps']:.2f}\n")
                f.write(f"- File: `{data['model_path'].name}`\n\n")
            
            f.write("## Recommendations\n")
            f.write("- **DEFAULT**: Best balance of size and accuracy\n")
            f.write("- **FLOAT16**: Smaller size, slightly reduced accuracy\n")
            f.write("- **FULL_INTEGER**: Smallest size, requires quantization-aware training\n\n")
            
            f.write("## Mobile Deployment Files\n")
            f.write("- `mobile_inference.py`: Python inference script\n")
            f.write("- `android_integration_guide.md`: Android integration guide\n")
        
        print(f"Conversion summary saved to: {summary_path}")

def main():
    """Main function to run TFLite conversion"""
    print("Starting TFLite conversion...")
    
    # Create converter
    converter = TFLiteConverter()
    
    # Convert with all optimizations
    results = converter.convert_all_optimizations()
    
    # Create mobile inference script
    converter.create_mobile_inference_script()
    
    # Create Android integration guide
    converter.create_android_integration_guide()
    
    print(f"\nTFLite conversion completed!")
    print(f"Mobile models saved to: {converter.output_dir}")

if __name__ == "__main__":
    main()
