# AI-Based Detection of Rotten Fruits Using CNN

## Introduction

This project studies the visual classification of fresh and rotten fruit with a convolutional neural network (CNN). Version 1 supports photographs of apples, bananas, and oranges.

The complete pipeline covers image collection guidance, exploratory analysis, reproducible dataset splitting, CNN training, evaluation, single-image prediction, and a local Flask demonstration. The repository does not contain a dataset or trained model, so predictive performance is not yet established.

## Historical Runtime Contract

This `legacy` version has a strict technical cutoff of November 18, 2018. Its canonical runtime is CPython 3.6.x with TensorFlow 1.12.0 and standalone Keras 2.2.4. It uses generator-specific Keras methods, the classic `acc` and `val_acc` history keys, and HDF5 model storage.

The complete compatibility review is recorded in [TEMPORAL_AUDIT.md](TEMPORAL_AUDIT.md).

## Problem Statement

Fruit can show visible signs of spoilage such as discoloration, spotting, bruising, and surface degradation. Manual assessment can vary between observers. This project investigates whether a CNN can learn image patterns associated with the visible freshness condition of three common fruits.

The classifier evaluates visible appearance only. It cannot detect pathogens, toxins, internal spoilage, smell, or other microbiological hazards. It must not be used to decide whether food is safe for consumption.

## Objective

The objective is to train a six-class image classifier that returns the fruit type, visible condition, complete predicted class, and model confidence.

The supported directory labels are:

```text
fresh_apple     rotten_apple
fresh_banana    rotten_banana
fresh_orange    rotten_orange
```

## Dataset

No third-party image collection is committed. Place source images in six class directories and use the included splitter to create reproducible 70% training, 15% validation, and 15% testing subsets. The default random seed is `42`.

```bash
python src/dataset_split.py path/to/raw_dataset --output dataset
```

Every source class needs at least seven images so all three subsets are non-empty. A meaningful experiment needs a substantially larger and varied collection. See [dataset/README.md](dataset/README.md) for the expected directory structure and collection guidance.

## Image Preprocessing

Images are loaded from class directories, resized to `150 × 150` pixels, and normalized by multiplying pixel values by `1/255`.

Training images use `ImageDataGenerator` with rotation, width and height shifts, shear, zoom, and horizontal flipping. Validation and test images are resized and normalized without augmentation.

## CNN Architecture

The classifier is a custom sequential CNN trained from scratch:

| Stage | Configuration |
| --- | --- |
| Input | 150 × 150 × 3 image |
| Convolution | 32 filters, 3 × 3 kernel, ReLU |
| Pooling | 2 × 2 max pooling |
| Convolution | 64 filters, 3 × 3 kernel, ReLU |
| Pooling | 2 × 2 max pooling |
| Convolution | 128 filters, 3 × 3 kernel, ReLU |
| Pooling | 2 × 2 max pooling |
| Classifier | Flatten, Dense 128 with ReLU, Dropout 0.5 |
| Output | Dense 6 with softmax |

Training uses Adam, categorical cross-entropy, and accuracy. The default batch size is 32. No pretrained model or transfer learning is used.

## Installation

Create and activate a CPython 3.6 environment, then install the single canonical dependency manifest:

```bash
python3.6 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The exact environment is:

| Package | Version |
| --- | --- |
| Python | 3.6.x |
| TensorFlow | 1.12.0 |
| Keras | 2.2.4 |
| h5py | 2.8.0 |
| NumPy | 1.15.4 |
| Matplotlib | 3.0.2 |
| scikit-learn | 0.20.0 |
| opencv-python | 3.4.3.18 |
| Flask | 1.0.2 |
| Pillow | 5.3.0 |
| Jupyter | 1.0.0 |

## Training

After preparing the dataset, train with:

```bash
python src/train.py --epochs 20 --batch-size 32
```

Training prints `model.summary()` and creates these genuine run artifacts:

```text
model/fruit_freshness_cnn.h5
model/class_indices.json
outputs/training_accuracy.png
outputs/training_loss.png
```

The JSON file stores the exact class indices created by the training generator. Evaluation, command-line prediction, and the web page all read this mapping.

## Evaluation

Evaluate once on the held-out test directory:

```bash
python src/evaluate.py
```

The script prints test loss, test accuracy, and a classification report. It calculates the confusion matrix and draws it manually with Matplotlib, saving the result as `outputs/confusion_matrix.png`.

## Prediction

Classify one image from the repository root:

```bash
python src/predict.py path/to/image.jpg
```

The output contains the fruit, condition, predicted display class, and confidence. These values come from the saved HDF5 model and its class mapping.

## Web Application

Start the local demonstration after training:

```bash
python app.py
```

Open `http://127.0.0.1:5000/`, choose a JPG, JPEG, PNG, or BMP image of an apple, banana, or orange, and select **Predict**. The upload limit is 8 MB.

## Results and Current Status

The code path is complete, but no dataset, HDF5 model, class mapping, measured accuracy, confusion matrix, or verified confidence result is committed. Therefore the model is not trained in this checkout and its performance remains unproven. Record only genuine runs in [EXPERIMENTS.md](EXPERIMENTS.md).

## Limitations

- Predictions are limited to the six classes used during training.
- Performance depends on dataset size, quality, class balance, and labeling accuracy.
- Lighting, background, camera quality, viewpoint, occlusion, and surface damage can affect predictions.
- A single label cannot describe mixed conditions or several fruit items in one photograph.
- Visible appearance is not a microbiological food-safety measurement.

## Future Scope

- Increase and balance the image dataset.
- Add more fruit classes.
- Improve robustness under varied lighting, backgrounds, and camera conditions.
- Experiment with deeper custom CNN architectures.
- Detect several fruit items in one scene.
- Develop a mobile application.
- Improve real-time camera prediction.

## Repository Structure

```text
├── README.md
├── TEMPORAL_AUDIT.md
├── EXPERIMENTS.md
├── requirements.txt
├── dataset/
│   └── README.md
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_cnn_training.ipynb
├── src/
│   ├── __init__.py
│   ├── dataset_split.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── model/
│   └── README.md
├── outputs/
│   └── README.md
├── static/
│   ├── css/style.css
│   └── uploads/.gitkeep
├── templates/
│   ├── index.html
│   └── result.html
└── app.py
```
