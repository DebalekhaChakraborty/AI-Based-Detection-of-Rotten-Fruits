"""Split class directories into reproducible training, validation, and test sets."""

import argparse
import os
import random
import shutil


CLASS_NAMES = (
    "fresh_apple",
    "rotten_apple",
    "fresh_banana",
    "rotten_banana",
    "fresh_orange",
    "rotten_orange",
)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def image_files(directory):
    """Return supported images in a stable order."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, name)
        for name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, name))
        and os.path.splitext(name)[1].lower() in IMAGE_EXTENSIONS
    )


def validate_source(source):
    missing = [
        name for name in CLASS_NAMES if not os.path.isdir(os.path.join(source, name))
    ]
    if missing:
        raise ValueError("Missing source class directories: " + ", ".join(missing))

    too_small = [
        name for name in CLASS_NAMES if len(image_files(os.path.join(source, name))) < 7
    ]
    if too_small:
        raise ValueError(
            "Each class needs at least 7 images for non-empty 70/15/15 splits. "
            "Too few images in: " + ", ".join(too_small)
        )


def validate_destination(output):
    for split_name in ("train", "validation", "test"):
        for class_name in CLASS_NAMES:
            destination = os.path.join(output, split_name, class_name)
            if os.path.isdir(destination) and image_files(destination):
                raise ValueError(
                    "Destination already contains split images: {}. "
                    "Choose an empty output directory.".format(destination)
                )


def split_counts(total, train_ratio, validation_ratio):
    train_count = int(total * train_ratio)
    validation_count = int(total * validation_ratio)
    return train_count, validation_count, total - train_count - validation_count


def split_dataset(source, output, train_ratio=0.70, validation_ratio=0.15, seed=42):
    if train_ratio <= 0 or validation_ratio < 0 or train_ratio + validation_ratio >= 1:
        raise ValueError("Ratios must leave positive portions for training and testing.")

    source = os.path.abspath(source)
    output = os.path.abspath(output)
    validate_source(source)
    validate_destination(output)

    random_generator = random.Random(seed)
    totals = {"train": 0, "validation": 0, "test": 0}

    for class_name in CLASS_NAMES:
        files = image_files(os.path.join(source, class_name))
        random_generator.shuffle(files)
        train_count, validation_count, _ = split_counts(
            len(files), train_ratio, validation_ratio
        )
        grouped_files = {
            "train": files[:train_count],
            "validation": files[train_count : train_count + validation_count],
            "test": files[train_count + validation_count :],
        }

        print("{} ({} images)".format(class_name, len(files)))
        for split_name, split_files in grouped_files.items():
            destination = os.path.join(output, split_name, class_name)
            if not os.path.isdir(destination):
                os.makedirs(destination)
            for source_file in split_files:
                shutil.copy2(
                    source_file, os.path.join(destination, os.path.basename(source_file))
                )
            totals[split_name] += len(split_files)
            print("  {:10s}: {}".format(split_name, len(split_files)))

    print("\nSplit complete (seed={}):".format(seed))
    for split_name in ("train", "validation", "test"):
        print("  {:10s}: {} images".format(split_name, totals[split_name]))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a deterministic directory-based image dataset split."
    )
    parser.add_argument("source", help="Directory containing six class folders")
    parser.add_argument(
        "--output", default="dataset", help="Output dataset directory"
    )
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--validation-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        split_dataset(
            args.source,
            args.output,
            train_ratio=args.train_ratio,
            validation_ratio=args.validation_ratio,
            seed=args.seed,
        )
    except (OSError, ValueError) as error:
        print("Dataset split could not be completed: {}".format(error))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
