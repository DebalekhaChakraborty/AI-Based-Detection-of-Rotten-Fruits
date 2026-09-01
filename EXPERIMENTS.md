# Genuine V1 Experiment Log

Run completed on August 31, 2026 using the frozen historical environment: Ubuntu 18.04.5, CPython 3.6.7, TensorFlow 1.12.0, standalone Keras 2.2.4, and the unchanged 71-package dependency manifest.

## Protocol

- Dataset: Kalluri, *Fruits fresh and rotten for classification*, Kaggle version 1 (August 24, 2018)
- Classes: `fresh_apple`, `fresh_banana`, `fresh_orange`, `rotten_apple`, `rotten_banana`, `rotten_orange`
- Final partitions: 1,539 train, 270 validation, 2,698 original held-out test
- Split: original test preserved; transformation families linked to test excluded from source train; remaining source-train families assigned approximately 85/15 by seed 42
- Shared settings: seed 42, 150 × 150 RGB, batch size 32, Adam, categorical cross-entropy, 20 fixed epochs
- Selection: highest checkpoint validation accuracy; validation loss and train/validation gap were declared tie-breakers
- Test policy: only the validation-selected checkpoint received the one-time final held-out evaluation

The source download already contains offline transformations. “Online augmentation” below means additional transformations generated during training.

## Validation results

| Exp | Model | Online augmentation | Dropout | Selected epoch | Train acc @ selected epoch | Best val acc | Val loss @ selected epoch | Test acc | Observation |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | Custom CNN baseline | No | 0 | 10 | 100.00% | 87.41% | 0.7773 | Not evaluated | Reached perfect training accuracy with a 12.59-point checkpoint gap; clear overfitting. |
| 2 | Custom CNN + dropout | No | 0.5 | 8 | 92.85% | **90.00%** | **0.5937** | **83.21%** | Best validation accuracy and much smaller 2.85-point checkpoint gap; selected. |
| 3 | Custom CNN + dropout | Yes | 0.5 | 14 | 88.30% | 88.89% | 1.0751 | Not evaluated | Small 0.58-point checkpoint gap, but lower peak validation accuracy and higher validation loss than Experiment 2. |

For completeness, fixed-schedule final-epoch metrics were:

| Exp | Final train acc | Final train loss | Final val acc | Final val loss |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 100.00% | 0.0002 | 86.30% | 0.9134 |
| 2 | 97.92% | 0.0681 | 76.30% | 1.6472 |
| 3 | 89.93% | 0.2640 | 81.85% | 1.0631 |

The fixed 20-epoch curves are genuine and stored in [`results/`](results/). Experiment 1 memorized the small leakage-safe training set. Dropout improved the best validation result and reduced the gap at the selected checkpoint. Additional online augmentation constrained training, but it did not beat dropout-only validation performance in this run. The outcome was not changed or retrained after test inspection.

## Validation-only model selection

Experiment 2 was selected before opening the held-out test because its 90.00% best validation accuracy exceeded Experiment 3 (88.89%) and Experiment 1 (87.41%). Its selected validation loss was also the lowest. The selected artifact is the epoch-8 `ModelCheckpoint`, saved locally as `model/fruit_freshness_cnn.h5`; the HDF5 file and class mapping remain ignored by Git.

## One-time final test evaluation

The selected checkpoint was run once over all 2,698 images in the untouched original test partition. Loss and metrics were derived from that single inference pass.

- Test loss: **0.6021**
- Test accuracy: **83.21%** (2,245 correct, 453 incorrect)
- Macro precision / recall / F1: **83.23% / 83.68% / 83.23%**
- Weighted precision / recall / F1: **83.10% / 83.21% / 82.93%**

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| `fresh_apple` | 79.22% | 87.85% | 83.31% | 395 |
| `fresh_banana` | 94.37% | 92.39% | 93.37% | 381 |
| `fresh_orange` | 77.83% | 85.05% | 81.28% | 388 |
| `rotten_apple` | 78.87% | 69.55% | 73.92% | 601 |
| `rotten_banana` | 88.40% | 97.74% | 92.83% | 530 |
| `rotten_orange` | 80.69% | 69.48% | 74.67% | 403 |

The genuine confusion matrix uses rows as actual classes and columns as predicted classes in the order shown:

| Actual / Predicted | fresh apple | fresh banana | fresh orange | rotten apple | rotten banana | rotten orange |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh apple | 347 | 8 | 6 | 34 | 0 | 0 |
| fresh banana | 9 | 352 | 4 | 0 | 8 | 8 |
| fresh orange | 1 | 3 | 330 | 27 | 0 | 27 |
| rotten apple | 72 | 1 | 46 | 418 | 36 | 28 |
| rotten banana | 3 | 1 | 0 | 4 | 518 | 4 |
| rotten orange | 6 | 8 | 38 | 47 | 24 | 280 |

The main weaknesses are rotten apples/oranges being confused with fresh examples or other rotten fruit. Rotten banana is the strongest-recall class. These results describe this dataset and do not establish food safety.

## Representative genuine predictions

The table uses two deterministic seed-42 samples per actual class, then the first misclassifications in generator order until six mistakes are represented. This selection rule was applied mechanically; it does not cherry-pick only correct outcomes. Filenames and source photographs are omitted.

| Actual class | Predicted class | Confidence | Correct? |
| --- | --- | ---: | --- |
| `fresh_apple` | `fresh_apple` | 99.64% | Yes |
| `fresh_apple` | `fresh_apple` | 83.90% | Yes |
| `fresh_banana` | `fresh_banana` | 78.92% | Yes |
| `fresh_banana` | `fresh_banana` | 100.00% | Yes |
| `fresh_orange` | `fresh_orange` | 99.69% | Yes |
| `fresh_orange` | `fresh_orange` | 97.83% | Yes |
| `rotten_apple` | `rotten_apple` | 94.46% | Yes |
| `rotten_apple` | `rotten_apple` | 93.01% | Yes |
| `rotten_banana` | `rotten_banana` | 91.60% | Yes |
| `rotten_banana` | `rotten_banana` | 100.00% | Yes |
| `rotten_orange` | `rotten_banana` | 100.00% | **No** |
| `rotten_orange` | `rotten_orange` | 99.99% | Yes |
| `fresh_apple` | `fresh_banana` | 58.25% | **No** |
| `fresh_apple` | `fresh_orange` | 92.77% | **No** |
| `fresh_apple` | `rotten_apple` | 65.47% | **No** |
| `fresh_apple` | `rotten_apple` | 57.81% | **No** |
| `fresh_apple` | `rotten_apple` | 81.54% | **No** |

## Real inference checks

- CLI: **PASS** — a genuine held-out fresh-apple image returned `Fresh Apple`, 99.64% confidence.
- Flask GET `/`: **PASS** — HTTP 200.
- Flask model-backed POST `/`: **PASS** — HTTP 200 with Fruit, Condition, Prediction, and Confidence rendered for a genuine held-out image (`Fresh Banana`). The temporary upload stayed outside the repository.

## Reproducibility boundary

The experiment code is in [`notebooks/03_cnn_experiments.ipynb`](notebooks/03_cnn_experiments.ipynb). Python, NumPy, and TensorFlow 1.x seeds were set to 42 for every variant. Perfect bit-for-bit numerical reproducibility is not guaranteed across CPU/GPU implementations. Dataset photographs and the HDF5 artifact are not committed.
