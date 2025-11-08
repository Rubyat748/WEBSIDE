from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os, json

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Folders
UPLOAD_FOLDER = "static/assets/planet_placeholders"
PLANET_DB = "planets.json"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------- Load planet data --------
def load_planets():
    if not os.path.exists(PLANET_DB):
        return []
    with open(PLANET_DB, "r") as f:
        return json.load(f)

def save_planets(planets):
    with open(PLANET_DB, "w") as f:
        json.dump(planets, f, indent=4)

# -------- Routes --------
@app.route("/")
def index():
    planets = load_planets()
    return render_template("index.html", planets=planets)

@app.route("/compare")
def compare():
    planets = load_planets()
    return render_template("compare.html", planets=planets)

@app.route("/about")
def about():
    return render_template("about.html")

# -------- Admin --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["admin"] = True
            return redirect(url_for("admin_panel"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("login"))

    planets = load_planets()

    if request.method == "POST":
        name = request.form["name"]
        size = request.form["size"]
        distance = request.form["distance"]
        fact = request.form["fact"]
        image = request.files["image"]

        if image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            img_path = f"static/assets/planet_placeholders/{filename}"
        else:
            img_path = "static/assets/planet_placeholders/placeholder.jpg"

        new_planet = {
            "name": name,
            "size": size,
            "distance": distance,
            "fact": fact,
            "image": img_path
        }

        planets.append(new_planet)
        save_planets(planets)
        return redirect(url_for("admin_panel"))

    return render_template("admin.html", planets=planets)

@app.route("/delete/<name>")
def delete_planet(name):
    if not session.get("admin"):
        return redirect(url_for("login"))
    planets = load_planets()
    planets = [p for p in planets if p["name"] != name]
    save_planets(planets)
    return redirect(url_for("admin_panel"))

# -------- API --------
@app.route("/api/planets")
def api_planets():
    return jsonify(load_planets())

if __name__ == "__main__":
    app.run(debug=True)
