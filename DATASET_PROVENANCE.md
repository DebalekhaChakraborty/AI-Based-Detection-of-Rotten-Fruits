# Dataset Provenance and Local Audit

## Source identity and historical gate

The genuine V1 run uses **Fruits fresh and rotten for classification**, published on Kaggle by **Sriram Reddy Kalluri** under the stable dataset reference `sriramr/fruits-fresh-and-rotten-for-classification`.

The provenance gate passed with reasonable confidence:

- The [original Kaggle dataset page](https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification) identifies Kalluri as owner and describes apples, oranges, and bananas.
- [Kaggle's public dataset metadata](https://www.kaggle.com/api/v1/datasets/view/sriramr/fruits-fresh-and-rotten-for-classification) reports dataset ID `46490`, version `1`, creation and last-update time `2018-08-24T15:05:40.8Z`, and version note `Initial release`. It reports only one version, so there is no evidence that a later replacement was substituted under the same name.
- The six directories in the downloaded version are fresh and rotten apple, banana, and orange.
- The paper [Evaluation of CNN based on Hyperparameters to Detect the Quality of Apples](https://ijettjournal.org/Volume-70/Issue-10/IJETT-V70I10P222.pdf) independently describes the Kalluri dataset as updated on August 24, 2018 and containing the same six fresh/rotten fruit categories.

This evidence places the version before the project's November 2018 cutoff. The dataset was downloaded from Kaggle, not from a mirror.

## Version and archive integrity

| Field | Recorded value |
| --- | --- |
| Kaggle reference | `sriramr/fruits-fresh-and-rotten-for-classification` |
| Kaggle dataset ID | `46490` |
| Version | `1` (`Initial release`) |
| Published/updated | August 24, 2018 |
| Kaggle-reported unpacked bytes | 1,949,616,736 |
| Locally inventoried canonical-tree bytes | 1,949,616,736 |
| Download SHA-256 | `5ccfb8624b7a279f22d3508f2ff1e2148c902c1fd755001e1a4b9b52a011abfb` |
| Archive integrity test | PASS |

The archive lists the same 13,599-image manifest under both `dataset/` and `dataset/dataset/`. Their relative manifests match; only one canonical tree was retained for the local audit. The downloaded archive and raw files stayed outside the repository.

## Raw local inventory

All 13,599 files are PNG images. Every image decoded successfully with OpenCV 3.4.3.18.

| Class | Source train | Source test | Total | Width range | Height range | Mean width × height |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `fresh_apple` | 1,693 | 395 | 2,088 | 150–584 | 142–510 | 353.50 × 351.87 |
| `fresh_banana` | 1,581 | 381 | 1,962 | 174–862 | 128–496 | 509.58 × 378.69 |
| `fresh_orange` | 1,466 | 388 | 1,854 | 144–750 | 138–478 | 362.86 × 318.11 |
| `rotten_apple` | 2,342 | 601 | 2,943 | 182–588 | 192–492 | 374.59 × 349.44 |
| `rotten_banana` | 2,224 | 530 | 2,754 | 188–796 | 190–518 | 512.33 × 375.07 |
| `rotten_orange` | 1,595 | 403 | 1,998 | 144–696 | 116–496 | 376.43 × 334.91 |
| **Total** | **10,901** | **2,698** | **13,599** |  |  |  |

Integrity findings:

- Unreadable/corrupt images: **0**
- Unique SHA-256 hashes: **13,599**
- Exact duplicate hash groups: **0**
- Exact cross-split duplicates: **0**
- Exact cross-class duplicates: **0**

## Transformation-family leakage control

Although no files are byte-identical, filenames show that the published dataset already contains offline variants such as rotations, translations, vertical flips, and salt-and-pepper transformations. Filename-family analysis found that every base photograph represented in the source test split also had transformed relatives in the source training split. A naive split would therefore leak near-identical visual content across development and test data.

The experiment copy applies this conservative policy without changing the download:

1. Preserve the original Kaggle test partition without reassignment.
2. Exclude all 9,092 source-train files whose base photograph is represented in the original test partition.
3. Treat every remaining base photograph and its offline variants as one group.
4. Shuffle those groups deterministically with Python seed `42` and assign approximately 85% to training and 15% to validation.

Excluded source-train variants by class were 1,387 fresh apple, 1,266 fresh banana, 1,187 fresh orange, 2,099 rotten apple, 1,801 rotten banana, and 1,352 rotten orange. After preparation there are zero filename-linked base groups and zero exact SHA-256 groups shared between final splits.

## Frozen experimental partitions

| Class | Train | Validation | Original test |
| --- | ---: | ---: | ---: |
| `fresh_apple` | 261 | 45 | 395 |
| `fresh_banana` | 270 | 45 | 381 |
| `fresh_orange` | 234 | 45 | 388 |
| `rotten_apple` | 207 | 36 | 601 |
| `rotten_banana` | 360 | 63 | 530 |
| `rotten_orange` | 207 | 36 | 403 |
| **Total** | **1,539** | **270** | **2,698** |

The train/validation partition contains 171/30 base-photograph groups respectively. The original test contains 1,310 groups. No corrupt image needed exclusion.

## Genuine EDA observations

The existing exploration notebook was run against the final genuine training partition. It inspected 1,539 images; dimensions ranged from 150 × 152 to 762 × 480, with mean dimensions about 414.9 × 350.1 pixels.

Visual inspection found many isolated fruit photographs on light or white backgrounds, with some darker or colored backgrounds. Scale, crop, and lighting vary. Offline rotations sometimes leave dark triangular borders. Fresh examples generally have smoother, more uniform, brighter surfaces; rotten examples commonly show dark lesions, bruising, shriveling, discoloration, or visible mold. These are dataset-level tendencies, not food-safety evidence. The final training partition is moderately imbalanced, with rotten banana largest and rotten apple/rotten orange smallest.

Because the source already contains offline transformations, Experiments 1 and 2 use no **additional online** augmentation; Experiment 3 adds the canonical `ImageDataGenerator` transformations.

## Licensing and redistribution

Kaggle metadata labels the license as `Unknown`; no explicit redistribution license was found. No license is inferred.

Dataset images are not redistributed in this repository.
