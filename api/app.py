import os
import sys
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, url_for

# Configure application
app = Flask(__name__)  

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = 'C1lrw@M=YGMk+-e#'

if not os.path.exists("/tmp"):
    os.makedirs("/tmp")
    
if sys.platform == "win32":
    db_path = "birthdays.db"  
else:
    db_path = "/tmp/birthdays.db"  

# Configure CS50 Library to use SQLite database
db = SQL(f"sqlite:///{db_path}")

db.execute("""
    CREATE TABLE IF NOT EXISTS birthdays (
        id INTEGER,
        name TEXT NOT NULL,
        date TEXT,
        PRIMARY KEY(id)
    )
""")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    birthdays = db.execute("SELECT * FROM birthdays;")

    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")

        if not name or not date:
            error = "Please, complete the form."
            return render_template("index.html", error=error, birthdays=birthdays)

        # Check if the name already exists in the database
        existing = db.execute("SELECT 1 FROM birthdays WHERE name=?", name)

        if existing:
            error = f"{name}'s birthday is already on the database."
            return render_template("index.html", error=error, birthdays=birthdays)

        db.execute("INSERT INTO birthdays (name, date) VALUES(?, ?)", name, date)
        flash("Birthday added successfully", "success")
        return redirect(url_for("index"))

    return render_template("index.html", birthdays=birthdays)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")

        db.execute("UPDATE birthdays SET name = ?, date = ? WHERE id = ?", name, date, id)
        flash("Updated successfully", "info")
        return redirect(url_for("index"))

    row = db.execute("SELECT * FROM birthdays WHERE id = ?", id)

    if not row:
        flash("Birthday not found", "error")
        return redirect(url_for("index"))

    name = row[0]["name"]
    date = row[0]["date"]

    return render_template("update.html", id=id, name=name, date=date)


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    flash("Deleted", "warning")
    return redirect(url_for("index"))
