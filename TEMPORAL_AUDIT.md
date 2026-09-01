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
| Dependency manifest | One `requirements.txt` with 71 exact direct, transitive, and packaging-tool pins | Yes | Removed the separate 2019 manifest, excluded post-cutoff releases, and closed runtime resolution for CPython 3.6.7 on Linux. |

## Dependency Closure

Every package selected below had a release on PyPI by November 18, 2018. A final metadata check covered all 71 pins and 109 dependency declarations applicable to CPython 3.6.7 on Linux; it found no post-cutoff release, missing applicable pin, `Requires-Python` conflict, or unsatisfied version constraint. The Python 3.6 column records package metadata, classifiers, or a CPython 3.6 release artifact as applicable. Optional development, documentation, test, visualization, and platform-specific dependencies that do not apply to a CPython 3.6 Linux runtime are intentionally excluded. In particular, the CPython 3.6 `grpcio` wheel requires only `six`; the source-level `futures` and `enum34` declarations are Python backports and are not dependencies of that wheel.

| Package | Version | Reason required | Available by 2018-11-18 | Python 3.6 compatible |
| --- | --- | --- | --- | --- |
| tensorflow | 1.12.0 | Project deep-learning backend | Yes | Yes |
| Keras | 2.2.4 | Project standalone neural-network API | Yes | Yes |
| h5py | 2.8.0 | Keras dependency and HDF5 model persistence | Yes | Yes |
| numpy | 1.15.4 | TensorFlow, Keras, Matplotlib, scikit-learn, and project array operations | Yes | Yes |
| matplotlib | 3.0.2 | Training and evaluation plots | Yes | Yes |
| scikit-learn | 0.20.0 | Classification report and confusion matrix | Yes | Yes |
| opencv-python | 3.4.3.18 | Notebook image exploration | Yes | Yes |
| Flask | 1.0.2 | Local demonstration application | Yes | Yes |
| Pillow | 5.3.0 | Image loading and generated image support | Yes | Yes |
| jupyter | 1.0.0 | Notebook environment metapackage | Yes | Yes |
| absl-py | 0.6.1 | TensorFlow dependency | Yes | Yes |
| astor | 0.7.1 | TensorFlow dependency | Yes | Yes |
| gast | 0.2.0 | Exact TensorFlow dependency | Yes | Yes |
| grpcio | 1.16.1 | TensorFlow RPC dependency on little-endian systems | Yes | Yes |
| Keras-Applications | 1.0.6 | TensorFlow and Keras application utilities | Yes | Yes |
| Keras-Preprocessing | 1.0.5 | TensorFlow and Keras image preprocessing | Yes | Yes |
| Markdown | 3.0.1 | TensorBoard dependency | Yes | Yes |
| protobuf | 3.6.1 | TensorFlow and TensorBoard serialization | Yes | Yes |
| PyYAML | 3.13 | Keras configuration dependency | Yes | Yes |
| scipy | 1.1.0 | Keras and scikit-learn numerical routines | Yes | Yes |
| six | 1.11.0 | TensorFlow, Keras, dateutil, Bleach, and notebook compatibility dependency | Yes | Yes |
| tensorboard | 1.12.0 | TensorFlow's matching visualization dependency | Yes | Yes |
| termcolor | 1.1.0 | TensorFlow console-output dependency | Yes | Yes |
| cycler | 0.10.0 | Matplotlib property-cycle dependency | Yes | Yes |
| kiwisolver | 1.0.1 | Matplotlib layout constraint solver | Yes | Yes |
| pyparsing | 2.3.0 | Matplotlib expression parser | Yes | Yes |
| python-dateutil | 2.7.5 | Matplotlib and Jupyter Client date handling | Yes | Yes |
| click | 7.0 | Flask command-line dependency | Yes | Yes |
| itsdangerous | 1.1.0 | Flask signed-data dependency | Yes | Yes |
| Jinja2 | 2.10 | Flask and nbconvert templating | Yes | Yes |
| MarkupSafe | 1.1.0 | Jinja2 escaping dependency | Yes | Yes |
| Werkzeug | 0.14.1 | Flask WSGI and request utility dependency | Yes | Yes |
| backcall | 0.1.0 | IPython callback utility | Yes | Yes |
| bleach | 3.0.2 | nbconvert HTML sanitization | Yes | Yes |
| decorator | 4.3.0 | IPython function-wrapping dependency | Yes | Yes |
| defusedxml | 0.5.0 | nbconvert safe XML handling | Yes | Yes |
| entrypoints | 0.2.3 | nbconvert entry-point discovery | Yes | Yes |
| ipykernel | 5.1.0 | Jupyter Python kernel | Yes | Yes |
| ipython | 7.1.1 | Interactive Python shell used by the kernel | Yes | Yes |
| ipython-genutils | 0.2.0 | Shared IPython/Jupyter utilities | Yes | Yes |
| ipywidgets | 7.4.2 | Jupyter widget metapackage dependency | Yes | Yes |
| jedi | 0.13.1 | IPython completion engine | Yes | Yes |
| jsonschema | 2.6.0 | nbformat notebook-schema validation | Yes | Yes |
| jupyter-client | 5.2.3 | Kernel protocol client; 5.2.4 was rejected because it is post-cutoff | Yes | Yes |
| jupyter-console | 6.0.0 | Jupyter terminal console | Yes | Yes |
| jupyter-core | 4.4.0 | Shared Jupyter paths and command utilities | Yes | Yes |
| mistune | 0.8.4 | nbconvert Markdown parser | Yes | Yes |
| nbconvert | 5.4.0 | Notebook document conversion | Yes | Yes |
| nbformat | 4.4.0 | Notebook document format and validation | Yes | Yes |
| notebook | 5.7.0 | Jupyter Notebook server | Yes | Yes |
| pandocfilters | 1.4.2 | nbconvert document filters | Yes | Yes |
| parso | 0.3.1 | Jedi Python parser | Yes | Yes |
| pexpect | 4.6.0 | IPython terminal process control on Unix | Yes | Yes |
| pickleshare | 0.7.5 | IPython lightweight persistence | Yes | Yes |
| prometheus-client | 0.4.2 | Notebook server metrics dependency | Yes | Yes |
| prompt-toolkit | 2.0.7 | IPython and Jupyter Console terminal interface | Yes | Yes |
| ptyprocess | 0.6.0 | pexpect and terminado pseudo-terminal support | Yes | Yes |
| Pygments | 2.2.0 | IPython, qtconsole, and nbconvert syntax highlighting | Yes | Yes |
| pyzmq | 17.1.2 | Jupyter kernel messaging transport | Yes | Yes |
| qtconsole | 4.4.2 | Jupyter Qt console metapackage dependency | Yes | Yes |
| Send2Trash | 1.5.0 | Notebook safe file deletion | Yes | Yes |
| terminado | 0.8.1 | Notebook terminal support | Yes | Yes |
| testpath | 0.4.2 | nbconvert path-checking dependency | Yes | Yes |
| tornado | 5.1.1 | Notebook server and kernel event loop | Yes | Yes |
| traitlets | 4.3.2 | IPython/Jupyter configuration framework | Yes | Yes |
| wcwidth | 0.1.7 | prompt-toolkit terminal-width calculations | Yes | Yes |
| webencodings | 0.5.1 | Bleach HTML encoding support | Yes | Yes |
| widgetsnbextension | 3.4.2 | Notebook front-end support for ipywidgets | Yes | Yes |
| pip | 18.1 | Period package installer used for the lock | Yes | Yes |
| setuptools | 40.5.0 | Period build and installation backend | Yes | Yes |
| wheel | 0.32.2 | TensorFlow requirement and period wheel tooling | Yes | Yes |

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
| `requirements.txt` | Single canonical manifest with 71 exact direct, transitive, and packaging-tool pins. |
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

Runtime validation completed in a disposable Ubuntu 18.04.5 LTS amd64 environment with an isolated, writable, tmpfs-backed `/dev/shm`. A direct C probe completed `sem_open`, `sem_close`, and `sem_unlink`. CPython 3.6.7 was then configured with `HAVE_SEM_OPEN` and `HAVE_SEM_UNLINK`; direct `_multiprocessing.SemLock` import and `multiprocessing.Semaphore(1)` construction both passed.

The unchanged `requirements.txt` installed exactly 71 expected packages with no missing, mismatched, or unexpected distributions, and `pip check` reported no broken requirements. Imports passed for scikit-learn 0.20.0, TensorFlow 1.12.0, standalone Keras 2.2.4, and the complete pinned import surface.

The repository splitter passed against temporary synthetic six-class images outside the repository. It created non-empty train, validation, and test directories for all six classes, and two runs with seed 42 produced identical manifests. The unchanged CNN constructed successfully with 4,829,126 parameters; `ImageDataGenerator`, `flow_from_directory`, `model.summary`, and one epoch of `fit_generator` with batch size 32 completed.

Temporary smoke artifacts included the HDF5 model, exact six-class mapping, accuracy and loss plots, and confusion-matrix plot. HDF5 reload passed. The unchanged evaluation path completed `evaluate_generator`, `predict_generator`, `classification_report`, and `confusion_matrix`. CLI prediction produced Fruit, Condition, Prediction, and Confidence fields. Flask test-client GET `/` and model-backed image POST `/` both passed. Notebook Python 3.6 metadata, setup constants, and import cells were consistent with the frozen environment.

All temporary images, splits, models, mappings, plots, and uploads were deleted with the disposable environment. The repository contained no smoke artifacts after cleanup, and `EXPERIMENTS.md` remained unchanged.

Smoke validation establishes runtime/software compatibility only. Synthetic data results are not model-performance evidence.

## Verdict

At source and dependency-manifest level, V1 is aligned to the November 18, 2018 cutoff. End-to-end runtime validation is blocked by the CPython 3.6.7 `ctypes` crash on the current host and must be retried on a compatible period-capable Linux environment. No feature, architecture change, transfer-learning component, modern serving framework, or Git history modification was introduced during this work.
