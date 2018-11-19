"""Train the six-class fruit freshness CNN from directory-based images."""

import argparse
import json
import math
import os


IMAGE_SIZE = (150, 150)
CLASS_NAMES = {
    "fresh_apple",
    "rotten_apple",
    "fresh_banana",
    "rotten_banana",
    "fresh_orange",
    "rotten_orange",
}


def require_class_directories(directory):
    if not os.path.isdir(directory):
        raise FileNotFoundError("Dataset directory does not exist: {}".format(directory))
    class_names = {
        name
        for name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, name))
    }
    if class_names != CLASS_NAMES:
        missing = sorted(CLASS_NAMES - class_names)
        unexpected = sorted(class_names - CLASS_NAMES)
        details = []
        if missing:
            details.append("missing: {}".format(", ".join(missing)))
        if unexpected:
            details.append("unexpected: {}".format(", ".join(unexpected)))
        raise ValueError("Invalid classes in {} ({})".format(directory, "; ".join(details)))


def build_model():
    from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
    from keras.models import Sequential

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(150, 150, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation="softmax"))
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def save_training_plots(history, output_directory):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    plt.figure(figsize=(8, 5))
    plt.plot(history.history["acc"], label="Training Accuracy")
    plt.plot(history.history["val_acc"], label="Validation Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, "training_accuracy.png"))
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, "training_loss.png"))
    plt.close()


def train(args):
    train_directory = os.path.join(args.dataset, "train")
    validation_directory = os.path.join(args.dataset, "validation")
    require_class_directories(train_directory)
    require_class_directories(validation_directory)

    from keras.preprocessing.image import ImageDataGenerator

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
        train_directory,
        target_size=IMAGE_SIZE,
        batch_size=args.batch_size,
        class_mode="categorical",
        shuffle=True,
        seed=args.seed,
    )
    validation_generator = validation_data.flow_from_directory(
        validation_directory,
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
    steps_per_epoch = max(1, int(math.ceil(training_generator.samples / float(args.batch_size))))
    validation_steps = max(1, int(math.ceil(validation_generator.samples / float(args.batch_size))))
    history = model.fit_generator(
        training_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=args.epochs,
        validation_data=validation_generator,
        validation_steps=validation_steps,
    )

    if not os.path.isdir(args.model_directory):
        os.makedirs(args.model_directory)
    model_path = os.path.join(args.model_directory, "fruit_freshness_cnn.h5")
    mapping_path = os.path.join(args.model_directory, "class_indices.json")
    model.save(model_path)
    with open(mapping_path, "w", encoding="utf-8") as mapping_file:
        json.dump(training_generator.class_indices, mapping_file, indent=2, sort_keys=True)
        mapping_file.write("\n")

    save_training_plots(history, args.output_directory)
    print("\nSaved model: {}".format(model_path))
    print("Saved class mapping: {}".format(mapping_path))
    print("Saved genuine training plots in: {}".format(args.output_directory))


def parse_args():
    parser = argparse.ArgumentParser(description="Train the fruit freshness CNN.")
    parser.add_argument("--dataset", default="dataset")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--model-directory", default="model")
    parser.add_argument("--output-directory", default="outputs")
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
