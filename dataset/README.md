# Dataset Preparation

The image dataset is not included in this repository. Collect images that you have permission to use and arrange the unsplit source directory with one folder per class:

```text
raw_dataset/
├── fresh_apple/
├── rotten_apple/
├── fresh_banana/
├── rotten_banana/
├── fresh_orange/
└── rotten_orange/
```

Supported image extensions are `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, and `.tiff`. Remove corrupt files and obvious duplicates before splitting the data. Images should represent varied backgrounds, viewpoints, and lighting conditions without placing photographs of the same item in different splits.

From the repository root, create a deterministic 70/15/15 split with:

```bash
python src/dataset_split.py path/to/raw_dataset --output dataset
```

The resulting structure is:

```text
dataset/
├── train/
│   ├── fresh_apple/
│   ├── rotten_apple/
│   ├── fresh_banana/
│   ├── rotten_banana/
│   ├── fresh_orange/
│   └── rotten_orange/
├── validation/
│   └── (the same six class folders)
└── test/
    └── (the same six class folders)
```

The default random seed is `42`. The splitter refuses to write into split folders that already contain images, preventing stale or mixed splits. Use a new output directory or remove the old generated split deliberately before running it again.

Keep the test set untouched during model development. The labels describe visible appearance only; they do not establish whether food is microbiologically safe.

