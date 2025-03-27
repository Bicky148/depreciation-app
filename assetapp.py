from flask import Flask, render_template, request
from datetime import datetime
import calendar

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    depreciated_value = None
    age_in_months = None

    if request.method == "POST":
        purchase_date = request.form["purchase_date"]
        purchase_cost = float(request.form["purchase_cost"])
        device_type = request.form["device_type"]

        # Determine End-of-Life months
        eol_months = 48 if device_type == "Mac" else 36

        # Convert purchase_date to datetime
        purchase_date_obj = datetime.strptime(purchase_date, "%Y-%m-%d")
        current_date = datetime.today()

        # Calculate age in months
        age_in_months = (current_date.year - purchase_date_obj.year) * 12 + (current_date.month - purchase_date_obj.month)

        # Calculate depreciated value
        depreciated_value = purchase_cost - (purchase_cost / eol_months * age_in_months)
        depreciated_value = max(depreciated_value, 0)  # Ensure it doesn't go below 0

    return render_template("index.html", depreciated_value=depreciated_value, age_in_months=age_in_months)

if __name__ == "__main__":
    app.run(debug=True)
