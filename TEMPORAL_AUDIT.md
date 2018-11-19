# V1 Temporal Audit

## Audit Contract

The `legacy` branch has a hard technical cutoff of November 18, 2018. The target interpreter is CPython 3.6.x. Executable Python, notebook code, dependency pins, Flask templates, CSS, documentation, and generated-artifact rules were reviewed against that date.

An item passes only when the selected release or API was available by the cutoff. When a browser or API detail was uncertain, the repository was changed to a simpler period-known form.

## Audit Matrix

| Component | Current usage | Available by 2018-11-18? | Action |
| --- | --- | --- | --- |
| Python | CPython 3.6 grammar, `os.path`, `argparse`, `json`, `random`, `shutil`, `lru_cache`, and formatted strings | Yes | All executable cells and modules use Python 3.6 syntax; no later standard-library keyword is used. |
| TensorFlow | 1.12.0 as the standalone Keras backend | Yes — released November 6, 2018 | Replaced the later 1.13.1 pin. |
| Keras | Standalone Keras 2.2.4 imports | Yes — released October 3, 2018 | Kept all deep-learning imports under `keras`, never `tensorflow.keras`. |
| Keras training | `ImageDataGenerator`, `flow_from_directory`, `fit_generator`, `evaluate_generator`, and `predict_generator` | Yes — present in Keras 2.2.4 | Retained the generator workflow in scripts and notebook. |
| Keras history | `acc`, `val_acc`, `loss`, and `val_loss` | Yes — Keras 2.2.4 naming | Retained classic keys without a later compatibility fallback. |
| Keras prediction image API | Direct `load_img` and `img_to_array` imports; `target_size=(150, 150)` | Yes — present in the period preprocessing package | Changed indirect module access to direct imports and omitted the optional color-mode argument. |
| Model persistence | `model.save()` to `.h5` and standalone `load_model` | Yes — supported by Keras 2.2.4 and h5py 2.8.0 | Kept HDF5 as the only model format. |
| NumPy | 1.15.4; `asarray`, `argmax`, `expand_dims`, and `arange` | Yes — released November 4, 2018 | Replaced the later 1.16.2 pin; retained stable array operations. |
| Matplotlib | 3.0.2; direct pyplot plotting | Yes — released November 11, 2018 | Replaced 3.0.3 and kept manual figures. |
| scikit-learn | 0.20.0; `classification_report` and `confusion_matrix` | Yes — released September 26, 2018 | Replaced 0.20.3; no later display helper or argument is used. |
| Confusion-matrix rendering | `imshow`, ticks, color bar, and per-cell text | Yes | Kept the manual Matplotlib implementation. |
| OpenCV | 3.4.3.18; `imread` and `cvtColor` in exploration | Yes — released September 9, 2018 with CPython 3.6 wheels | Replaced 3.4.5.20. |
| Flask | 1.0.2; route decorators, uploads, templates, redirects, flash messages, and error handler | Yes — released May 2, 2018 with Python 3.6 support | Kept a synchronous local Flask application. |
| Pillow | 5.3.0 | Yes — released October 1, 2018 with Python 3.6 support | Replaced 5.4.1. |
| h5py | 2.8.0 | Yes — released June 5, 2018 with Python 3.6 support | Replaced 2.9.0. |
| Jupyter | 1.0.0 | Yes — released August 12, 2015 | Retained the period-available notebook metapackage. |
| Notebook format | nbformat 4, minor 2; Python 3.6 metadata; empty outputs | Yes — minor 2 dates to 2016 | Kept the conservative schema and cleared execution state. |
| CSS | Fixed/percentage widths, Flexbox, block layout, media query, and ordinary properties | Yes | Removed Grid, gap declarations, custom properties, and arithmetic sizing functions for conservative browser support. |
| HTML/Jinja | HTML5 form and ordinary Jinja interpolation/control blocks | Yes | Retained simple server-rendered templates and corrected the project title. |
| Dependency manifest | One `requirements.txt` with ten direct exact pins | Yes | Removed the separate 2019 manifest and all post-cutoff pins. |

## Exact Dependency Evidence

The selected package releases all predate the cutoff:

- [TensorFlow 1.12.0](https://pypi.org/project/tensorflow/1.12.0/) — November 6, 2018.
- [Keras 2.2.4](https://pypi.org/project/Keras/2.2.4/) — October 3, 2018. Its tagged [training implementation](https://github.com/keras-team/keras/blob/2.2.4/keras/engine/training.py) contains the generator methods, and its tagged [saving implementation](https://github.com/keras-team/keras/blob/2.2.4/keras/engine/saving.py) contains HDF5 model loading and saving.
- [h5py 2.8.0](https://pypi.org/project/h5py/2.8.0/) — June 5, 2018.
- [NumPy 1.15.4](https://pypi.org/project/numpy/1.15.4/) — November 4, 2018.
- [Matplotlib 3.0.2](https://pypi.org/project/matplotlib/3.0.2/) — November 11, 2018.
- [scikit-learn 0.20.0](https://pypi.org/project/scikit-learn/0.20.0/) — September 26, 2018.
- [opencv-python 3.4.3.18](https://pypi.org/project/opencv-python/3.4.3.18/) — September 9, 2018; its release files include CPython 3.6 wheels.
- [Flask 1.0.2](https://pypi.org/project/Flask/1.0.2/) — May 2, 2018 and classified for Python 3.6.
- [Pillow 5.3.0](https://pypi.org/project/Pillow/5.3.0/) — October 1, 2018.
- [Jupyter 1.0.0](https://pypi.org/project/jupyter/1.0.0/) — August 12, 2015.

## Anachronisms and Inconsistencies Corrected

1. The previous dependency contract used a March 31, 2019 cutoff and post-cutoff releases including TensorFlow 1.13.1, h5py 2.9.0, NumPy 1.16.2, Matplotlib 3.0.3, scikit-learn 0.20.3, OpenCV 3.4.5.20, and Pillow 5.4.1. All were replaced with the exact November 18, 2018-compatible pins.
2. `requirements.txt` delegated to `requirements-legacy-2019.txt`. The extra file was removed; `requirements.txt` is now the single canonical manifest.
3. Prediction code and the training notebook accessed image helpers through an imported module and passed `color_mode`. Both now directly import `load_img` and `img_to_array`, and call `load_img(path, target_size=(150, 150))`.
4. The stylesheet used CSS Grid, gap declarations, custom properties, and newer arithmetic sizing functions. It now uses ordinary block and Flexbox layout with `width`, `max-width`, and a media query.
5. The project title included “and Vegetables.” The README and upload page now use “AI-Based Detection of Rotten Fruits Using CNN.”
6. Earlier code used path-object handling, including the later `Path.unlink(missing_ok=True)` form. Executable files now use `os.path`, explicit existence checks, and `os.remove`.
7. Notebook metadata had used a later minor schema. Both notebooks now declare nbformat 4.2, Python 3.6, null execution counts, and empty outputs.
8. A later native Keras model suffix had appeared in ignore rules. Generated model handling is now HDF5-only.

## File Review

| File or area | Result |
| --- | --- |
| `requirements.txt` | Single canonical manifest with the ten required exact pins. |
| `src/train.py` | Standalone Keras, custom sequential CNN, directory generators, `fit_generator`, classic history keys, and HDF5 output. |
| `src/evaluate.py` | Generator evaluation/prediction, scikit-learn 0.20-era metrics, and manual confusion-matrix drawing. |
| `src/predict.py` | Required direct image helper imports and period-compatible HDF5 loading. |
| `src/dataset_split.py` | Python 3.6-compatible deterministic splitting with `os.path` and `shutil`. |
| `app.py` | Flask 1.0-era synchronous upload and prediction flow. |
| `notebooks/01_data_exploration.ipynb` | Conservative OpenCV/NumPy/Matplotlib exploration and 4.2 metadata. |
| `notebooks/02_cnn_training.ipynb` | Mirrors the classic standalone Keras script APIs and direct prediction image helpers. |
| `static/css/style.css` | Conservative 2018 block/Flexbox layout without Grid or arithmetic sizing. |
| `templates/` | Simple HTML/Jinja views; corrected fruit-only project title. |
| Documentation and ignore rules | Consistent HDF5 artifact contract, genuine-result policy, and no reference to a second requirements file. |

## Verification Boundary

The pipeline is structurally complete, but it was not trained or evaluated because this checkout contains no source image dataset, generated split, HDF5 model, class mapping, or measured output. No accuracy or confidence claim can therefore be made. The experiment log remains intentionally empty.

The historical packages were not imported in the current development interpreter. Runtime verification must be performed in the canonical CPython 3.6.x environment after a real dataset is supplied.

## Verdict

At source and manifest level, V1 is aligned to the November 18, 2018 cutoff. No feature, architecture change, transfer-learning component, modern serving framework, or Git history modification was introduced during this audit.
