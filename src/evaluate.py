"""Evaluate the trained CNN on the held-out test directory."""

import argparse
import json
import math
from pathlib import Path


def load_mapping(mapping_path):
    if not mapping_path.is_file():
        raise FileNotFoundError("Class mapping not found: {}".format(mapping_path))
    with mapping_path.open("r", encoding="utf-8") as mapping_file:
        mapping = json.load(mapping_file)
    if not isinstance(mapping, dict) or len(mapping) != 6:
        raise ValueError("Class mapping must contain exactly six classes.")
    return mapping


def evaluate(args):
    test_directory = args.dataset / "test"
    if not test_directory.is_dir():
        raise FileNotFoundError("Test dataset not found: {}".format(test_directory))
    if not args.model.is_file():
        raise FileNotFoundError("Trained model not found: {}".format(args.model))
    saved_mapping = load_mapping(args.mapping)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.metrics import classification_report, confusion_matrix
    from keras.models import load_model
    from keras.preprocessing.image import ImageDataGenerator
    test_data = ImageDataGenerator(rescale=1.0 / 255)
    test_generator = test_data.flow_from_directory(
        str(test_directory),
        target_size=(150, 150),
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=False,
    )
    if test_generator.samples == 0:
        raise ValueError("The test dataset contains no readable images.")
    if test_generator.class_indices != saved_mapping:
        raise ValueError(
            "Test class directories do not match model/class_indices.json."
        )

    model = load_model(str(args.model))
    steps = max(1, int(math.ceil(test_generator.samples / float(args.batch_size))))
    test_generator.reset()
    test_loss, test_accuracy = model.evaluate_generator(test_generator, steps=steps)
    test_generator.reset()
    probabilities = model.predict_generator(test_generator, steps=steps, verbose=1)
    probabilities = probabilities[: test_generator.samples]
    predicted_classes = np.argmax(probabilities, axis=1)
    true_classes = test_generator.classes
    ordered_names = [
        name for name, _ in sorted(saved_mapping.items(), key=lambda item: item[1])
    ]
    labels = list(range(len(ordered_names)))

    print("\nTest loss: {:.4f}".format(test_loss))
    print("Test accuracy: {:.4f}".format(test_accuracy))
    print("\nClassification report:\n")
    print(
        classification_report(
            true_classes,
            predicted_classes,
            labels=labels,
            target_names=ordered_names,
        )
    )

    matrix = confusion_matrix(true_classes, predicted_classes, labels=labels)
    figure, axis = plt.subplots(figsize=(9, 8))
    axis.imshow(matrix, interpolation="nearest", cmap="Blues")
    axis.set_xticks(labels)
    axis.set_yticks(labels)
    axis.set_xticklabels(ordered_names, rotation=45, ha="right")
    axis.set_yticklabels(ordered_names)
    axis.set_xlabel("Predicted label")
    axis.set_ylabel("True label")
    threshold = matrix.max() / 2.0 if matrix.max() > 0 else 0.5
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            axis.text(
                column,
                row,
                format(matrix[row, column], "d"),
                ha="center",
                va="center",
                color="white" if matrix[row, column] > threshold else "black",
            )
    axis.set_title("Fruit Freshness Classification Confusion Matrix")
    figure.tight_layout()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    output_path = args.output_directory / "confusion_matrix.png"
    figure.savefig(output_path)
    plt.close(figure)
    print("Saved confusion matrix: {}".format(output_path))


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate the CNN on held-out test images.")
    parser.add_argument("--dataset", type=Path, default=Path("dataset"))
    parser.add_argument("--model", type=Path, default=Path("model/fruit_freshness_cnn.h5"))
    parser.add_argument("--mapping", type=Path, default=Path("model/class_indices.json"))
    parser.add_argument("--output-directory", type=Path, default=Path("outputs"))
    parser.add_argument("--batch-size", type=int, default=32)
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        evaluate(args)
    except ModuleNotFoundError as error:
        print("Evaluation dependencies are missing: {}. Run: pip install -r requirements.txt".format(error))
        return 1
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as error:
        print("Evaluation could not be completed: {}".format(error))
        print("Prepare the dataset and train the model before evaluation.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
