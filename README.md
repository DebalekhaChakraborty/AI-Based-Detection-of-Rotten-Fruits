# AI-Based Detection of Rotten Fruits and Vegetables Using CNN

## Introduction

This project studies the visual classification of fresh and rotten produce with a convolutional neural network (CNN). The idea originated during undergraduate study around 2018–2019, when small custom CNNs were a common way to learn image classification. This repository implements that original classical scope today and does not claim that the present code or repository existed at that time.

Version 1 supports photographs of apples, bananas, and oranges. It follows a direct learning sequence: acquire images, inspect and preprocess them, prepare directory-based data splits, train a custom CNN from scratch, evaluate it, make a single-image prediction, and demonstrate the result in a local Flask page.

## Problem Statement

Fruits and vegetables can undergo visible changes during spoilage, including discoloration, spotting, texture change, bruising, and surface degradation. Manual assessment can also vary between observers. This project investigates whether a CNN can learn image patterns associated with the visible freshness condition of three common fruits.

The classifier evaluates visible appearance only. It cannot detect pathogens, toxins, internal spoilage, smell, or other microbiological hazards. It must not be used to decide whether food is safe for consumption.

## Objective

The objective is to train a six-class image classifier that returns:

- fruit type;
- visible freshness condition;
- complete predicted class; and
- confidence assigned by the trained model.

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

Every source class needs at least seven images so all three subsets are non-empty. In a serious experiment, substantially more varied images are needed. See [dataset/README.md](dataset/README.md) for the complete directory structure and collection guidance.

## Image Preprocessing

Images are loaded from class directories, converted to RGB, resized to `150 × 150` pixels, and normalized by multiplying pixel values by `1/255`.

Training images use the classical `ImageDataGenerator` workflow with rotation, width and height shifts, shear, zoom, and horizontal flipping. Validation and test images are only resized and normalized; augmentation is not applied to them.

## CNN Architecture

The classifier is a custom sequential CNN trained from scratch:

| Stage | Configuration |
| --- | --- |
| Input | 150 × 150 × 3 RGB image |
| Convolution | 32 filters, 3 × 3 kernel, ReLU |
| Pooling | 2 × 2 max pooling |
| Convolution | 64 filters, 3 × 3 kernel, ReLU |
| Pooling | 2 × 2 max pooling |
| Convolution | 128 filters, 3 × 3 kernel, ReLU |
| Pooling | 2 × 2 max pooling |
| Classifier | Flatten, Dense 128 with ReLU, Dropout 0.5 |
| Output | Dense 6 with softmax |

Training uses Adam, categorical cross-entropy, and accuracy. The default batch size is 32. No pretrained image model or transfer learning is used.

## Training

Create and activate an isolated Python environment, then install the compatible runtime dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements-legacy-2019.txt` is a documentary reference to an approximate period environment. It is intentionally not the installation file for current computers.

After preparing the dataset, train with:

```bash
python src/train.py --epochs 20 --batch-size 32
```

The epoch count and batch size are configurable. Training prints `model.summary()` and writes only genuine run artifacts:

```text
model/fruit_freshness_cnn.h5
model/class_indices.json
outputs/training_accuracy.png
outputs/training_loss.png
```

The JSON file stores the exact class indices created by the training generator. Evaluation, command-line prediction, and the web page read this mapping instead of assuming a class order.

## Evaluation

Evaluate once on the held-out test directory:

```bash
python src/evaluate.py
```

The script prints test loss, test accuracy, and a classification report. It calculates and saves the real confusion matrix as `outputs/confusion_matrix.png`. If the dataset or trained artifacts are absent, it explains what must be prepared instead of inventing results.

## Prediction

Classify one image from the repository root:

```bash
python src/predict.py path/to/image.jpg
```

The output contains fruit, condition, predicted display class, and confidence. All values are derived from the saved model and its class mapping.

## Web Application

The local demonstration accepts JPG, JPEG, PNG, and BMP files up to 8 MB. Start it after training:

```bash
python app.py
```

Open `http://127.0.0.1:5000/`, choose an apple, banana, or orange image, and select **Predict**. The result page displays the uploaded photograph and the same real prediction fields as the command-line utility.

## Results

No accuracy, loss, confidence example, confusion matrix, or experimental conclusion is supplied in advance. Run the workflow on a documented dataset, then record genuine results in [EXPERIMENTS.md](EXPERIMENTS.md). Generated plots and model files are ignored by Git.

## Limitations

- Predictions are limited to the six classes used during training.
- Performance depends strongly on the size, quality, and balance of the collected dataset.
- Backgrounds, lighting, camera quality, viewpoint, occlusion, and surface damage may affect predictions.
- A single label cannot describe mixed conditions or multiple produce items in one photograph.
- Visual appearance is not a microbiological food-safety measurement.

## Future Scope

- Increase and balance the image dataset.
- Include additional fruits and vegetables.
- Improve robustness under different lighting and camera conditions.
- Reduce sensitivity to image backgrounds.
- Experiment with deeper custom CNN architectures.
- Detect multiple produce items in one scene.
- Develop a mobile application.
- Improve real-time camera prediction.

## Technologies Used

- Python
- OpenCV and Pillow
- NumPy
- Matplotlib
- scikit-learn
- Keras with TensorFlow
- Flask
- HTML and CSS
- Jupyter Notebook

## Repository Structure

```text
├── README.md
├── EXPERIMENTS.md
├── requirements.txt
├── requirements-legacy-2019.txt
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
│   └── uploads/
├── templates/
│   ├── index.html
│   └── result.html
└── app.py
```

When Version 1 has been trained, evaluated, reviewed, and committed, create its release tag without changing commit dates:

```bash
git tag -a v1.0-classical-cnn -m "Classical CNN Version 1"
```
