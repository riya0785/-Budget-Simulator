from flask import Flask, render_template, request, jsonify, send_file
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from budget_simulator import BudgetSimulator, BudgetInput
import json

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
        csv_filename = f"simulation_{budget_input.monthly_income}_{budget_input.savings_goal}.csv"
        simulator.export_results_csv(csv_filename)
        results['csv_filename'] = csv_filename
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/download/<filename>')
def download_csv(filename):
    try:
        file_path = os.path.join('budget_simulator', filename)
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception:
        return jsonify({'error': 'File not found'}), 404

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
