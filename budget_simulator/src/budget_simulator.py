import random
import numpy as np
import os
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class BudgetInput:
    monthly_income: float
    fixed_expenses: Dict[str, float]
    variable_expenses: Dict[str, float]
    savings_goal: float
    simulation_months: int = 12


@dataclass
class MonthlyResult:
    month: int
    income: float
    fixed_expenses: float
    variable_expenses: float
    total_expenses: float
    monthly_savings: float
    cumulative_savings: float
    savings_goal_met: bool
    expense_variations: Dict[str, float]


class BudgetSimulator:
    def __init__(self, budget_input: BudgetInput):
        self.budget_input = budget_input
        self.results: List[MonthlyResult] = []

    def simulate_variable_expenses(self, base_expenses: Dict[str, float], month: int) -> Dict[str, float]:
        varied_expenses = {}
        for category, base_amount in base_expenses.items():
            seasonal_factor = 1.0
            if month in [12, 1]:
                seasonal_factor = 1.15
            elif month in [2, 3]:
                seasonal_factor = 0.90
            elif month in [7, 8]:
                seasonal_factor = 1.10
            random_variation = random.uniform(0.85, 1.15)
            varied_amount = base_amount * seasonal_factor * random_variation
            varied_expenses[category] = round(varied_amount, 2)
        return varied_expenses

    def simulate_income_variation(self, base_income: float, month: int) -> float:
        if random.random() < 0.8:
            return base_income
        else:
            variation = random.uniform(0.95, 1.05)
            return round(base_income * variation, 2)

    def run_simulation(self) -> Dict[str, Any]:
        self.results = []
        cumulative_savings = 0
        months_goal_met = 0
        for month in range(1, self.budget_input.simulation_months + 1):
            monthly_income = self.simulate_income_variation(self.budget_input.monthly_income, month)
            fixed_total = sum(self.budget_input.fixed_expenses.values())
            varied_variable_expenses = self.simulate_variable_expenses(self.budget_input.variable_expenses, month)
            variable_total = sum(varied_variable_expenses.values())
            total_expenses = fixed_total + variable_total
            monthly_savings = monthly_income - total_expenses
            cumulative_savings += monthly_savings
            savings_goal_met = monthly_savings >= self.budget_input.savings_goal
            if savings_goal_met:
                months_goal_met += 1
            month_result = MonthlyResult(
                month=month,
                income=monthly_income,
                fixed_expenses=fixed_total,
                variable_expenses=variable_total,
                total_expenses=total_expenses,
                monthly_savings=monthly_savings,
                cumulative_savings=cumulative_savings,
                savings_goal_met=savings_goal_met,
                expense_variations=varied_variable_expenses
            )
            self.results.append(month_result)
        summary = self._generate_summary(months_goal_met)
        return {
            'monthly_results': [asdict(result) for result in self.results],
            'summary': summary,
            'input_parameters': asdict(self.budget_input)
        }

    def _generate_summary(self, months_goal_met: int) -> Dict[str, Any]:
        if not self.results:
            return {}
        total_income = sum(result.income for result in self.results)
        total_expenses = sum(result.total_expenses for result in self.results)
        average_monthly_savings = sum(result.monthly_savings for result in self.results) / len(self.results)
        final_cumulative_savings = self.results[-1].cumulative_savings
        savings_goal_percentage = (months_goal_met / len(self.results)) * 100
        min_monthly_savings = min(result.monthly_savings for result in self.results)
        max_monthly_savings = max(result.monthly_savings for result in self.results)
        best_month = max(self.results, key=lambda x: x.monthly_savings)
        worst_month = min(self.results, key=lambda x: x.monthly_savings)
        return {
            'total_income': round(total_income, 2),
            'total_expenses': round(total_expenses, 2),
            'average_monthly_savings': round(average_monthly_savings, 2),
            'final_cumulative_savings': round(final_cumulative_savings, 2),
            'months_goal_met': months_goal_met,
            'savings_goal_percentage': round(savings_goal_percentage, 1),
            'min_monthly_savings': round(min_monthly_savings, 2),
            'max_monthly_savings': round(max_monthly_savings, 2),
            'best_month': {
                'month': best_month.month,
                'savings': round(best_month.monthly_savings, 2)
            },
            'worst_month': {
                'month': worst_month.month,
                'savings': round(worst_month.monthly_savings, 2)
            },
            'savings_volatility': round(max_monthly_savings - min_monthly_savings, 2)
        }

    def export_results_csv(self, filename: str = "synthetic_budget_simulator_extended.csv") -> str:
        if not self.results:
            return "No simulation results to export. Run simulation first."
        directory = "budget_simulator"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = [
                'Month', 'Income', 'Fixed_Expenses', 'Variable_Expenses',
                'Total_Expenses', 'Monthly_Savings', 'Cumulative_Savings',
                'Savings_Goal_Met'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'Month': result.month,
                    'Income': result.income,
                    'Fixed_Expenses': result.fixed_expenses,
                    'Variable_Expenses': result.variable_expenses,
                    'Total_Expenses': result.total_expenses,
                    'Monthly_Savings': result.monthly_savings,
                    'Cumulative_Savings': result.cumulative_savings,
                    'Savings_Goal_Met': result.savings_goal_met
                })
        return f"Results exported to {filepath}"

    def generate_recommendations(self) -> List[str]:
        recommendations = []
        if not self.results:
            return ["No simulation results to analyze. Run simulation first."]
        savings_goal = self.budget_input.savings_goal
        avg_savings = sum(r.monthly_savings for r in self.results) / len(self.results)
        if avg_savings < savings_goal:
            recommendations.append(
                "Your average monthly savings are below your savings goal. "
                "Consider reducing some variable expenses."
            )
        variable_expenses_by_category = {key: [] for key in self.budget_input.variable_expenses.keys()}
        for result in self.results:
            for category, value in result.expense_variations.items():
                variable_expenses_by_category[category].append(value)
        high_variability = []
        for category, values in variable_expenses_by_category.items():
            std_dev = np.std(values)
            if std_dev > 0.1 * self.budget_input.variable_expenses[category]:
                high_variability.append((category, std_dev))
        if high_variability:
            rec_text = "High variability detected in variable expenses: "
            rec_text += ", ".join(f"{c} (std dev: {v:.2f})" for c, v in high_variability)
            rec_text += ". Consider budgeting cautiously for these items."
            recommendations.append(rec_text)
        total_fixed = sum(self.budget_input.fixed_expenses.values())
        monthly_income = self.budget_input.monthly_income
        if total_fixed > 0.4 * monthly_income:
            recommendations.append(
                "Fixed expenses occupy over 40% of your monthly income. "
                "Look into renegotiating or reducing fixed costs like rent or insurance."
            )
        if not recommendations:
            recommendations.append("Your budget looks well balanced. Keep up the good work!")
        return recommendations
