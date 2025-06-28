from flask import Flask, flash, redirect, render_template, request, url_for

from configs import Config
from helpers import close_db, run_query, run_exec, format_date, get_days_until


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
    if request.method == "POST":
        name = request.form.get("name")
        birthday_date = request.form.get("birthday")

        if not name or not birthday_date:
            flash("Please complete the form.", "error")
            return redirect(url_for("index"))

        # Check if the name and date combination already exists
        existing = run_query("SELECT 1 FROM birthdays WHERE name = {} AND date = {}", name, birthday_date)

        if existing:
            flash(f"This birthday is already in the database.", "error")
            return redirect(url_for("index"))

        run_exec("INSERT INTO birthdays (name, date) VALUES({}, {})", name, birthday_date)
        flash("Birthday added successfully! 🎉", "success")
        return redirect(url_for("index"))


    birthdays = run_query("SELECT * FROM birthdays")
    for birthday in birthdays:
        birthday['formatted_date'] = format_date(birthday['date'])
        birthday['days_until'] = get_days_until(birthday['date'])

    return render_template("index.html", birthdays=birthdays)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "POST":
        name = request.form.get("name")
        birthday_date = request.form.get("birthday")
        
        run_exec("UPDATE birthdays SET name = {}, date = {} WHERE id = {}", name, birthday_date, id)
        flash("Birthday updated successfully! ✨", "success")
        return redirect(url_for("index"))

    row = run_query("SELECT * FROM birthdays WHERE id = {}", id)

    if not row:
        flash("Birthday not found", "error")
        return redirect(url_for("index"))

    birthday = row[0]

    return render_template("update.html", birthday=birthday)


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    existing = run_query("SELECT name FROM birthdays WHERE id = {}", id)
    
    if not existing:
        flash("Birthday not found.", "error")
    else:
        run_exec("DELETE FROM birthdays WHERE id = {}", id)
        flash(f"Birthday deleted successfully!", "error")
    
    return redirect(url_for("index"))
