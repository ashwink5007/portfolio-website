"""
Model Evaluation Script for Cattle/Buffalo Classification
Provides detailed evaluation metrics and failure case analysis
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from pathlib import Path
import pandas as pd
import cv2
from tensorflow.keras.preprocessing import image
import os

class ModelEvaluator:
    def __init__(self, model_path="models/final_model.h5", data_dir="processed_data"):
        self.model_path = Path(model_path)
        self.data_dir = Path(data_dir)
        self.results_dir = Path("evaluation_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Load model
        self.model = tf.keras.models.load_model(str(self.model_path))
        
        # Load test data
        self.setup_test_data()
    
    def setup_test_data(self):
        """Setup test data generator"""
        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        self.test_generator = test_datagen.flow_from_directory(
            self.data_dir / 'test',
            target_size=(224, 224),
            batch_size=32,
            class_mode='binary',
            shuffle=False
        )
        
        self.class_names = list(self.test_generator.class_indices.keys())
        print(f"Test classes: {self.class_names}")
        print(f"Test samples: {self.test_generator.samples}")
    
    def evaluate_model(self):
        """Comprehensive model evaluation"""
        print("Evaluating model...")
        
        # Get predictions
        predictions = self.model.predict(self.test_generator)
        y_pred = (predictions > 0.5).astype(int).flatten()
        y_true = self.test_generator.classes
        
        # Calculate metrics
        test_loss, test_accuracy = self.model.evaluate(self.test_generator, verbose=0)
        
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Test Loss: {test_loss:.4f}")
        
        # Generate classification report
        report = classification_report(
            y_true, y_pred, 
            target_names=self.class_names,
            output_dict=True
        )
        
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, target_names=self.class_names))
        
        # Save results
        self.save_evaluation_results(test_accuracy, test_loss, report, y_true, y_pred, predictions)
        
        return {
            'accuracy': test_accuracy,
            'loss': test_loss,
            'predictions': predictions,
            'y_true': y_true,
            'y_pred': y_pred,
            'report': report
        }
    
    def save_evaluation_results(self, accuracy, loss, report, y_true, y_pred, predictions):
        """Save evaluation results to files"""
        # Save metrics to CSV
        metrics_df = pd.DataFrame({
            'Metric': ['Accuracy', 'Loss'],
            'Value': [accuracy, loss]
        })
        metrics_df.to_csv(self.results_dir / 'metrics.csv', index=False)
        
        # Save detailed report
        report_df = pd.DataFrame(report).transpose()
        report_df.to_csv(self.results_dir / 'classification_report.csv')
        
        # Save predictions
        pred_df = pd.DataFrame({
            'True_Label': y_true,
            'Predicted_Label': y_pred,
            'Prediction_Probability': predictions.flatten()
        })
        pred_df.to_csv(self.results_dir / 'predictions.csv', index=False)
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """Plot and save confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.class_names,
                   yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig(self.results_dir / 'confusion_matrix.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        return cm
    
    def plot_roc_curve(self, y_true, predictions):
        """Plot ROC curve"""
        fpr, tpr, _ = roc_curve(y_true, predictions)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(self.results_dir / 'roc_curve.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        return roc_auc
    
    def analyze_failure_cases(self, y_true, y_pred, predictions, top_n=20):
        """Analyze failure cases and save images"""
        print("Analyzing failure cases...")
        
        # Find misclassified samples
        misclassified_indices = np.where(y_true != y_pred)[0]
        
        # Sort by confidence (most confident wrong predictions)
        misclassified_probs = predictions[misclassified_indices].flatten()
        sorted_indices = np.argsort(misclassified_probs)[::-1]
        top_failures = misclassified_indices[sorted_indices[:top_n]]
        
        # Create failure cases directory
        failures_dir = self.results_dir / 'failure_cases'
        failures_dir.mkdir(exist_ok=True)
        
        # Save failure case images
        failure_data = []
        for i, idx in enumerate(top_failures):
            # Get image path
            img_path = self.test_generator.filepaths[idx]
            
            # Load and save image with prediction info
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Create figure
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
            ax.imshow(img)
            
            true_label = self.class_names[y_true[idx]]
            pred_label = self.class_names[y_pred[idx]]
            confidence = predictions[idx][0]
            
            ax.set_title(f'True: {true_label} | Pred: {pred_label} | Conf: {confidence:.3f}')
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig(failures_dir / f'failure_{i+1}.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            failure_data.append({
                'image_path': img_path,
                'true_label': true_label,
                'predicted_label': pred_label,
                'confidence': confidence,
                'failure_type': 'misclassification'
            })
        
        # Save failure cases summary
        failure_df = pd.DataFrame(failure_data)
        failure_df.to_csv(self.results_dir / 'failure_cases.csv', index=False)
        
        print(f"Saved {len(failure_data)} failure cases to {failures_dir}")
        
        return failure_df
    
    def generate_evaluation_report(self, results):
        """Generate comprehensive evaluation report"""
        report_path = self.results_dir / 'evaluation_report.md'
        
        with open(report_path, 'w') as f:
            f.write("# Model Evaluation Report\n\n")
            f.write(f"## Model Performance\n")
            f.write(f"- **Test Accuracy**: {results['accuracy']:.4f}\n")
            f.write(f"- **Test Loss**: {results['loss']:.4f}\n\n")
            
            f.write(f"## Class-wise Performance\n")
            for class_name in self.class_names:
                if class_name in results['report']:
                    metrics = results['report'][class_name]
                    f.write(f"### {class_name}\n")
                    f.write(f"- Precision: {metrics['precision']:.4f}\n")
                    f.write(f"- Recall: {metrics['recall']:.4f}\n")
                    f.write(f"- F1-Score: {metrics['f1-score']:.4f}\n\n")
            
            f.write(f"## Visualizations\n")
            f.write(f"- Confusion Matrix: `confusion_matrix.png`\n")
            f.write(f"- ROC Curve: `roc_curve.png`\n")
            f.write(f"- Failure Cases: `failure_cases/` directory\n\n")
            
            f.write(f"## Files Generated\n")
            f.write(f"- `metrics.csv`: Basic metrics\n")
            f.write(f"- `classification_report.csv`: Detailed classification report\n")
            f.write(f"- `predictions.csv`: All predictions with probabilities\n")
            f.write(f"- `failure_cases.csv`: Summary of failure cases\n")
        
        print(f"Evaluation report saved to: {report_path}")
    
    def run_full_evaluation(self):
        """Run complete evaluation pipeline"""
        print("Running full model evaluation...")
        
        # Evaluate model
        results = self.evaluate_model()
        
        # Generate visualizations
        cm = self.plot_confusion_matrix(results['y_true'], results['y_pred'])
        roc_auc = self.plot_roc_curve(results['y_true'], results['predictions'])
        
        # Analyze failure cases
        failure_df = self.analyze_failure_cases(
            results['y_true'], results['y_pred'], results['predictions']
        )
        
        # Generate report
        self.generate_evaluation_report(results)
        
        print(f"\nEvaluation completed!")
        print(f"Results saved to: {self.results_dir}")
        print(f"ROC AUC: {roc_auc:.4f}")
        
        return results

def main():
    """Main function to run model evaluation"""
    print("Starting model evaluation...")
    
    # Create evaluator
    evaluator = ModelEvaluator()
    
    # Run full evaluation
    results = evaluator.run_full_evaluation()
    
    print("Evaluation completed successfully!")

if __name__ == "__main__":
    main()

