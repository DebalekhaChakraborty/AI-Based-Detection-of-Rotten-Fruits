# Model Artifacts

Training writes two generated files to this directory:

- `fruit_freshness_cnn.h5` — the trained Keras CNN in the HDF5 format used by this project.
- `class_indices.json` — the exact class-to-index mapping produced by the training generator.

Both files are ignored by Git because they are generated from the local dataset. Prediction and evaluation require both artifacts. Do not create a class mapping manually or commit an unverified trained model.

