from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import csv
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from budget_simulator import BudgetSimulator, BudgetInput
import json

# Ensure downloads directory exists
downloads_dir = os.path.join('budget_simulator', 'downloads')
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate_budget():
    try:
        data = request.get_json()
        budget_input = BudgetInput(
            monthly_income=float(data['monthly_income']),
            fixed_expenses=data['fixed_expenses'],
            variable_expenses=data['variable_expenses'],
            savings_goal=float(data['savings_goal']),
            simulation_months=int(data.get('simulation_months', 12))
        )
        simulator = BudgetSimulator(budget_input)
        results = simulator.run_simulation()
        recommendations = simulator.generate_recommendations()
        results['recommendations'] = recommendations
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"budget_simulation_{timestamp}.csv"
        simulator.export_results_csv(csv_filename)
        results['csv_filename'] = csv_filename
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/download/<filename>')
def download_csv(filename):
    try:
        file_path = os.path.join('budget_simulator', 'downloads', filename)
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/csv/<filename>')
def view_csv(filename):
    try:
        file_path = os.path.join('budget_simulator', 'downloads', filename)
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        csv_data = []
        headers = []
        
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            for row in reader:
                # Convert numeric fields
                processed_row = {}
                for key, value in row.items():
                    try:
                        # Try to convert to float for numeric fields
                        if key in ['Income', 'Fixed_Expenses', 'Variable_Expenses', 
                                  'Total_Expenses', 'Monthly_Savings', 'Cumulative_Savings']:
                            processed_row[key] = float(value)
                        elif key == 'Month':
                            processed_row[key] = int(value)
                        elif key == 'Savings_Goal_Met':
                            processed_row[key] = value.lower() == 'true'
                        else:
                            processed_row[key] = value
                    except ValueError:
                        processed_row[key] = value
                csv_data.append(processed_row)
        
        return jsonify({
            'success': True, 
            'csv_data': csv_data,
            'headers': headers
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
