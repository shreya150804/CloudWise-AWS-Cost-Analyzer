  CloudWise – AWS Cost Analyzer

CloudWise is a **smart cost analysis dashboard** that helps you **track, analyze, and explain AWS billing anomalies**.  
It combines **data preprocessing, anomaly detection, and AI-style reasoning (mocked GPT explanations)** to provide insights into unusual spending patterns.

---

# ✨ Features
- 📊 **Interactive Dashboard** built with Streamlit + Plotly  
- 🔍 **Anomaly Detection** using Z-score on daily AWS costs  
- 🤖 **AI-Style Explanations** (mock GPT reasoning using service & usage type)  
- 📂 **Modular Codebase** (`utils/` for clean and reusable logic)  
- 📑 **Upload Your Own Billing Data** or use the provided sample dataset  

---

# 📂 Project Structure
│── app.py # Streamlit app (main dashboard)
│── README.md # Project documentation
│── utils/
│ ├── data_loader.py # Load and preprocess data
│ ├── analysis.py # Aggregation and breakdowns
│ ├── anomalies.py # Z-score anomaly detection
│ └── ai.py # Mock GPT-style explanations


🛠️ Tech Stack
Python 3.10+
Streamlit – Interactive dashboard
Plotly – Charts & visualizations
Pandas / NumPy – Data wrangling
Z-score – Anomaly detection


👩‍💻 Author
Shreya Wani
📌 LinkedIn
 | GitHub
