# 📦 Predictive Supply Chain Optimization

This repository hosts an end-to-end data science pipeline designed to solve one of the most expensive problems in logistics: **Inventory Volatility**.

Using the **Olist E-commerce dataset**, this project moves beyond traditional "static averages" to implement a **probabilistic inventory model** driven by Machine Learning (Facebook Prophet) and statistical risk management.

---

## 🚀 Why This Matters (The Business Case)

In high-volume e-commerce, inventory management is a balancing act between two financial risks:
1.  **Stockouts (Lost Revenue):** If a "Hero Product" runs out, the company loses immediate sales and long-term customer loyalty.
2.  **Overstock (Frozen Capital):** Excess inventory ties up cash flow in warehousing costs and depreciation, preventing investment in growth.

**The Problem:** Most legacy systems rely on simple averages (e.g., "We sell 10 units a day, so buy 10").
**The Failure Mode:** Averages hide volatility. If a supplier is 3 days late or a marketing campaign spikes demand by 20%, the "average" model fails, leading to stockouts.

**The Solution:** This project builds a **resilient system** that calculates Safety Stock based on *variance* ($\sigma$), not just averages, ensuring a 95% Service Level even during supply chain disruptions.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `notebooks/01_Data_Engineering.ipynb` | **ETL Pipeline:** Merges 9 raw relational tables into a clean Master Source of Truth. Handles date parsing and null-value logic. |
| `notebooks/02_ABC_Analysis.ipynb` | **Strategic Segmentation:** Uses the **Pareto Principle (80/20)** to identify high-value SKUs. Focuses resources on the products that drive revenue. |
| `notebooks/03_Forecasting.ipynb` | **Demand Forecasting:** Trains a **Prophet** additive regression model to predict weekly sales trends, seasonality, and holiday spikes. |
| `notebooks/04_Inventory_Optimization.ipynb` | **Risk Modeling:** transform forecasts into actionable Reorder Points (ROP) using lead-time variance analysis. |
| `notebooks/05_Executive_Report.ipynb` | **Simulation & ROI:** Runs a 90-day "Sawtooth" simulation to stress-test the policy and visualize potential cost savings. |

## 💾 Data Source
* **Dataset:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (via Kaggle).
* **Context:** Real anonymized order data from 100k+ orders in Brazil.

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

* **Service Level Stability:** Maintained >95% availability even during simulated demand spikes.
* **Capital Efficiency:** Reduced holding costs for Class C (low value) items by strictly limiting their safety stock.
* **Operational Automation:** Generated automated "Reorder Point" triggers, removing manual guesswork from the purchasing process.

---

## ⚖️ License

**Code:** The software logic in this repository is licensed under the **MIT License**. You are free to use, modify, and distribute the code.

**Data:** The dataset is provided by Olist under **CC BY-NC-SA 4.0**.
* **Attribution:** Data provided by Olist.
* **Non-Commercial:** The data cannot be used for commercial purposes.
* **ShareAlike:** If you modify the dataset, you must share it under the same license.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python 3.11+
* Anaconda or Miniconda

### 2. Environment Setup
It is recommended to use a separate Conda environment to ensure library compatibility (Prophet requires specific versions).

```bash
# Create the environment
conda create -n supply_chain_311 python=3.11

# Activate it
conda activate supply_chain_311

# Install dependencies
pip install -r requirements.txt
