from flask import Flask, render_template, request, jsonify
from datetime import datetime

def calculate_depreciated_value(purchase_cost, eol_months, purchase_date, current_date):
    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    
    age_in_months = (current_date.year - purchase_date.year) * 12 + (current_date.month - purchase_date.month)
    depreciated_value = purchase_cost - (purchase_cost / eol_months * age_in_months)
    depreciated_value = max(depreciated_value, 0)
    
    return depreciated_value, age_in_months

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            purchase_costs = [float(cost.strip()) for cost in request.form['purchase_costs'].split(',') if cost.strip()]
            purchase_dates = [date.strip() for date in request.form['purchase_dates'].split(',') if date.strip()]
            eol_option = request.form['eol_option']
            custom_eol = request.form.get('custom_eol', '0')
            current_date = request.form['current_date']
            
            if len(purchase_costs) != len(purchase_dates):
                return jsonify({"error": "The number of purchase costs must match the number of purchase dates."})
            
            eol_months = 48 if eol_option == "MAC" else 36 if eol_option == "WIN" else int(custom_eol or 0)
            
            results = []
            for cost, date in zip(purchase_costs, purchase_dates):
                try:
                    depreciated_value, age_in_months = calculate_depreciated_value(cost, eol_months, date, current_date)
                    results.append({
                        "purchase_cost": cost,
                        "eol_months": eol_months,
                        "purchase_date": date,
                        "current_date": current_date,
                        "age_in_months": age_in_months,
                        "depreciated_value": f"{depreciated_value:.2f}"
                    })
                except ValueError:
                    return jsonify({"error": f"Invalid date format for: {date}"})
            
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
