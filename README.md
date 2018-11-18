# AI-Based Detection of Rotten Fruits and Vegetables Using CNN

A convolutional neural network that classifies fruits and vegetables as fresh
or rotten from a photograph.

## Motivation

Spoilage is identified by manual inspection in most post-harvest supply chains,
which is slow and inconsistent between graders. This project trains a CNN to
perform the same visual classification.

## Layout

```text
src/         training, evaluation, and dataset-splitting code
dataset/     local image splits (not tracked — see dataset/README.md)
model/       trained weights and class mapping (generated, not tracked)
outputs/     accuracy, loss, and confusion-matrix plots (generated)
notebooks/   exploratory work
templates/   Flask templates for the prediction interface
static/      CSS and uploaded images for the interface
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`requirements-legacy-2019.txt` records the original TensorFlow 1.x environment
for reference; it is not expected to install on a current interpreter.

## Status

Repository structure and documentation only. No trained model, metrics, or
results are included — `EXPERIMENTS.md` is filled in from genuine runs.

## Note on labels

Class labels describe visible appearance. They do not establish whether food is
microbiologically safe to eat.
