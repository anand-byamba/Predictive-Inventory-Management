# 📦 Predictive Supply Chain Optimization

This repository hosts an end-to-end data science pipeline designed to solve one of the most expensive problems in logistics: **Inventory Volatility**.

Using the **Olist E-commerce dataset**, this project moves beyond traditional "static averages" to implement a **probabilistic inventory model** driven by Machine Learning (Facebook Prophet) and statistical risk management.

**Now features an fully automated pipeline and an interactive executive dashboard.**

---

## 🚀 Quick Start

### 1. Run the Pipeline
Execute the full data engineering, analysis, and optimization pipeline with one command:
```bash
python run_pipeline.py
```
This script will:
1.  Process raw data.
2.  Train forecasting models.
3.  Optimize inventory parameters.
4.  Generate static figure assets in `results/figures/`.

### 2. Launch the Dashboard
View the results in an interactive web application:
```bash
streamlit run dashboard.py
```
This allows you to verify the impact of different service levels and costs on your bottom line in real-time.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `run_pipeline.py` | **Automation Orchestrator:** Runs all notebooks sequentially to generate results. |
| `dashboard.py` | **Interactive App:** Streamlit dashboard for stakeholders to explore scenarios. |
| `notebooks/01_Data_Engineering.ipynb` | **ETL Pipeline:** Merges 9 raw relational tables into a clean Master Source of Truth. |
| `notebooks/02_ABC_Analysis.ipynb` | **Strategic Segmentation:** Uses Pareto Principle (80/20) to identify high-value SKUs. |
| `notebooks/03_Forecasting.ipynb` | **Demand Forecasting:** Trains a **Prophet** model to predict weekly sales trends. |
| `notebooks/04_Inventory_Optimization.ipynb` | **Risk Modeling:** Transforms forecasts into actionable Reorder Points (ROP). |
| `notebooks/05_Executive_Report.ipynb` | **Simulation & ROI:** 90-day "Sawtooth" simulation to stress-test the policy. |
| `results/figures/` | **Generated Assets:** Automatically generated plots (Cost Comparison, Sawtooth Chart, etc.). |

---

## 🧠 Methodology: The "Stochastic" Approach

Instead of guessing, we use the **Root Sum of Squared Error** formula to account for independent variabilities in Supply and Demand.

$$
Safety Stock = Z \times \sqrt{(\bar{L} \times \sigma_D^2) + (\bar{D}^2 \times \sigma_L^2)}
$$

* **$Z$ (Service Factor):** We use **1.65** to target a **95% Service Level** (statistically guaranteeing stock availability 95% of the time).
* **$\sigma_L$ (Supply Risk):** Measures how unreliable the supplier is (Standard Deviation of Lead Time).
* **$\sigma_D$ (Demand Risk):** Measures how volatile customer purchasing is (Standard Deviation of Daily Sales).

**Key Insight:** By decoupling these risks, we can hold *less* inventory for stable products and *more* for volatile ones, optimizing total working capital.

---

## 📊 Results & Impact

The 90-day simulation stress-tested this policy against a reactive baseline:

*   **Service Level Stability:** Maintained >95% availability even during simulated demand spikes.
*   **Capital Efficiency:** Reduced holding costs for Class C (low value) items by strictly limiting their safety stock.
*   **Operational Automation:** Generated automated "Reorder Point" triggers, removing manual guesswork.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
*   Python 3.11+
*   Anaconda or Miniconda

### 2. Environment Setup
It is recommended to use a separate Conda environment to ensure library compatibility.

```bash
# Create the environment
conda create -n supply_chain_311 python=3.11

# Activate it
conda activate supply_chain_311

# Install dependencies
pip install -r requirements.txt
```

---

## ⚖️ License

**Code:** The software logic in this repository is licensed under the **MIT License**.

**Data:** The dataset is provided by Olist under **CC BY-NC-SA 4.0**.
