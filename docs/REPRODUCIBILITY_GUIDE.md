# V2 Reproducibility Guide

## Reproducibility Standard

Every reported number must be traceable to an experiment ID, immutable configuration, dataset and split hashes, environment record, model weights identifier, and generated artifact manifest. A notebook alone is not an experiment record.

## Environment Record

Record at minimum:

- Operating system and architecture
- Python version
- CUDA toolkit and driver versions, or explicit CPU-only status
- GPU model and count
- Framework and vision-library versions
- Full resolved Python package lock
- Relevant system libraries and determinism settings
- Repository commit and working-tree status

`requirements-v2.txt` is a lightweight bootstrap manifest. Each executed experiment must additionally preserve an exact resolved environment lock.

## Model Record

Record:

- Architecture and model family
- Parameter count and trainable parameter count
- Pretrained dataset description, when known
- Exact pretrained weights name, revision, and checksum or provider identifier
- Adaptation mode: from scratch, frozen, linear probe, partial fine-tune, full fine-tune, or prompted
- Selected checkpoint path, checksum, epoch/step, and validation selection rule

Remote model names without a revision are insufficient because upstream weights can change.

## Training Record

Record:

- Batch size and gradient accumulation
- Learning rate and schedule
- Epochs or optimizer steps
- Optimizer and all optimizer parameters
- Loss function and class weighting
- Input resolution, normalization, augmentation, and sampling
- Random seed or seed set
- Precision mode and determinism flags
- Early-stopping or checkpoint policy
- Start/end time and resource usage context

Perfect numerical reproducibility may not be possible across devices. Deterministic controls and known nondeterministic operations must still be recorded.

## Evaluation Record

Record:

- Dataset source version and checksum
- Train, validation, and test manifest checksums
- Exact sample counts and exclusions
- Class-index mapping
- Evaluation code version and configuration
- Metrics, averaging conventions, thresholds, and confidence-interval procedure
- Test-access decision record
- Cross-domain and few-shot protocols, where applicable
- Explanation sample-selection and human-review rubrics

## Artifact Manifest

Every completed experiment should list:

- Configuration file
- Console or structured log
- Environment lock
- Split manifests
- Selected checkpoint reference and checksum
- Metric tables
- Learning curves
- Confusion matrix
- Per-sample predictions using non-sensitive identifiers
- Qualitative evaluation record, if applicable
- Failure notes and deviations from protocol

Large weights, raw images, and restricted data must not be committed merely for convenience. Their controlled storage location and checksums should be recorded instead.

## Minimum Completion Checklist

- [ ] Experiment ID and objective registered before test access
- [ ] Repository commit and clean/dirty status recorded
- [ ] Exact environment captured
- [ ] Dataset provenance and license gate passed
- [ ] Split manifests frozen and hashed
- [ ] Seeds and determinism boundary recorded
- [ ] Validation selection rule applied
- [ ] Test access logged
- [ ] Required metrics and artifacts generated
- [ ] Limitations and deviations documented
- [ ] Artifact manifest verified

An experiment that misses a required item may remain useful for exploration, but it must not be presented as a fully reproducible confirmatory result.
