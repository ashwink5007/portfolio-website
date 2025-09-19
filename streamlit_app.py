"""
Streamlit Demo App for Cattle/Buffalo Classification
Interactive web interface for testing the trained model
"""

import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
import io

# Configure page
st.set_page_config(
    page_title="Cattle/Buffalo Classifier",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitCattleClassifier:
    def __init__(self):
        self.model_path = "models/final_model.h5"
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if Path(self.model_path).exists():
                self.model = tf.keras.models.load_model(self.model_path)
                st.success("✅ Model loaded successfully!")
            else:
                st.error("❌ Model not found! Please train the model first.")
                self.model = None
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Convert RGB to BGR if needed
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Resize to 224x224
        img_resized = cv2.resize(img_array, (224, 224))
        
        # Normalize
        img_normalized = img_resized.astype(np.float32) / 255.0
        
        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
    
    def predict(self, image):
        """Make prediction on image"""
        if self.model is None:
            return None, "Model not loaded"
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Make prediction
            prediction = self.model.predict(processed_image, verbose=0)
            probability = prediction[0][0]
            
            # Convert to class
            predicted_class = "Buffalo" if probability > 0.5 else "Cow"
            confidence = max(probability, 1 - probability)
            
            return {
                'class': predicted_class,
                'confidence': confidence,
                'probability': probability,
                'is_buffalo': probability > 0.5
            }, None
            
        except Exception as e:
            return None, str(e)

def main():
    """Main Streamlit app"""
    st.title("🐄 Cattle/Buffalo Breed Classifier")
    st.markdown("---")
    
    # Initialize classifier
    classifier = StreamlitCattleClassifier()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Image Classification", "Model Information", "Dataset Statistics"]
    )
    
    if page == "Image Classification":
        st.header("📸 Upload and Classify Images")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image of a cow or buffalo"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Uploaded Image")
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Image info
                st.subheader("Image Information")
                st.write(f"**Size:** {image.size}")
                st.write(f"**Mode:** {image.mode}")
                st.write(f"**Format:** {uploaded_file.type}")
            
            with col2:
                st.subheader("Classification Result")
                
                # Classify image
                if st.button("🔍 Classify Image", type="primary"):
                    with st.spinner("Classifying image..."):
                        result, error = classifier.predict(image)
                    
                    if error:
                        st.error(f"Classification failed: {error}")
                    else:
                        # Display results
                        st.success("✅ Classification completed!")
                        
                        # Prediction
                        st.metric(
                            label="Predicted Class",
                            value=result['class'],
                            delta=f"{result['confidence']:.1%} confidence"
                        )
                        
                        # Probability breakdown
                        cow_prob = 1 - result['probability']
                        buffalo_prob = result['probability']
                        
                        # Create probability chart
                        fig = go.Figure(data=[
                            go.Bar(
                                x=['Cow', 'Buffalo'],
                                y=[cow_prob, buffalo_prob],
                                marker_color=['#2E8B57', '#8B4513'],
                                text=[f'{cow_prob:.1%}', f'{buffalo_prob:.1%}'],
                                textposition='auto'
                            )
                        ])
                        
                        fig.update_layout(
                            title="Prediction Probabilities",
                            yaxis_title="Probability",
                            yaxis=dict(range=[0, 1]),
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Additional info
                        st.info(f"""
                        **Detailed Results:**
                        - Predicted Class: {result['class']}
                        - Confidence: {result['confidence']:.1%}
                        - Raw Probability: {result['probability']:.4f}
                        - Is Buffalo: {result['is_buffalo']}
                        """)
        
        else:
            st.info("👆 Please upload an image to get started")
            
            # Show sample images if available
            sample_dir = Path("processed_data/test")
            if sample_dir.exists():
                st.subheader("Sample Images")
                st.write("Here are some sample images from the test set:")
                
                # Get sample images
                cow_dir = sample_dir / "cow"
                buffalo_dir = sample_dir / "buffalo"
                
                if cow_dir.exists() and buffalo_dir.exists():
                    cow_images = list(cow_dir.glob("*.jpg"))[:3]
                    buffalo_images = list(buffalo_dir.glob("*.jpg"))[:3]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Cows:**")
                        for img_path in cow_images:
                            img = Image.open(img_path)
                            st.image(img, width=150)
                    
                    with col2:
                        st.write("**Buffaloes:**")
                        for img_path in buffalo_images:
                            img = Image.open(img_path)
                            st.image(img, width=150)
    
    elif page == "Model Information":
        st.header("🤖 Model Information")
        
        if classifier.model is not None:
            # Model architecture
            st.subheader("Model Architecture")
            
            # Model summary
            buffer = io.StringIO()
            classifier.model.summary(print_fn=lambda x: buffer.write(x + '\n'))
            model_summary = buffer.getvalue()
            
            st.text(model_summary)
            
            # Model details
            st.subheader("Model Details")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Input Shape", str(classifier.model.input_shape[1:]))
            
            with col2:
                st.metric("Output Shape", str(classifier.model.output_shape[1:]))
            
            with col3:
                total_params = classifier.model.count_params()
                st.metric("Total Parameters", f"{total_params:,}")
            
            # Performance metrics (if available)
            metrics_file = Path("evaluation_results/metrics.csv")
            if metrics_file.exists():
                st.subheader("Performance Metrics")
                metrics_df = pd.read_csv(metrics_file)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    accuracy = metrics_df[metrics_df['Metric'] == 'Accuracy']['Value'].iloc[0]
                    st.metric("Test Accuracy", f"{accuracy:.1%}")
                
                with col2:
                    loss = metrics_df[metrics_df['Metric'] == 'Loss']['Value'].iloc[0]
                    st.metric("Test Loss", f"{loss:.4f}")
                
                # Confusion matrix
                cm_file = Path("evaluation_results/confusion_matrix.png")
                if cm_file.exists():
                    st.subheader("Confusion Matrix")
                    st.image(str(cm_file), use_column_width=True)
        
        else:
            st.error("Model not loaded. Please train the model first.")
    
    elif page == "Dataset Statistics":
        st.header("📊 Dataset Statistics")
        
        # Check if processed data exists
        processed_dir = Path("processed_data")
        if not processed_dir.exists():
            st.error("Processed data not found. Please run data preprocessing first.")
            return
        
        # Load metadata
        metadata_file = processed_dir / "metadata.csv"
        if metadata_file.exists():
            df = pd.read_csv(metadata_file)
            
            # Overall statistics
            st.subheader("Dataset Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Images", len(df))
            
            with col2:
                cow_count = len(df[df['class_name'] == 'cow'])
                st.metric("Cow Images", cow_count)
            
            with col3:
                buffalo_count = len(df[df['class_name'] == 'buffalo'])
                st.metric("Buffalo Images", buffalo_count)
            
            with col4:
                balance = min(cow_count, buffalo_count) / max(cow_count, buffalo_count)
                st.metric("Class Balance", f"{balance:.1%}")
            
            # Class distribution
            st.subheader("Class Distribution")
            class_counts = df['class_name'].value_counts()
            
            fig = px.pie(
                values=class_counts.values,
                names=class_counts.index,
                title="Class Distribution",
                color_discrete_map={'cow': '#2E8B57', 'buffalo': '#8B4513'}
            )
            st.plotly_chart(fig, use_column_width=True)
            
            # Split distribution
            if 'train_metadata.csv' in [f.name for f in processed_dir.glob('*metadata.csv')]:
                st.subheader("Train/Validation/Test Split")
                
                splits = ['train', 'val', 'test']
                split_data = []
                
                for split in splits:
                    split_file = processed_dir / f"{split}_metadata.csv"
                    if split_file.exists():
                        split_df = pd.read_csv(split_file)
                        split_counts = split_df['class_name'].value_counts()
                        
                        for class_name, count in split_counts.items():
                            split_data.append({
                                'Split': split.title(),
                                'Class': class_name.title(),
                                'Count': count
                            })
                
                if split_data:
                    split_df = pd.DataFrame(split_data)
                    fig = px.bar(
                        split_df,
                        x='Split',
                        y='Count',
                        color='Class',
                        title="Data Split Distribution",
                        color_discrete_map={'Cow': '#2E8B57', 'Buffalo': '#8B4513'}
                    )
                    st.plotly_chart(fig, use_column_width=True)
        
        else:
            st.error("Metadata not found. Please run data preprocessing first.")

if __name__ == "__main__":
    main()
