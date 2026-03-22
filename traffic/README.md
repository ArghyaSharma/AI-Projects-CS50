# Traffic Sign Classification (CNN)

This project implements a Convolutional Neural Network (CNN) using TensorFlow/Keras to classify traffic signs into 43 categories.

## Overview
The model is trained on labeled image data, where each category corresponds to a specific traffic sign. Images are resized and processed before being used for training.

## Data Processing
- Images are loaded using OpenCV
- Resized to 30 × 30 pixels
- Stored as NumPy arrays
- Labels are converted to one-hot encoded format

## Model Architecture
The CNN is implemented using a sequential model:

- Conv2D (32 filters, 3×3, ReLU)
- MaxPooling (2×2)
- Conv2D (64 filters, 3×3, ReLU)
- MaxPooling (2×2)
- Flatten
- Dense (128 units, ReLU)
- Dropout (0.5)
- Output layer (43 classes, softmax)

## Training
- Optimizer: Adam
- Loss: Categorical Crossentropy
- Evaluation metric: Accuracy
- Train-test split: 60% / 40%
- Epochs: 10

The dataset directory should contain subfolders named 0–42, each representing a traffic sign category.

## Note
- The dataset is not included in this repository due to its size
- The program expects a dataset structured into labeled category folders
