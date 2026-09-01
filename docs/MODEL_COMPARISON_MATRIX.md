# Model Comparison Matrix

## Comparison Cohorts

The year labels identify research cohorts for this project, not necessarily the original publication year of every named architecture.

| Generation | Model | Training Style | Representation | Expected Strength |
| --- | --- | --- | --- | --- |
| 2018 | Custom CNN | From scratch | Task specific | Historical baseline |
| 2020 | ResNet / EfficientNet | Transfer learning | ImageNet features | Stronger reusable visual features |
| 2024 | DINOv2 | Self-supervised feature extraction or fine-tuning | Foundation representation | Labelled-data efficiency |
| 2024 | CLIP / SigLIP | Vision-language feature extraction or fine-tuning | Semantic visual-language features | Cross-domain generalization |
| 2026 | VLM cohort | Multimodal reasoning | Image and language | Evidence-oriented explanation |

These entries define hypotheses to test. They are not performance claims, implementation commitments, or rankings.

## Required Comparison Dimensions

| Dimension | Required record |
| --- | --- |
| Supervision | Labels used locally and assumptions inherited from pretraining |
| Adaptation | From scratch, frozen probe, partial fine-tuning, full fine-tuning, or prompted evaluation |
| Data | Dataset version, split manifest, labelled fraction, and exclusions |
| Capacity | Parameter count and trainable parameter count |
| Input | Resolution, normalization, augmentation, and modality |
| Compute | Device, precision, training/inference time, and approximate resource budget |
| Selection | Validation metric and checkpoint rule |
| Evaluation | Core classification metrics and registered robustness tests |
| Explanation | Output type, rubric, sample protocol, and human-review process |
| Reproducibility | Environment lock, configuration, weights identifier, seed, and artifact hashes |

## Planned Evaluation Modes

- **Historical reference:** report frozen V1 evidence without changing its runtime or implementation.
- **Modern supervised baseline:** establish a current framework baseline before introducing pretrained representations.
- **Transfer-learning comparison:** compare frozen and fine-tuned convolutional features under the same split.
- **Foundation embedding comparison:** train controlled lightweight classifiers on fixed embeddings.
- **Few-shot comparison:** repeat predetermined labelled fractions and seeds.
- **Cross-domain comparison:** train or select on the primary data and evaluate separately on approved external data.
- **Multimodal comparison:** assess both class decisions and language explanations under a registered rubric.

No model in this matrix has been implemented or evaluated by V2 yet.
