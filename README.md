# 🎯 Automated Portfolio Management System

A smart, adaptive tool for **Trading 212** users that automates portfolio rebalancing and capital allocation, no more manual oversight. Powered by Python and an integrated DeepSeek R1 AI engine, it analyzes performance and news, identifies historical patterns, and adjusts investments in real time.

---

## 🔍 Overview

Between **September 2024 and present**, this system has been evolving to deliver:

- **Dynamic Rebalancing:** Maintains target “pie” allocations by continuously adjusting positions.
- **Smart Capital Allocation:** Responds to real-time market conditions, markets shifting? The system reallocates accordingly.
- **DeepSeek R1 Model:** Analyzes your past trades and parses recent market news to spot similar historical behavior and forecast what's next.
- **Fully Automated:** No manual input required once it’s deployed, just sit back and let it run.

---

## 🧠 Tech & Skills

- **Core Language:** Python  
- **Key Domains:** Machine Learning, NLP, Finance, Algo Trading, Risk Management  
- **APIs:** Trading 212 integration for trades and portfolio data  
- **Tools & Techniques:** Pattern recognition, backtesting, financial modeling, asset allocation

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/devluhar26/PortfolioManagement.git
cd PortfolioManagement

# Set up virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# Update config with your Trading 212 credentials and target allocations
cp config.example.yaml config.yaml
# Edit config.yaml with your API keys, pie targets, DeepSeek settings, etc.

# Run the system
python clock.py
