# V2 Experiment Protocol

## Protocol Status

This document defines the rules that must be satisfied before a V2 result can be treated as research evidence. It does not contain model results.

## Dataset Rules

- Record the dataset title, source, owner, version, retrieval date, checksum, license or terms, and local preparation procedure.
- Preserve official train/test partitions when they exist and are methodologically suitable.
- Create validation data only from the development partition.
- Store every final split as an immutable manifest with stable sample identifiers and a recorded seed.
- Audit exact duplicates, transformation families, subject/object overlap, and other plausible leakage routes before training.
- Keep the test set closed during model choice, hyperparameter selection, threshold selection, and prompt development.
- Apply the same class ontology and evaluation protocol to models in a direct comparison.
- Report cross-domain datasets separately from the primary benchmark.
- Never infer redistribution permission from public availability.

## Comparison Controls

A comparison must state which variable is changing: architecture, pretraining, supervision, labelled-data fraction, fine-tuning strategy, or reasoning interface. All other feasible factors should remain fixed or be reported as confounders. Compute budget, input resolution, parameter count, and pretrained data assumptions must accompany performance claims.

The historical V1 result is a fixed reference, not a modern rerun. A reproduced modern baseline receives a new experiment ID and cannot overwrite V1 evidence.

## Metrics

### Classification

- Accuracy
- Per-class precision, recall, F1-score, and support
- Macro and weighted F1-score
- Confusion matrix

Where class imbalance or operating thresholds matter, balanced accuracy, calibration, and confidence intervals may be registered before execution. Additional metrics must not replace the core set without explanation.

### Representation Analysis

- Training-data efficiency across predetermined labelled fractions
- Few-shot performance under a fixed sampling protocol
- Cross-domain generalization on separately identified datasets
- Linear-probe versus fine-tuned performance, where applicable

### Explainability

- Qualitative comparison using a fixed, documented sample set
- Human interpretation of relevance, visible-evidence grounding, clarity, and uncertainty
- Error analysis for plausible but unsupported explanations

Human review must record the rubric, reviewer instructions, sample-selection method, and disagreement handling. A convincing narrative is not automatically a faithful explanation.

## Model Selection and Test Gate

1. Register the experiment configuration and split hashes.
2. Train or evaluate all planned validation variants.
3. Select the model and checkpoint using the declared validation rule.
4. Freeze code, configuration, weights identifier, and decision record.
5. Open the test set once for the registered final evaluation.
6. Report the outcome without tuning against test errors.

If the protocol changes after test access, the work becomes exploratory and must use a new untouched test source for confirmatory claims.

## Experiment Identification

Use stable IDs with the form `V2-PHASE-MODEL-DATA-RUN`, for example `V2-P2-TL-PRIMARY-001`. IDs identify an evidence record, not merely a notebook session.

## Experiment Template

Every experiment record must include:

### Experiment ID

Unique identifier, status, owner, and execution dates.

### Objective

The specific question or hypothesis and the comparison being made.

### Model

Architecture, parameter count, pretraining source, weights identifier, checkpoint policy, and trainable components.

### Dataset

Version, checksum, class ontology, split-manifest hashes, sample counts, exclusions, and license boundary.

### Training Configuration

Environment, device, precision, input resolution, augmentation, sampling, stopping rule, and compute budget.

### Hyperparameters

Batch size, learning rate and schedule, epochs or steps, optimizer, regularization, seed, and all model-specific settings.

### Results

Declared metrics with units, aggregation method, uncertainty where available, and links to immutable artifacts.

### Observations

Learning behavior, error patterns, qualitative evidence, and deviations from the plan.

### Limitations

Known confounders, data constraints, generalization boundary, and claims that the experiment cannot support.
