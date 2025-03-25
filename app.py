from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from PIL import Image, UnidentifiedImageError
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part!", "error")
            return redirect(url_for("upload_file"))

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected!", "error")
            return redirect(url_for("upload_file"))

        try:
            # Open image to check format
            img = Image.open(file)

            # Ensure the image is actually a PNG
            if img.format != "PNG":
                flash("Only PNG files are allowed!", "error")
                return redirect(url_for("upload_file"))

            # Save the uploaded file
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Convert PNG to JPG
            rgb_img = img.convert("RGB")
            jpg_path = filepath.replace(".png", ".jpg")
            rgb_img.save(jpg_path, "JPEG")

            flash("File converted successfully!", "success")
            return send_file(jpg_path, as_attachment=True)

        except UnidentifiedImageError:
            flash("Invalid or corrupted image file!", "error")
            return redirect(url_for("upload_file"))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("upload_file"))

    return render_template("index.html")

if __name__=='__main__' :
    app.run(debug=True)