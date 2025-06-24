from flask import Flask, flash, g, redirect, render_template, request, url_for

from configs import Config
from db_helpers import close_db, run_query, run_exec


# Configure application
app = Flask(__name__)  
app.config.from_object(Config)

app.teardown_appcontext(close_db)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():

    birthdays = run_query("SELECT * FROM birthdays")

    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")

        if not name or not date:
            error = "Please, complete the form."
            return render_template("index.html", error=error, birthdays=birthdays)

        # Check if the name already exists in the database
        existing = run_query("SELECT 1 FROM birthdays WHERE name = {} AND date = {}", name, date)

        if existing:
            error = f"{name}'s birthday is already in the database."
            return render_template("index.html", error=error, birthdays=birthdays)

        run_exec("INSERT INTO birthdays (name, date) VALUES({}, {})", name, date)
        flash("Birthday added successfully", "success")
        return redirect(url_for("index"))

    return render_template("index.html", birthdays=birthdays)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        
        run_exec("UPDATE birthdays SET name = {}, date = {} WHERE id = {}", name, date, id)
        flash("Updated successfully", "info")
        return redirect(url_for("index"))

    row = run_query("SELECT * FROM birthdays WHERE id = {}", id)

    if not row:
        flash("Birthday not found", "error")
        return redirect(url_for("index"))

    name = row[0]["name"]
    date = row[0]["date"]

    return render_template("update.html", id=id, name=name, date=date)


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    run_exec("DELETE FROM birthdays WHERE id = {}", id)
    flash("Deleted", "warning")
    return redirect(url_for("index"))
