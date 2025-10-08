# AI Budget Advisor Setup Guide

## Overview
The Budget Simulator now includes an AI-powered recommendation engine using Ollama LLM that provides personalized, intelligent budget allocation advice based on your simulation results.

## Prerequisites

### 1. Install Ollama
Download and install Ollama from: https://ollama.ai/

### 2. Pull a Language Model
After installing Ollama, you need to download a language model. The system is configured to use `llama3.2` by default:

```bash
# Pull the default model (recommended)
ollama pull llama3.2

# Alternative models you can use:
ollama pull mistral
ollama pull llama3.1
ollama pull codellama
```

### 3. Start Ollama Service
Make sure Ollama is running:

```bash
# Start Ollama (it usually starts automatically after installation)
ollama serve
```

### 4. Install Python Dependencies
Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
The AI recommendations are automatically generated when you call the `generate_recommendations()` method on your BudgetSimulator:

```python
from src.budget_simulator import BudgetSimulator, BudgetInput

# Your budget setup
budget_data = BudgetInput(
    monthly_income=5000,
    fixed_expenses={'rent': 1500, 'insurance': 300},
    variable_expenses={'food': 600, 'entertainment': 400},
    savings_goal=800,
    simulation_months=12
)

# Run simulation
simulator = BudgetSimulator(budget_data)
results = simulator.run_simulation()

# Get AI-powered recommendations
recommendations = simulator.generate_recommendations()
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")
```

### Changing the AI Model
You can specify a different Ollama model when creating the simulator:

```python
# Using a different model
simulator.ai_advisor = AIBudgetAdvisor(model_name="mistral")
recommendations = simulator.generate_recommendations()
```

## Features

### What the AI Analyzes
The AI advisor performs comprehensive analysis of:

- **Income Stability**: Consistency of income across months
- **Savings Performance**: How well you meet your savings goals
- **Expense Patterns**: Variable expense volatility and budget adherence
- **Budget Allocation**: Ratios of fixed vs variable expenses
- **Financial Trends**: Whether your financial situation is improving or declining

### Types of Recommendations
The AI provides specific, actionable advice on:

1. **Budget Reallocation**: Specific dollar amounts to shift between categories
2. **Expense Optimization**: Which categories to focus on for cuts or increases  
3. **Savings Strategies**: How to achieve savings goals more consistently
4. **Financial Stability**: Reducing volatility and improving predictability
5. **Goal Adjustment**: Whether targets are realistic based on patterns

### Sample AI Recommendations
```
1. Reduce your food budget from $600 to $520 monthly since you're averaging $545 
   in actual spending with 23% volatility - this $80/month reduction will help 
   you meet your $800 savings goal in 85% of months instead of current 58%.

2. Allocate an additional $50/month to entertainment (increase from $400 to $450) 
   since you're consistently overspending by $45/month in this category, causing 
   budget stress in 9 out of 12 months.

3. Consider negotiating your rent down by $100-150/month as fixed expenses 
   consume 36% of income, leaving limited flexibility for unexpected costs.
```

## Fallback System

If Ollama is not available or fails, the system automatically falls back to rule-based recommendations to ensure the application continues working.

### Troubleshooting

#### "Ollama not available" Error
1. Make sure Ollama is installed and running: `ollama serve`
2. Verify the model is downloaded: `ollama list`
3. Check the model name matches what you're using in code

#### Slow AI Response
- Ollama runs locally and may be slow on less powerful hardware
- Consider using smaller models like `llama3.2:1b` for faster responses
- The system has timeouts and will fall back to rule-based recommendations

#### No Recommendations Generated
- Ensure you've run a simulation first: `simulator.run_simulation()`
- Check that simulation results contain data
- The system will always provide fallback recommendations if AI fails

## Model Recommendations

### For Better Performance:
- **llama3.2:1b** - Fastest, good for quick recommendations
- **llama3.2** - Balanced performance and quality (default)

### For Better Quality:
- **llama3.1:8b** - Higher quality analysis, slower
- **mistral** - Alternative model with good financial reasoning

## Configuration

You can customize the AI behavior by modifying the `AIBudgetAdvisor` class:

```python
# Custom configuration
advisor = AIBudgetAdvisor(model_name="mistral")
advisor.model_name = "llama3.1:8b"  # Change model anytime
```

The AI system uses carefully crafted prompts designed specifically for financial analysis and budget optimization to ensure relevant, actionable advice.