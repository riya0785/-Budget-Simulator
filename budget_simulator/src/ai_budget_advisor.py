import ollama
import json
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import asdict


class AIBudgetAdvisor:
    """
    AI-powered budget advisor using Ollama LLM for intelligent financial recommendations
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.ollama_available = self._check_ollama_availability()
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama service is available and model exists"""
        try:
            models = ollama.list()
            available_models = [model for model in models]
            return any(self.model_name in model for model in available_models)
        except Exception as e:
            print(f"Ollama not available: {e}")
            return False
    
    def generate_recommendations(self, budget_input, simulation_results: List) -> List[str]:
        """
        Generate AI-powered budget recommendations based on simulation results
        
        Args:
            budget_input: BudgetInput object with user's financial parameters
            simulation_results: List of MonthlyResult objects from simulation
            
        Returns:
            List of recommendation strings
        """
        if not simulation_results:
            return ["No simulation results to analyze. Run simulation first."]
        
        # if not self.ollama_available:
        #     print("Ollama not available, using fallback recommendations")
        #     return self._get_fallback_recommendations(budget_input, simulation_results)
        
        try:
            # Prepare comprehensive budget analysis
            analysis_data = self._prepare_budget_analysis(budget_input, simulation_results)
            
            # Generate AI recommendations
            ai_recommendations = self._get_ai_recommendations(analysis_data)
            
            # Ensure we have quality recommendations
            if len(ai_recommendations) < 2:
                fallback_recs = self._get_fallback_recommendations(budget_input, simulation_results)
                ai_recommendations.extend(fallback_recs)
            
            return ai_recommendations[:6]  # Limit to 6 recommendations
            
        except Exception as e:
            print(f"AI recommendation generation failed: {e}")
            return self._get_fallback_recommendations(budget_input, simulation_results)
    
    def _prepare_budget_analysis(self, budget_input, simulation_results: List) -> Dict[str, Any]:
        """Prepare comprehensive financial analysis data for AI processing"""
        
        # Basic financial metrics
        total_months = 12
        avg_savings = sum(r.monthly_savings for r in simulation_results) / total_months
        total_income = sum(r.income for r in simulation_results)
        total_expenses = sum(r.total_expenses for r in simulation_results)
        savings_rate = (sum(r.monthly_savings for r in simulation_results) / total_income) * 100
        
        # Savings goal analysis
        months_goal_met = sum(1 for r in simulation_results if r.savings_goal_met)
        goal_achievement_rate = (months_goal_met / total_months) * 100
        
        # Expense pattern analysis
        variable_expense_analysis = self._analyze_variable_expenses(budget_input, simulation_results)
        
        # Financial stability metrics
        income_stability = self._calculate_income_stability(simulation_results)
        expense_volatility = self._calculate_expense_volatility(simulation_results)
        
        # Budget allocation ratios
        total_fixed = sum(budget_input.fixed_expenses.values())
        total_variable_budget = sum(budget_input.variable_expenses.values())
        fixed_ratio = (total_fixed / budget_input.monthly_income) * 100
        variable_ratio = (total_variable_budget / budget_input.monthly_income) * 100
        planned_savings_ratio = (budget_input.savings_goal / budget_input.monthly_income) * 100
        
        # Performance indicators
        best_month = max(simulation_results, key=lambda x: x.monthly_savings)
        worst_month = min(simulation_results, key=lambda x: x.monthly_savings)
        
        return {
            'monthly_income': budget_input.monthly_income,
            'savings_goal': budget_input.savings_goal,
            'simulation_months': total_months,
            'average_monthly_savings': avg_savings,
            'total_expenses': total_expenses,
            'actual_savings_rate': savings_rate,
            'planned_savings_ratio': planned_savings_ratio,
            'goal_achievement_rate': goal_achievement_rate,
            'fixed_expense_ratio': fixed_ratio,
            'variable_expense_ratio': variable_ratio,
            'income_stability_score': income_stability,
            'expense_volatility_score': expense_volatility,
            'fixed_expenses': dict(budget_input.fixed_expenses),
            'variable_expenses_budget': dict(budget_input.variable_expenses),
            'variable_expense_analysis': variable_expense_analysis,
            'best_month': {
                'month': best_month.month,
                'savings': best_month.monthly_savings,
                'expenses': best_month.total_expenses
            },
            'worst_month': {
                'month': worst_month.month,
                'savings': worst_month.monthly_savings,
                'expenses': worst_month.total_expenses
            },
            'final_cumulative_savings': simulation_results[-1].cumulative_savings,
            'savings_trend': self._calculate_savings_trend(simulation_results)
        }
    
    def _analyze_variable_expenses(self, budget_input, simulation_results: List) -> Dict[str, Dict]:
        """Analyze variable expense patterns across simulation"""
        analysis = {}
        
        for category in budget_input.variable_expenses.keys():
            category_expenses = [r.expense_variations[category] for r in simulation_results]
            budget_amount = budget_input.variable_expenses[category]
            
            avg_actual = np.mean(category_expenses)
            std_dev = np.std(category_expenses)
            min_spent = min(category_expenses)
            max_spent = max(category_expenses)
            
            # Calculate key metrics
            budget_adherence = (budget_amount - avg_actual) / budget_amount * 100
            volatility_ratio = std_dev / budget_amount if budget_amount > 0 else 0
            months_over_budget = sum(1 for exp in category_expenses if exp > budget_amount)
            
            analysis[category] = {
                'budget': budget_amount,
                'average_actual': avg_actual,
                'std_deviation': std_dev,
                'min_spent': min_spent,
                'max_spent': max_spent,
                'budget_adherence_pct': budget_adherence,
                'volatility_ratio': volatility_ratio,
                'months_over_budget': months_over_budget,
                'overspend_months_pct': (months_over_budget / len(simulation_results)) * 100
            }
        
        return analysis
    
    def _calculate_income_stability(self, simulation_results: List) -> float:
        """Calculate income stability score (0-1, higher is more stable)"""
        incomes = [r.income for r in simulation_results]
        if len(set(incomes)) == 1:  # All incomes are the same
            return 1.0
        
        cv = np.std(incomes) / np.mean(incomes)  # Coefficient of variation
        return max(0, 1 - cv)  # Convert to stability score
    
    def _calculate_expense_volatility(self, simulation_results: List) -> float:
        """Calculate expense volatility score (0-1, lower is better)"""
        expenses = [r.total_expenses for r in simulation_results]
        cv = np.std(expenses) / np.mean(expenses)  # Coefficient of variation
        return min(1, cv)  # Cap at 1
    
    def _calculate_savings_trend(self, simulation_results: List) -> str:
        """Analyze savings trend over time"""
        savings = [r.monthly_savings for r in simulation_results]
        
        if len(savings) < 3:
            return "insufficient_data"
        
        # Simple trend analysis using first half vs second half
        mid_point = len(savings) // 2
        first_half_avg = np.mean(savings[:mid_point])
        second_half_avg = np.mean(savings[mid_point:])
        
        diff_pct = ((second_half_avg - first_half_avg) / abs(first_half_avg)) * 100 if first_half_avg != 0 else 0
        
        if diff_pct > 10:
            return "improving"
        elif diff_pct < -10:
            return "declining"
        else:
            return "stable"
    
    def _get_ai_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations using Ollama LLM"""
        
        prompt = self._create_detailed_prompt(analysis_data)
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': '''You are a highly experienced certified financial planner and budget optimization expert. 
                        Your expertise includes personal finance, behavioral economics, and practical money management strategies.
                        
                        Analyze the provided budget simulation data and provide 3-4 specific, actionable recommendations 
                        focused on budget allocation optimization and financial improvement.
                        
                        Your recommendations should be:
                        - Specific and actionable (not generic advice)
                        - Prioritized by potential impact
                        - Realistic and achievable
                        - Based on the actual data patterns
                        - Include specific dollar amounts or percentages when relevant
                        - Provide advices for improving the savings rate and also ways to optimize budget allocations
                        - Address potential risks and how to mitigate them
                        - For each expense category, suggest specific budget adjustments based on historical data and trends.
                        
                        FORMATTING REQUIREMENTS:
                        - Start each recommendation with a clear, descriptive title using **Title** format
                        - Follow with detailed explanation in regular text
                        - Use **bold** for emphasis on important numbers, percentages, or key actions
                        - Use *italics* for category names or secondary emphasis
                        - Do NOT use markdown headers (# ## ###) 
                        - Each recommendation should be a complete paragraph
                        
                        Example format:
                        **Increase Grocery Budget Allocation** Based on your spending patterns, increase your *grocery* budget from $600 to **$660** (10% increase) as you exceed budget in **67%** of months. This will reduce financial stress and improve meal planning consistency.'''
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'num_predict': 800
                }
            )
            
            return self._parse_ai_response(response['message']['content'])
            
        except Exception as e:
            print(f"Ollama API call failed: {e}")
            return []
    
    def _create_detailed_prompt(self, data: Dict[str, Any]) -> str:
        """Create comprehensive prompt for AI analysis"""
        
        prompt = f"""
BUDGET SIMULATION ANALYSIS - {data['simulation_months']} MONTHS

INCOME & SAVINGS PERFORMANCE:
• Monthly Income: ${data['monthly_income']:,.2f}
• Savings Goal: ${data['savings_goal']:,.2f}/month ({data['planned_savings_ratio']:.1f}% of income)
• Actual Average Savings: ${data['average_monthly_savings']:,.2f}/month ({data['actual_savings_rate']:.1f}% of income)
• Goal Achievement Rate: {data['goal_achievement_rate']:.1f}% of months
• Savings Trend: {data['savings_trend']}
• Final Cumulative Savings: ${data['final_cumulative_savings']:,.2f}

EXPENSE ALLOCATION:
• Total Expenses: ${data['total_expenses']:,.2f}
• Fixed Expenses: {data['fixed_expense_ratio']:.1f}% of income (${sum(data['fixed_expenses'].values()):,.2f})
• Variable Expenses Budget: {data['variable_expense_ratio']:.1f}% of income (${sum(data['variable_expenses_budget'].values()):,.2f})

FIXED EXPENSE BREAKDOWN:"""
        
        for category, amount in data['fixed_expenses'].items():
            pct = (amount / data['monthly_income']) * 100
            prompt += f"\n  - {category}: ${amount:,.2f} ({pct:.1f}%)"
        
        prompt += "\n\nVARIABLE EXPENSE ANALYSIS:"
        for category, analysis in data['variable_expense_analysis'].items():
            prompt += f"""
  - {category}:
    Budget: ${analysis['budget']:.2f} | Actual Avg: ${analysis['average_actual']:.2f}
    Budget Adherence: {analysis['budget_adherence_pct']:+.1f}% | Volatility: {analysis['volatility_ratio']:.2f}
    Over-budget {analysis['months_over_budget']}/{data['simulation_months']} months ({analysis['overspend_months_pct']:.0f}%)"""
        
        prompt += f"""

FINANCIAL STABILITY METRICS:
• Income Stability Score: {data['income_stability_score']:.2f}/1.0
• Expense Volatility Score: {data['expense_volatility_score']:.2f}/1.0
• Best Month: Month {data['best_month']['month']} (${data['best_month']['savings']:,.2f} saved)
• Worst Month: Month {data['worst_month']['month']} (${data['worst_month']['savings']:,.2f} saved)

OPTIMIZATION PRIORITIES:
Based on this data, provide specific budget allocation recommendations that will:
1. Help achieve the ${data['savings_goal']:,.2f}/month savings goal more consistently
2. Optimize expense categories showing poor budget adherence or high volatility  
3. Improve overall financial stability and predictability
4. Suggest specific dollar amount adjustments to budget allocations

Focus on the most impactful changes this person can make to their budget allocation strategy."""

        return prompt
    
    def _parse_ai_response(self, ai_response: str) -> List[str]:
        """Parse AI response into clean recommendation list with HTML formatting"""
        
        lines = [line.strip() for line in ai_response.strip().split('\n') if line.strip()]
        recommendations = []
        current_rec = ""
        
        for line in lines:
            # Skip headers or very short lines
            if len(line) < 15 or line.isupper() or line.endswith(':'):
                continue
            
            # Check if this starts a new recommendation
            if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '-', '•', '*']) or \
               any(line.lower().startswith(verb) for verb in ['reduce', 'increase', 'allocate', 'consider', 'adjust', 'review', 'create', 'establish', 'set', 'implement', 'focus', 'prioritize']):
                
                if current_rec:
                    recommendations.append(current_rec.strip())
                current_rec = line
            else:
                current_rec += " " + line
        
        # Add the last recommendation
        if current_rec:
            recommendations.append(current_rec.strip())
        
        # Clean up recommendations and apply HTML formatting
        cleaned = []
        for rec in recommendations:
            # Remove numbering and bullets
            rec = rec.lstrip('1234567890.-•* ').strip()
            
            # Only keep substantial recommendations
            if len(rec) > 30 and not rec.lower().startswith('here') and not rec.lower().startswith('based on'):
                # Convert markdown formatting to HTML
                formatted_rec = self._convert_markdown_to_html(rec)
                # Additional cleanup for common AI formatting issues
                formatted_rec = self._final_format_cleanup(formatted_rec)
                cleaned.append(formatted_rec)
        
        return cleaned
    
    def _final_format_cleanup(self, text: str) -> str:
        """Final cleanup of formatting issues"""
        import re
        
        # Ensure the first word/phrase is properly bolded if it looks like a title
        # Pattern: "Word1 Word2 Word3" at start -> "<strong>Word1 Word2 Word3</strong>"
        if not text.startswith('<strong>'):
            # Look for title-like patterns at the beginning
            title_match = re.match(r'^([A-Z][a-z]*(?:\s+[A-Z][a-z]*)*(?:\s+[A-Z][a-z]*)*)\s+', text)
            if title_match:
                title = title_match.group(1)
                # Check if it's likely a title (2-4 words, title case)
                words = title.split()
                if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words):
                    text = f'<strong>{title}</strong> {text[len(title):].strip()}'
        
        # Remove any duplicate spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Ensure proper sentence structure
        text = text.strip()
        if text and not text.endswith('.'):
            text += '.'
        
        return text
    
    def _convert_markdown_to_html(self, text: str) -> str:
        """Convert markdown formatting to HTML tags"""
        import re
        
        # Handle unmatched ** at the end of titles (common AI formatting issue)
        # Look for patterns like "Title** Some text" and convert to "**Title** Some text"
        text = re.sub(r'^([^*]+)\*\*\s+', r'**\1** ', text)
        
        # Convert **text** to <strong>text</strong>
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        
        # Convert *text* to <em>text</em> (but only if not part of **)
        text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
        
        # Convert __text__ to <strong>text</strong> (alternative bold)
        text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
        
        # Convert _text_ to <em>text</em> (alternative italic)
        text = re.sub(r'(?<!_)_([^_]+?)_(?!_)', r'<em>\1</em>', text)
        
        # Convert `code` to <code>code</code>
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        
        # Handle common AI formatting mistakes
        # Fix "Title** " -> "<strong>Title</strong> "
        text = re.sub(r'^([A-Z][^*]*?)\*\*\s*', r'<strong>\1</strong> ', text)
        
        # Clean up any remaining unpaired ** or *
        text = re.sub(r'\*\*(?![^<]*>)', '', text)  # Remove ** not inside HTML tags
        text = re.sub(r'(?<![<>])\*(?![^<]*>)', '', text)  # Remove * not inside HTML tags
        
        # Ensure proper spacing around HTML tags
        text = re.sub(r'<strong>\s*', '<strong>', text)
        text = re.sub(r'\s*</strong>', '</strong>', text)
        text = re.sub(r'<em>\s*', '<em>', text)
        text = re.sub(r'\s*</em>', '</em>', text)
        
        return text.strip()
    
    def _get_fallback_recommendations(self, budget_input, simulation_results: List) -> List[str]:
        """Rule-based fallback recommendations when AI is unavailable"""
        
        recommendations = []
        
        if not simulation_results:
            return ["No simulation data available for analysis."]
        
        # Prepare basic analysis for fallback
        avg_savings = sum(r.monthly_savings for r in simulation_results) / len(simulation_results)
        months_goal_met = sum(1 for r in simulation_results if r.savings_goal_met)
        goal_achievement_rate = (months_goal_met / len(simulation_results)) * 100
        
        total_fixed = sum(budget_input.fixed_expenses.values())
        fixed_ratio = (total_fixed / budget_input.monthly_income) * 100
        
        # Savings shortfall analysis
        if avg_savings < budget_input.savings_goal:
            shortfall = budget_input.savings_goal - avg_savings
            recommendations.append(
                f"Increase your monthly savings by ${shortfall:.2f} to meet your ${budget_input.savings_goal:.2f} goal. "
                f"Consider reducing variable expenses or negotiating lower fixed costs."
            )
        
        # Fixed expense ratio check
        if fixed_ratio > 50:
            recommendations.append(
                f"Your fixed expenses consume {fixed_ratio:.1f}% of income, which is quite high. "
                f"Target reducing fixed costs by 10-15% through renegotiating rent, insurance, or subscriptions."
            )
        elif fixed_ratio > 40:
            recommendations.append(
                f"Fixed expenses at {fixed_ratio:.1f}% of income limit financial flexibility. "
                f"Look for opportunities to reduce by ${total_fixed * 0.1:.2f}/month."
            )
        
        # Variable expense analysis
        high_variance_categories = []
        overspend_categories = []
        
        for category, budget_amount in budget_input.variable_expenses.items():
            actual_expenses = [r.expense_variations[category] for r in simulation_results]
            avg_actual = sum(actual_expenses) / len(actual_expenses)
            std_dev = np.std(actual_expenses)
            
            if std_dev > 0.2 * budget_amount:
                high_variance_categories.append(category)
            
            if avg_actual > budget_amount * 1.1:
                overspend_categories.append((category, avg_actual - budget_amount))
        
        if overspend_categories:
            category_text = ", ".join([f"{cat} (${overspend:.2f} over)" for cat, overspend in overspend_categories])
            recommendations.append(
                f"Consistently overspending in: {category_text}. "
                f"Increase these budget allocations or implement stricter spending controls."
            )
        
        if high_variance_categories:
            recommendations.append(
                f"High spending volatility in {', '.join(high_variance_categories)}. "
                f"Create weekly spending targets and track expenses more closely in these categories."
            )
        
        # Goal achievement analysis
        if goal_achievement_rate < 30:
            recommendations.append(
                f"Only achieved savings goal in {goal_achievement_rate:.0f}% of months. "
                f"Consider reducing your monthly savings target to ${budget_input.savings_goal * 0.8:.2f} "
                f"to build consistency, then gradually increase."
            )
        
        # Emergency fund recommendation
        if simulation_results[-1].cumulative_savings < budget_input.monthly_income * 3:
            recommendations.append(
                f"Build an emergency fund of ${budget_input.monthly_income * 3:.2f} (3 months expenses) "
                f"before focusing on other financial goals."
            )
        
        if not recommendations:
            recommendations.append(
                f"Your budget is well-balanced with a {goal_achievement_rate:.0f}% savings goal success rate. "
                f"Continue monitoring and consider gradually increasing your savings target."
            )
        
        return recommendations


# Utility function to integrate with existing BudgetSimulator
def create_ai_advisor(model_name: str = "llama3.2") -> AIBudgetAdvisor:
    """
    Factory function to create AI budget advisor
    
    Args:
        model_name: Name of Ollama model to use (default: llama3.2)
        
    Returns:
        AIBudgetAdvisor instance
    """
    return AIBudgetAdvisor(model_name)