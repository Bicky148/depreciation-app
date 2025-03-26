from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

def calculate_depreciated_value(purchase_cost, eol_months, purchase_date, current_date):
    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    
    age_in_months = (current_date.year - purchase_date.year) * 12 + (current_date.month - purchase_date.month)
    depreciated_value = purchase_cost - (purchase_cost / eol_months * age_in_months)
    depreciated_value = max(depreciated_value, 0)
    
    return depreciated_value, age_in_months

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    purchase_costs = [float(x.strip()) for x in data['purchase_costs'].split(',') if x.strip()]
    purchase_dates = [x.strip() for x in data['purchase_dates'].split(',') if x.strip()]
    eol_option = data['eol_option']
    
    if len(purchase_costs) != len(purchase_dates):
        return jsonify({'error': 'Mismatch between costs and dates'}), 400
    
    if eol_option == "MAC":
        eol_months = 48
    elif eol_option == "WIN":
        eol_months = 36
    else:
        eol_months = int(data['custom_eol']) if data['custom_eol'].isdigit() else 0
    
    current_date = data['current_date']
    results = []
    
    for cost, date in zip(purchase_costs, purchase_dates):
        try:
            depreciated_value, age_in_months = calculate_depreciated_value(cost, eol_months, date, current_date)
            results.append({
                'purchase_cost': cost,
                'eol_months': eol_months,
                'purchase_date': date,
                'current_date': current_date,
                'age_in_months': age_in_months,
                'depreciated_value': round(depreciated_value, 2)
            })
        except ValueError:
            return jsonify({'error': f'Invalid date format for {date}'}), 400
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Creating templates/index.html for frontend
index_html = """\
<!DOCTYPE html>
<html>
<head>
    <title>Depreciation Calculator</title>
    <script>
        async function calculateDepreciation() {
            let purchase_costs = document.getElementById("purchase_costs").value;
            let purchase_dates = document.getElementById("purchase_dates").value;
            let eol_option = document.getElementById("eol_option").value;
            let custom_eol = document.getElementById("custom_eol").value;
            let current_date = document.getElementById("current_date").value;

            let response = await fetch("/calculate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ purchase_costs, purchase_dates, eol_option, custom_eol, current_date })
            });

            let result = await response.json();
            document.getElementById("results").innerText = JSON.stringify(result, null, 2);
        }
    </script>
</head>
<body>
    <h2>Asset Depreciation Calculator</h2>
    <label>Purchase Costs (comma-separated):</label>
    <input type="text" id="purchase_costs"><br>
    <label>Purchase Dates (YYYY-MM-DD, comma-separated):</label>
    <input type="text" id="purchase_dates"><br>
    <label>Select Platform:</label>
    <select id="eol_option">
        <option value="MAC">MAC</option>
        <option value="WIN">WIN</option>
        <option value="Custom">Custom</option>
    </select>
    <br>
    <label>Custom EOL (Months, if applicable):</label>
    <input type="text" id="custom_eol"><br>
    <label>Current Date:</label>
    <input type="date" id="current_date"><br>
    <button onclick="calculateDepreciation()">Calculate</button>
    <pre id="results"></pre>
</body>
</html>
"""

# Creating Dockerfile
dockerfile_content = """\
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install flask
CMD ["python", "app.py"]
"""

# Save frontend and Dockerfile
def save_files():
    with open("templates/index.html", "w") as f:
        f.write(index_html)
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)

save_files()
