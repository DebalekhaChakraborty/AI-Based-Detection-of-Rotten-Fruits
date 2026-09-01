"""Classify one image with the trained fruit freshness CNN."""

import argparse
import json
import os
from functools import lru_cache


DEFAULT_MODEL = "model/fruit_freshness_cnn.h5"
DEFAULT_MAPPING = "model/class_indices.json"


def load_class_names(mapping_path):
    if not os.path.isfile(mapping_path):
        raise FileNotFoundError(
            "Class mapping not found: {}. Train the model first.".format(mapping_path)
        )
    with open(mapping_path, "r", encoding="utf-8") as mapping_file:
        class_indices = json.load(mapping_file)
    if not isinstance(class_indices, dict) or len(class_indices) != 6:
        raise ValueError("Class mapping must contain exactly six classes.")
    return {int(index): class_name for class_name, index in class_indices.items()}


@lru_cache(maxsize=4)
def load_trained_model(model_path):
    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            "Trained model not found: {}. Run python src/train.py first.".format(model_path)
        )
    from keras.models import load_model

    return load_model(model_path, compile=False)


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
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image not found: {}".format(image_path))
    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            "Trained model not found: {}. Run python src/train.py first.".format(model_path)
        )

    class_names = load_class_names(mapping_path)
    import numpy as np
    from keras.preprocessing.image import img_to_array
    from keras.preprocessing.image import load_img

    model = load_trained_model(os.path.abspath(model_path))
    loaded_image = load_img(image_path, target_size=(150, 150))
    image_array = img_to_array(loaded_image).astype("float32") / 255.0
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
    parser.add_argument("image", help="Path to an apple, banana, or orange image")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--mapping", default=DEFAULT_MAPPING)
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
    print("AI-Based Detection of Rotten Fruits Using CNN\n")
    print("Fruit       : {}".format(result["fruit"]))
    print("Condition   : {}".format(result["condition"]))
    print("Prediction  : {}".format(result["prediction"]))
    print("Confidence  : {:.2f}%".format(result["confidence"]))
    print("---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
