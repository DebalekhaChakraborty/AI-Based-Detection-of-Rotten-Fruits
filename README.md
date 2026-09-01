# AI-Based Detection of Rotten Fruits Using CNN

## Introduction

This project studies the visual classification of fresh and rotten fruit with a convolutional neural network (CNN). Version 1 supports photographs of apples, bananas, and oranges.

The complete pipeline covers provenance and integrity auditing, exploratory analysis, leakage-aware splitting, CNN training, evaluation, single-image prediction, and a local Flask demonstration. V1 has now been genuinely trained and evaluated while keeping the third-party dataset and large model binary outside Git.

## Project Evolution

### V1 — Classical Deep Learning (2018)

V1 is the completed historical study, **AI-Based Fruit Freshness Classification Using CNN (2018)**. It uses a custom CNN trained from scratch with TensorFlow 1.x, standalone Keras 2.2.4, and OpenCV. The `legacy` branch freezes its implementation, environment, genuine experiments, and documented limitations.

### V2 — Modern Vision AI Research (2026)

V2 is **AI-Based Fruit Freshness Intelligence Using Modern Vision AI**, a comparative research programme exploring:

- Modern from-scratch CNN baselines
- Transfer learning
- Self-supervised vision foundation models
- Vision-language representations
- Multimodal reasoning and explanation assessment
- Labelled-data efficiency and cross-domain generalization

**Research in progress.** V2 currently provides the research protocol, dataset strategy, reproducibility rules, roadmap, configuration intent, and empty project structure only. No V2 model has been implemented and no V2 result is claimed.

The research framework begins with [V2_RESEARCH_BLUEPRINT.md](docs/V2_RESEARCH_BLUEPRINT.md). The complete protocol is in [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md), and planned model cohorts are defined without results in [MODEL_COMPARISON_MATRIX.md](docs/MODEL_COMPARISON_MATRIX.md).

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

The genuine experiment uses Sriram Reddy Kalluri's Kaggle dataset, [*Fruits fresh and rotten for classification*](https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification), version 1 from August 24, 2018. Its six categories map directly to the V1 labels. Kaggle lists the license as unknown, so the archive and individual photographs are excluded from this repository.

Dataset images are not redistributed in this repository.

The download contained 10,901 source-train and 2,698 source-test PNGs. All 13,599 decoded successfully, all SHA-256 hashes were unique, and no exact cross-split duplicate was found. Filename analysis nevertheless revealed source-provided rotations, translations, flips, and noise variants derived from the same base photographs across the published train/test boundary.

The preparation therefore preserved the original test set, removed 9,092 source-train variants linked to test base photographs, grouped every remaining transformation family, and split those groups approximately 85/15 with seed 42. The frozen experiment counts are:

| Class | Train | Validation | Original test |
| --- | ---: | ---: | ---: |
| Fresh apple | 261 | 45 | 395 |
| Fresh banana | 270 | 45 | 381 |
| Fresh orange | 234 | 45 | 388 |
| Rotten apple | 207 | 36 | 601 |
| Rotten banana | 360 | 63 | 530 |
| Rotten orange | 207 | 36 | 403 |
| **Total** | **1,539** | **270** | **2,698** |

The full historical evidence, raw inventory, dimension ranges, leakage analysis, EDA observations, and redistribution boundary are in [DATASET_PROVENANCE.md](DATASET_PROVENANCE.md). The generic splitter remains available for other legitimately sourced collections; see [dataset/README.md](dataset/README.md).

## Image Preprocessing

Images are loaded from class directories, resized to `150 × 150` pixels, and normalized by multiplying pixel values by `1/255`.

Experiment 1 and Experiment 2 use only normalization. Experiment 3 uses the canonical `ImageDataGenerator` rotation, width and height shifts, shear, zoom, and horizontal flip settings. Validation and test images are resized and normalized without online augmentation. The published source itself already contains offline transformations, which is disclosed separately from online augmentation.

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

## V1 Installation

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

## V2 Environment Boundary

V2 uses a separate Python 3.11+ research environment and never installs modern packages into the V1 environment:

```bash
python3.11 -m venv .venv-v2
source .venv-v2/bin/activate
python -m pip install -r requirements-v2.txt
```

`requirements-v2.txt` is a bootstrap manifest for PyTorch, torchvision, timm, transformers, OpenCV, scikit-learn, pandas, NumPy, Matplotlib, Jupyter, seaborn, and Pillow. Exact resolved versions must be locked and recorded before an experiment. No V2 packages are required to inspect the research framework.

## Training

The three controlled variants are defined explicitly in [notebooks/03_cnn_experiments.ipynb](notebooks/03_cnn_experiments.ipynb). After preparing the documented local partition, the canonical augmentation-based training entry point remains:

```bash
python src/train.py --epochs 20 --batch-size 32
```

Training prints `model.summary()` and creates these local artifacts:

```text
model/fruit_freshness_cnn.h5
model/class_indices.json
outputs/training_accuracy.png
outputs/training_loss.png
```

The JSON file stores the exact class indices created by the training generator. Evaluation, command-line prediction, and the web page all read this mapping. For the genuine comparison, best-validation checkpoints were retained, and the validation-selected Experiment 2 checkpoint was copied to the canonical local model path. The model and mapping are ignored by Git.

## Evaluation

For a new, independently prepared run, evaluate once on its held-out test directory only after validation-based model selection:

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

## Experimental Results

All variants used the same seed-42 partition, 150 × 150 inputs, Adam, categorical cross-entropy, batch size 32, and 20 fixed epochs. “Augmentation” here means additional online augmentation.

| Experiment | Dropout | Online augmentation | Selected epoch | Train acc @ selected epoch | Best validation acc | Validation loss |
| ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 1 — baseline | 0 | No | 10 | 100.00% | 87.41% | 0.7773 |
| 2 — dropout | 0.5 | No | 8 | 92.85% | **90.00%** | **0.5937** |
| 3 — dropout + augmentation | 0.5 | Yes | 14 | 88.30% | 88.89% | 1.0751 |

Experiment 2 was selected strictly from validation behavior. The baseline showed the clearest overfitting, with perfect training accuracy and a 12.59-point checkpoint gap. Dropout improved validation accuracy and reduced that gap. Online augmentation constrained the fit and produced a small checkpoint gap, but it did not exceed dropout-only validation performance in this run.

The six genuine learning curves are in [results/](results/), and exact histories and observations are recorded in [EXPERIMENTS.md](EXPERIMENTS.md).

## Final Evaluation

After selection, the Experiment 2 epoch-8 checkpoint was evaluated once using a single inference pass across all 2,698 original held-out test images.

- Test loss: **0.6021**
- Test accuracy: **83.21%** (2,245 correct, 453 incorrect)
- Macro F1: **83.23%**
- Weighted F1: **82.93%**

Rotten banana had the strongest recall at 97.74%. Rotten apple and rotten orange were the weakest-recall classes at 69.55% and 69.48%, with confusion involving fresh fruit and other rotten-fruit classes. The genuine [confusion matrix](results/final_confusion_matrix.png), full six-class report, and a deterministic prediction table containing both correct and incorrect cases are in [EXPERIMENTS.md](EXPERIMENTS.md).

The real selected model also passed the unchanged CLI and Flask GET/model-backed POST checks with genuine held-out images. These metrics describe this specific historical dataset and split; they do not imply microbiological safety or broad real-world generalization.

## Observations

- Conservative transformation-family leakage removal reduced the usable development data substantially; honest independence was prioritized over a larger headline training count.
- The published images vary in crop, scale, lighting, and background, but many still resemble isolated or stock-style fruit photographs.
- Offline rotations sometimes introduce dark border artifacts that a model could learn.
- The validation peak occurred well before epoch 20 in every experiment, so preserving the best checkpoint mattered.
- Dropout-only won this comparison. The expected augmentation variant was not assumed to be superior.
- High-confidence mistakes occurred, so softmax confidence must not be interpreted as calibrated certainty.

## Limitations

- Predictions are limited to the six classes used during training.
- Performance depends on dataset size, quality, class balance, and labeling accuracy.
- Lighting, background, camera quality, viewpoint, occlusion, and surface damage can affect predictions.
- A single label cannot describe mixed conditions or several fruit items in one photograph.
- Visible appearance is not a microbiological food-safety measurement.

## Future Scope

V1 remains frozen. Future research is organized through the phased [V2 roadmap](docs/ROADMAP.md): research setup, modern baseline reproduction, transfer learning, foundation embeddings, vision-language reasoning, and paper preparation.

## Repository Structure

```text
├── README.md
├── TEMPORAL_AUDIT.md
├── DATASET_PROVENANCE.md
├── EXPERIMENTS.md
├── requirements.txt
├── requirements-v2.txt
├── docs/
│   ├── V2_RESEARCH_BLUEPRINT.md
│   ├── EXPERIMENT_PROTOCOL.md
│   ├── MODEL_COMPARISON_MATRIX.md
│   ├── DATASET_STRATEGY.md
│   ├── REPRODUCIBILITY_GUIDE.md
│   └── ROADMAP.md
├── dataset/
│   └── README.md
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_cnn_training.ipynb
│   └── 03_cnn_experiments.ipynb
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
├── results/
│   ├── experiment_01_accuracy.png
│   ├── experiment_01_loss.png
│   ├── experiment_02_accuracy.png
│   ├── experiment_02_loss.png
│   ├── experiment_03_accuracy.png
│   ├── experiment_03_loss.png
│   └── final_confusion_matrix.png
├── v2/
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── splits/
│   ├── notebooks/
│   ├── src/
│   │   ├── datasets/
│   │   ├── models/
│   │   ├── training/
│   │   ├── evaluation/
│   │   └── visualization/
│   ├── experiments/
│   ├── configs/
│   │   ├── baseline_cnn.yaml
│   │   ├── transfer_learning.yaml
│   │   ├── foundation_embedding.yaml
│   │   └── vlm_evaluation.yaml
│   └── results/
├── static/
│   ├── css/style.css
│   └── uploads/.gitkeep
├── templates/
│   ├── index.html
│   └── result.html
└── app.py
```
