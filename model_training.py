"""
Model Training Script for Cattle/Buffalo Classification
Uses MobileNetV2 for efficient mobile deployment
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras import layers, Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

class CattleBuffaloClassifier:
    def __init__(self, data_dir="processed_data", img_size=(224, 224), batch_size=32):
        self.data_dir = Path(data_dir)
        self.img_size = img_size
        self.batch_size = batch_size
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        
        # Set up data generators
        self.setup_data_generators()
        
    def setup_data_generators(self):
        """Set up data generators with augmentation"""
        print("Setting up data generators...")
        
        # Data augmentation
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            zoom_range=0.1,
            fill_mode='nearest'
        )
        
        val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255
        )
        
        # Create generators
        self.train_generator = train_datagen.flow_from_directory(
            self.data_dir / 'train',
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',  # cow=0, buffalo=1
            shuffle=True
        )
        
        self.val_generator = val_datagen.flow_from_directory(
            self.data_dir / 'val',
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',
            shuffle=False
        )
        
        # Get class names
        self.class_names = list(self.train_generator.class_indices.keys())
        self.num_classes = len(self.class_names)
        
        print(f"Classes: {self.class_names}")
        print(f"Training samples: {self.train_generator.samples}")
        print(f"Validation samples: {self.val_generator.samples}")
    
    def create_model(self):
        """Create MobileNetV2 based model"""
        print("Creating model...")
        
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            input_shape=(*self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model initially
        base_model.trainable = False
        
        # Add custom classification head
        model = tf.keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.2),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(1, activation='sigmoid')  # Binary classification
        ])
        
        # Compile model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, epochs=20):
        """Train the model"""
        print("Training model...")
        
        # Create model
        model = self.create_model()
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=self.models_dir / 'best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        history = model.fit(
            self.train_generator,
            epochs=epochs,
            validation_data=self.val_generator,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        model.save(self.models_dir / 'final_model.h5')
        
        # Plot training history
        self.plot_training_history(history)
        
        return model, history
    
    def fine_tune_model(self, model, epochs=10):
        """Fine-tune the model by unfreezing some layers"""
        print("Fine-tuning model...")
        
        # Unfreeze top layers of base model
        base_model = model.layers[0]
        base_model.trainable = True
        
        # Fine-tune from this layer onwards
        fine_tune_at = 100
        
        # Freeze all the layers before the `fine_tune_at` layer
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001/10),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Continue training
        history_fine = model.fit(
            self.train_generator,
            epochs=epochs,
            initial_epoch=len(model.history.history['loss']),
            validation_data=self.val_generator,
            callbacks=[
                EarlyStopping(
                    monitor='val_accuracy',
                    patience=3,
                    restore_best_weights=True,
                    verbose=1
                )
            ],
            verbose=1
        )
        
        # Save fine-tuned model
        model.save(self.models_dir / 'fine_tuned_model.h5')
        
        return model, history_fine
    
    def plot_training_history(self, history):
        """Plot training history"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        axes[0].plot(history.history['accuracy'], label='Training Accuracy')
        axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
        axes[0].set_title('Model Accuracy')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot loss
        axes[1].plot(history.history['loss'], label='Training Loss')
        axes[1].plot(history.history['val_loss'], label='Validation Loss')
        axes[1].set_title('Model Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.savefig(self.models_dir / 'training_history.png', dpi=150, bbox_inches='tight')
        plt.show()
    
    def evaluate_model(self, model):
        """Evaluate model on test set"""
        print("Evaluating model...")
        
        # Load test data
        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        test_generator = test_datagen.flow_from_directory(
            self.data_dir / 'test',
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='binary',
            shuffle=False
        )
        
        # Evaluate
        test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
        
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Test Loss: {test_loss:.4f}")
        
        return test_loss, test_accuracy

def main():
    """Main function to run model training"""
    print("Starting model training...")
    
    # Create classifier
    classifier = CattleBuffaloClassifier()
    
    # Train model
    model, history = classifier.train_model(epochs=20)
    
    # Fine-tune model
    model, history_fine = classifier.fine_tune_model(model, epochs=10)
    
    # Evaluate model
    test_loss, test_accuracy = classifier.evaluate_model(model)
    
    print(f"\nTraining completed!")
    print(f"Final Test Accuracy: {test_accuracy:.4f}")
    print(f"Models saved to: {classifier.models_dir}")

if __name__ == "__main__":
    main()

