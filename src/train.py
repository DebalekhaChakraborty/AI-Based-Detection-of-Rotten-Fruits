"""Train the six-class fruit freshness CNN from directory-based images."""

import argparse
import json
from pathlib import Path


IMAGE_SIZE = (150, 150)


def require_class_directories(directory):
    if not directory.is_dir():
        raise FileNotFoundError("Dataset directory does not exist: {}".format(directory))
    class_directories = [path for path in directory.iterdir() if path.is_dir()]
    if not class_directories:
        raise FileNotFoundError("No class directories found in: {}".format(directory))


def build_model():
    from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
    from tensorflow.keras.models import Sequential

    model = Sequential(
        [
            Conv2D(32, (3, 3), activation="relu", input_shape=(150, 150, 3)),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, (3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(128, (3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(128, activation="relu"),
            Dropout(0.5),
            Dense(6, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def save_training_plots(history, output_directory):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output_directory.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(history.history["accuracy"], label="Training Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_directory / "training_accuracy.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_directory / "training_loss.png")
    plt.close()


def train(args):
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    train_directory = args.dataset / "train"
    validation_directory = args.dataset / "validation"
    require_class_directories(train_directory)
    require_class_directories(validation_directory)

    training_data = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    validation_data = ImageDataGenerator(rescale=1.0 / 255)

    training_generator = training_data.flow_from_directory(
        str(train_directory),
        target_size=IMAGE_SIZE,
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=True,
        seed=args.seed,
    )
    validation_generator = validation_data.flow_from_directory(
        str(validation_directory),
        target_size=IMAGE_SIZE,
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=False,
    )

    if training_generator.num_classes != 6:
        raise ValueError(
            "Expected 6 training classes, found {}: {}".format(
                training_generator.num_classes, training_generator.class_indices
            )
        )
    if validation_generator.class_indices != training_generator.class_indices:
        raise ValueError("Training and validation class directories do not match.")

    model = build_model()
    model.summary()
    history = model.fit(
        training_generator,
        epochs=args.epochs,
        validation_data=validation_generator,
    )

    args.model_directory.mkdir(parents=True, exist_ok=True)
    model_path = args.model_directory / "fruit_freshness_cnn.h5"
    mapping_path = args.model_directory / "class_indices.json"
    model.save(str(model_path))
    with mapping_path.open("w", encoding="utf-8") as mapping_file:
        json.dump(training_generator.class_indices, mapping_file, indent=2, sort_keys=True)
        mapping_file.write("\n")

    save_training_plots(history, args.output_directory)
    print("\nSaved model: {}".format(model_path))
    print("Saved class mapping: {}".format(mapping_path))
    print("Saved genuine training plots in: {}".format(args.output_directory))


def parse_args():
    parser = argparse.ArgumentParser(description="Train the fruit freshness CNN.")
    parser.add_argument("--dataset", type=Path, default=Path("dataset"))
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--model-directory", type=Path, default=Path("model"))
    parser.add_argument("--output-directory", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        print("Training could not start: epochs and batch size must be positive.")
        return 1
    try:
        train(args)
    except ModuleNotFoundError as error:
        print("Training dependencies are missing: {}. Run: pip install -r requirements.txt".format(error))
        return 1
    except (FileNotFoundError, OSError, ValueError) as error:
        print("Training could not start: {}".format(error))
        print("Prepare the dataset first; see dataset/README.md.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

