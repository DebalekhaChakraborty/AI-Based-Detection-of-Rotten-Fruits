"""Small Flask demonstration for the trained fruit freshness CNN."""

import os
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from src.predict import predict_image


BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = os.path.join(BASE_DIRECTORY, "static", "uploads")
MODEL_PATH = os.path.join(BASE_DIRECTORY, "model", "fruit_freshness_cnn.h5")
MAPPING_PATH = os.path.join(BASE_DIRECTORY, "model", "class_indices.json")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "fruit-freshness-local-demo"
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    uploaded_file = request.files.get("image")
    if uploaded_file is None or not uploaded_file.filename:
        flash("Choose an image before selecting Predict.")
        return redirect(url_for("index"))
    if not allowed_file(uploaded_file.filename):
        flash("Use a JPG, JPEG, PNG, or BMP image.")
        return redirect(url_for("index"))

    original_name = secure_filename(uploaded_file.filename)
    stored_name = "{}_{}".format(uuid4().hex, original_name)
    if not os.path.isdir(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    image_path = os.path.join(UPLOAD_DIRECTORY, stored_name)
    uploaded_file.save(image_path)

    try:
        result = predict_image(image_path, MODEL_PATH, MAPPING_PATH)
    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError) as error:
        if os.path.isfile(image_path):
            os.remove(image_path)
        flash(str(error))
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        result=result,
        image_url=url_for("static", filename="uploads/{}".format(stored_name)),
    )


@app.errorhandler(413)
def image_too_large(_error):
    flash("The selected image is larger than the 8 MB upload limit.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
