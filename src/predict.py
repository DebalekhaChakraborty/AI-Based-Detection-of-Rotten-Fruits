"""Classify one image with the trained fruit freshness CNN."""

import argparse
import json
from functools import lru_cache
from pathlib import Path


DEFAULT_MODEL = Path("model/fruit_freshness_cnn.h5")
DEFAULT_MAPPING = Path("model/class_indices.json")


def load_class_names(mapping_path):
    if not mapping_path.is_file():
        raise FileNotFoundError(
            "Class mapping not found: {}. Train the model first.".format(mapping_path)
        )
    with mapping_path.open("r", encoding="utf-8") as mapping_file:
        class_indices = json.load(mapping_file)
    if not isinstance(class_indices, dict) or len(class_indices) != 6:
        raise ValueError("Class mapping must contain exactly six classes.")
    return {int(index): class_name for class_name, index in class_indices.items()}


@lru_cache(maxsize=4)
def load_trained_model(model_path_string):
    model_path = Path(model_path_string)
    if not model_path.is_file():
        raise FileNotFoundError(
            "Trained model not found: {}. Run python src/train.py first.".format(model_path)
        )
    from keras.models import load_model

    return load_model(str(model_path), compile=False)


def label_details(class_name):
    try:
        condition, fruit = class_name.split("_", 1)
    except ValueError as error:
        raise ValueError("Unexpected class label: {}".format(class_name)) from error
    return {
        "fruit": fruit.replace("_", " ").title(),
        "condition": condition.title(),
        "prediction": "{} {}".format(condition.title(), fruit.replace("_", " ").title()),
    }


def predict_image(image_path, model_path=DEFAULT_MODEL, mapping_path=DEFAULT_MAPPING):
    image_path = Path(image_path)
    model_path = Path(model_path)
    mapping_path = Path(mapping_path)
    if not image_path.is_file():
        raise FileNotFoundError("Image not found: {}".format(image_path))
    if not model_path.is_file():
        raise FileNotFoundError(
            "Trained model not found: {}. Run python src/train.py first.".format(model_path)
        )

    class_names = load_class_names(mapping_path)
    import numpy as np
    from keras.preprocessing.image import img_to_array, load_img

    model = load_trained_model(str(model_path.resolve()))
    image = load_img(str(image_path), target_size=(150, 150), color_mode="rgb")
    image_array = img_to_array(image).astype("float32") / 255.0
    batch = np.expand_dims(image_array, axis=0)
    probabilities = model.predict(batch, verbose=0)[0]
    predicted_index = int(np.argmax(probabilities))
    if predicted_index not in class_names:
        raise ValueError("Predicted index is absent from the saved class mapping.")

    result = label_details(class_names[predicted_index])
    result["class_name"] = class_names[predicted_index]
    result["confidence"] = float(probabilities[predicted_index]) * 100.0
    return result


def parse_args():
    parser = argparse.ArgumentParser(description="Classify one fruit image.")
    parser.add_argument("image", type=Path, help="Path to an apple, banana, or orange image")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        result = predict_image(args.image, args.model, args.mapping)
    except ModuleNotFoundError as error:
        print("Prediction dependencies are missing: {}. Run: pip install -r requirements.txt".format(error))
        return 1
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as error:
        print("Prediction could not be completed: {}".format(error))
        return 1

    print("\n---")
    print("Fruit Quality Detection Using CNN\n")
    print("Fruit       : {}".format(result["fruit"]))
    print("Condition   : {}".format(result["condition"]))
    print("Prediction  : {}".format(result["prediction"]))
    print("Confidence  : {:.2f}%".format(result["confidence"]))
    print("---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
