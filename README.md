<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/d87c8b5a-4e4b-482f-b7c2-dacd98fc23f7" /># Budget Simulator 💰📊

## Overview
Budget Simulator is a sophisticated web-based tool that helps users plan their financial future through intelligent budget simulation and AI-powered recommendations. It combines Monte Carlo simulation techniques with cutting-edge AI analysis to provide personalized financial insights.

## ✨ Features
- **Smart Budget Simulation**: Simulate monthly income, expenses, and savings with realistic variations
- **AI-Powered Recommendations**: Get personalized budget optimization advice using Ollama LLM
- **Interactive Visualizations**: Dynamic charts showing savings trends and expense patterns  
- **Flexible Time Periods**: Run simulations from 6 to 24 months
- **Detailed Analytics**: Download comprehensive CSV reports with monthly breakdowns
- **Expense Volatility Analysis**: Understand spending patterns and budget adherence
- **Savings Goal Tracking**: Monitor progress toward financial objectives

## 🚀 Quick Start

### Prerequisites
Before you begin, ensure you have the following installed on your PC:

- **Python 3.8+** ([Download Python](https://python.org/downloads/))
- **Git** ([Download Git](https://git-scm.com/downloads))
- **Ollama** (Optional, for AI recommendations) ([Download Ollama](https://ollama.ai/))

### Step 1: Clone the Repository
Open your terminal/command prompt and run:

```bash
git clone https://github.com/riya0785/-Budget-Simulator.git
cd -Budget-Simulator
```

### Step 2: Set Up Python Environment (Recommended)
Create a virtual environment to keep dependencies isolated:

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
Navigate to the budget_simulator directory and install required packages:

```bash
cd budget_simulator
pip install -r requirements.txt
```

### Step 4: Set Up AI Features (Optional but Recommended)
For intelligent budget recommendations:

1. **Install Ollama** from https://ollama.ai/
2. **Pull a language model** (choose one):
   ```bash
   # Recommended for balance of speed and quality
   ollama pull llama3.2
   
   # Alternative options
   ollama pull mistral
   ollama pull llama3.1
   ```
3. **Start Ollama service**:
   ```bash
   ollama serve
   ```

### Step 5: Run the Application
Start the Flask web server:

```bash
python src/app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

### Step 6: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
or 
http://127.0.0.1:5000
```


## 📖 How to Use

### 1. Input Your Financial Information
- **Monthly Income**: Enter your regular monthly income
- **Savings Goal**: Set your target monthly savings amount
- **Fixed Expenses**: Add recurring expenses (rent, insurance, etc.)
- **Variable Expenses**: Add flexible expenses (food, entertainment, etc.)

### 2. Run the Simulation
Click "Run Simulation" to generate:
- Monthly expense variations based on realistic patterns
- Seasonal adjustments (holidays, summer, etc.)
- Income fluctuations (20% chance of variation)
- Cumulative savings projections

### 3. Review Results
- **Charts**: Interactive visualizations of your financial projections
- **Summary**: Key metrics like average savings and goal achievement rate
- **AI Recommendations**: Personalized advice for budget optimization
- **CSV Export**: Detailed monthly data for further analysis

### 4. Implement Recommendations
Use the AI-generated suggestions to:
- Adjust budget allocations
- Identify overspending categories
- Optimize savings strategies
- Improve financial stability

## 🛠️ Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'ollama'"
**Solution**: Install the missing package
```bash
pip install ollama
```

#### "Ollama not available" message
**Solutions**:
1. Ensure Ollama is installed and running: `ollama serve`
2. Verify a model is installed: `ollama list`
3. Pull a model if needed: `ollama pull llama3.2`

#### Flask app won't start
**Solutions**:
1. Check if virtual environment is activated
2. Ensure you're in the correct directory (`budget_simulator/src/`)
3. Verify all dependencies are installed: `pip install -r requirements.txt`

#### Port 5000 already in use
**Solution**: Use a different port
```bash
python src/app.py --port 5001
```

### Performance Tips
- For faster AI responses, use smaller models: `ollama pull llama3.2:1b`
- Close other applications to free up system resources
- Use SSD storage for better performance

## 📁 Project Structure
```
-Budget-Simulator/
├── budget_simulator/
│   ├── src/
│   │   ├── app.py                    # Flask web application
│   │   ├── budget_simulator.py       # Core simulation logic
│   │   └── ai_budget_advisor.py      # AI recommendation engine
│   ├── templates/
│   │   ├── base.html                 # HTML template base
│   │   └── index.html                # Main application interface
│   ├── static/css/
│   │   └── styles.css                # Application styling
│   ├── requirements.txt              # Python dependencies
│   └── AI_SETUP.md                   # Detailed AI setup guide
├── README.md                         # This file
└── .gitignore                        # Git ignore rules
```

## 🧪 Testing
Test the AI recommendation system:
```bash
cd budget_simulator/src
python test_ai_recommendations.py
```
Sure! Here's a simpler, easy-to-understand version for your README:

---

## ⚠️ Things to Know

1. **LLM Recommendations Take Time**

   * When you click to get recommendations, it may take **about 1 minute**.
   * Please wait and don’t refresh or close the page while it’s running.

2. **Flask Port Issues on Windows**

   * Sometimes Windows blocks certain ports and you may see this error:

     ```
     An attempt was made to access a socket in a way forbidden by its access permissions
     ```
   * To fix it:

     * Use a port **above 55000** in `app.py`:

       ```python
       app.run(debug=True, host='127.0.0.1', port=55000)
       ```
     * Make sure **Python is allowed** through Windows Firewall.
     * Run your terminal as **Administrator** if needed.

3. **Extra Tips**

   * Make sure no other app is using the same port.
   * If Flask or LLM doesn’t start, close any running Python processes with:

     ```powershell
     taskkill /IM python.exe /F
     ```

---



## 🤝 Contributing
Contributions are welcome! Please feel free to:
- Report bugs by opening an issue
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 Example Usage
Here's a sample budget to try:

- **Monthly Income**: Rs.5,000
- **Savings Goal**: Rs.800
- **Fixed Expenses**: 
  - Rent: Rs.1,500
  - Insurance: Rs.300
  - Car Payment: Rs450
- **Variable Expenses**:
  - Food: Rs.600
  - Entertainment: Rs.400
  - Gas: Rs.200

## 🚨 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+
- **RAM**: 4GB (8GB recommended for AI features)
- **Storage**: 2GB free space
- **Internet**: Required for initial setup and Ollama model downloads

### Recommended Specifications
- **RAM**: 8GB+ (for optimal AI performance)
- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **Storage**: SSD for faster model loading

## 🔧 Advanced Configuration

### Using Different AI Models
You can switch between different Ollama models for varied performance:

```python
# In your code, modify the AIBudgetAdvisor initialization
from src.ai_budget_advisor import AIBudgetAdvisor

# Use different models
advisor = AIBudgetAdvisor(model_name="mistral")        # Alternative model
advisor = AIBudgetAdvisor(model_name="llama3.2:1b")   # Faster, smaller model
advisor = AIBudgetAdvisor(model_name="llama3.1:8b")   # Higher quality, slower
```

### Environment Variables
You can customize the application behavior:

```bash
# Set custom port
export FLASK_PORT=8080

# Enable debug mode
export FLASK_DEBUG=1

# Set Ollama host (if running remotely)
export OLLAMA_HOST=http://localhost:11434
```

### Running in Production
For production deployment:

```bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

## 🆘 Support

### Getting Help
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check `AI_SETUP.md` for detailed AI configuration
- **Community**: Join discussions in the repository

### FAQ

**Q: Can I run this without the AI features?**
A: Yes! The application works perfectly without Ollama. You'll get rule-based recommendations instead.

**Q: How much data does Ollama use?**
A: Model sizes range from 1GB (llama3.2:1b) to 7GB (llama3.1:8b). Download once, use offline.

**Q: Is my financial data secure?**
A: Yes! All processing happens locally on your machine. No data is sent to external servers.

**Q: Can I customize the simulation parameters?**
A: Yes! Modify the values in `budget_simulator.py` for different economic scenarios.

## 📊 Sample Output
After running a simulation, you'll see:
- **Monthly savings trend chart**
- **Expense category breakdown**
- **Goal achievement percentage**
- **AI recommendations like**:
  - *"Increase grocery budget by $50/month to reduce overspending stress"*
  - *"Consider reducing entertainment expenses by 15% to meet savings goals"*
  - *"Your housing costs are optimal at 32% of income"*


## 📄 License
This project is licensed under the MIT License - see the repository for details.

## 👥 Authors & Contact
- **Developers**: Riya Shukla, Chris Vinod Kurian, Aparna Iyer
- **Email**: riya.shukla.btech2022@sitpune.edu.in, chris.kurian.btech2022@sitpune.edu.in,
aparna.iyer.btech2022@sitpune.edu.in
- **Repository**: https://github.com/riya0785/-Budget-Simulator


---

**Made with ❤️ for better financial planning**

*Happy Budgeting! 🎯💰*
