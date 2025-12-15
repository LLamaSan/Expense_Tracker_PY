from flask import Flask, render_template, request, redirect, url_for
from datetime import date

from db import (
    init_db,
    add_expense,
    delete_expense,
    get_total_expense,
    get_filtered_expenses,
    get_expense_by_id,
    update_expense,
    get_category_totals
)

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    category = request.args.get("category")
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    expenses = get_filtered_expenses(category, start_date, end_date)
    total = get_total_expense()
    category_totals = get_category_totals()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_totals=category_totals,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add():
    add_expense(
        request.form["amount"],
        request.form["category"],
        request.form["description"],
        request.form["date"]
    )
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        update_expense(
            id,
            request.form["amount"],
            request.form["category"],
            request.form["description"],
            request.form["date"]
        )
        return redirect(url_for("index"))

    expense = get_expense_by_id(id)
    return render_template("edit.html", expense=expense)


if __name__ == "__main__":
    app.run(debug=True)
