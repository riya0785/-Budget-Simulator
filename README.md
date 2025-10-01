# Budget Simulator

## What is Budget Simulator?

Budget Simulator is a web-based interactive tool designed to help users plan their financial future by simulating monthly income, fixed and variable expenses, and savings goals over a customizable time period. It provides visual insights into spending patterns, savings growth, and financial recommendations to optimize your budget.

---

## Why Use This Simulator?

- **Financial Clarity:** Visualize your income, expenses, and savings trends over time to make informed decisions.  
- **Dynamic Expense Modeling:** Realistic variations in expenses simulate real-life unpredictability.  
- **Personalized Recommendations:** Get tailored budgeting advice based on your simulation results to improve financial health.  
- **Customizable Duration:** Run simulations from 6 up to 24 months to fit your planning needs.  
- **Easy-to-Use Interface:** Friendly web UI with exportable reports and interactive charts.

---

## How to Use

### Prerequisites

- Python 3.11+ installed  
- Install dependencies via: pip install -r requirements.txt


### Setup and Run

1. Clone or download this repository.  
2. Navigate into the project folder via terminal.  
3. Run the app: python app.py
4. Open browser at `http://localhost:5000`.

### Inputs

- **Monthly Income:** Your total monthly earnings.  
- **Savings Goal:** The amount you aim to save monthly.  
- **Fixed Expenses:** Regular monthly costs like rent, insurance, etc.  
- **Variable Expenses:** Fluctuating expenses like groceries, entertainment.  
- **Simulation Length:** Number of months (e.g., 6, 12, 18) to simulate.

### Outputs

- **Monthly Savings and Expenses Summary** with interactive charts.  
- **Downloadable CSV Reports** to review detailed monthly data.  
- **Personalized Budgeting Recommendations** to improve your financial plan.

---

## Example Scenarios

### Scenario 1: Moderate Income, High Fixed Costs

- Income: 40000  
- Savings Goal: 7000  
- Fixed Expenses: Rent 18000, Insurance 4000, Loan 3000  
- Variable Expenses: Groceries 5000, Entertainment 2000, Transport 1500  
- Duration: 12 months  

Expected to highlight high fixed costs and suggest adjusting variable expenses.

### Scenario 2: Low Income, Balanced Spending

- Income: 15000  
- Savings Goal: 3000  
- Fixed Expenses: Rent 5000, Utilities 1500  
- Variable Expenses: Groceries 2000, Entertainment 1000  
- Duration: 12 months  

Expected balanced budget without warnings.

### Scenario 3: High Income, Aggressive Saving Goal

- Income: 100000  
- Savings Goal: 50000  
- Fixed Expenses: Mortgage 30000, Insurance 5000  
- Variable Expenses: Groceries 10000, Travel 5000, Entertainment 7000  
- Duration: 12 months  

Expected recommendations if saving goal is not met.

---

## Project Structure

- `src/`: Backend simulation logic Python code.  
- `templates/`: Jinja2 HTML templates.  
- `static/`: Javascript, CSS files.  
- `budget_simulator/`: Folder storing simulation CSV files.  
- `app.py`: Flask application entry point.

---

## Future Enhancements

- AI-powered expense forecasting and personalized advice using LLaMA or similar models.  
- User accounts and saving multiple scenarios.  
- PDF report export.  
- Mobile-optimized responsive UI.

---

## Contributing

Contributions are welcome! Fork the repo, open issues or PRs for improvements and bug fixes.

---

## License

This project is licensed under the MIT License.

