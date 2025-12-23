
import streamlit as st
import pandas as pd
import json
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Page Config
st.set_page_config(
    page_title="Inventory Optimization Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- 1. Load Data ---
@st.cache_data
def load_data():
    # Load Optimization Results
    with open('data/optimization_results.json', 'r') as f:
        opt_results = json.load(f)
    
    # Load Forecast Data (for visualization)
    if os.path.exists('data/forecast_output.csv'):
        forecast_df = pd.read_csv('data/forecast_output.csv')
        # Ensure dates are datetime
        if 'ds' in forecast_df.columns:
            forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
    else:
        forecast_df = pd.DataFrame()

    return opt_results, forecast_df

try:
    opt_results, forecast_df = load_data()
except FileNotFoundError:
    st.error("Data files not found. Please run the pipeline first.")
    st.stop()

# --- 2. Sidebar: Scenario Controls ---
st.sidebar.header("⚙️ Simulation Parameters")
st.sidebar.markdown("Adjust these to visualize impact on cost & risk.")

# User inputs (defaults from JSON or standard values)
service_level_target = st.sidebar.slider("Target Service Level (%)", 80.0, 99.9, 95.0, 0.1)
holding_cost_pct = st.sidebar.slider("Annual Holding Cost (%)", 10, 40, 20, 1)
stockout_cost = st.sidebar.number_input("Stockout Cost per Unit ($)", value=50, step=5)
lead_time_days = st.sidebar.number_input("Lead Time (Days)", value=15, step=1)

# Extract core metrics from loaded results (as baseline)
# We re-calculate based on slider inputs to show interactivity
avg_weekly_demand = opt_results.get('avg_weekly_demand', 0)
unit_price = opt_results.get('unit_price', 0)
# Re-calculate implied standard deviation from original ROP if needed, 
# but for this demo simplifying: we use the static SS/ROP as baseline and modify roughly via multipliers 
# OR we just implement the simple logic here.

# Let's do a simple dynamic calculation for the "What-If"
# Z-score approximation
from scipy.stats import norm
z_score = norm.ppf(service_level_target / 100.0)

# We need demand std dev to calculate SS properly. 
# Since we don't have it in the simple JSON, we'll estimate it from the original SS.
# Original SS = Z_orig * StdDev_L
# StdDev_L = Original SS / 1.65 (approx for 95%)
original_ss = opt_results.get('safety_stock', 0)
estimated_std_dev_L = original_ss / 1.65 if original_ss > 0 else 5.0

# Calculate New Metrics based on Input
new_safety_stock = z_score * estimated_std_dev_L
new_rop = lead_time_days * (avg_weekly_demand / 7) + new_safety_stock

# --- 3. Main Dashboard ---

st.title("🚀 Executive Inventory Dashboard")
st.markdown("### Predictive Analytics & Optimization Report")

# Top Level Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Unit Price", f"${unit_price:,.2f}")
col2.metric("Avg Weekly Demand", f"{avg_weekly_demand:,.0f} units")
col3.metric("Rec. Safety Stock", f"{new_safety_stock:,.0f} units", delta=f"{new_safety_stock - original_ss:,.0f} vs Baseline")
col4.metric("Reorder Point", f"{new_rop:,.0f} units")

st.divider()

# Two columns for main charts
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("💰 Cost Impact Analysis")
    
    # Cost Logic
    # Scenario A: Reactive (No SS, 5% stockout)
    est_missed_sales_A = (avg_weekly_demand * 52) * 0.05
    cost_stockout_A = est_missed_sales_A * (unit_price + stockout_cost)
    total_cost_A = cost_stockout_A
    
    # Scenario B: Optimized (With User Params)
    cost_holding_B = new_safety_stock * unit_price * (holding_cost_pct / 100.0)
    # Assuming valid service level -> roughly 0 stockouts for simplicity of comparison, 
    # or minimal stockouts. Let's assume 0 for "Optimized"
    total_cost_B = cost_holding_B
    
    savings = total_cost_A - total_cost_B
    
    # Plotly Bar Chart
    cost_data = pd.DataFrame({
        'Scenario': ['Reactive (Current)', 'Optimized (Proposed)'],
        'Annual Cost': [total_cost_A, total_cost_B],
        'Color': ['red', 'green']
    })
    
    fig_cost = px.bar(
        cost_data, x='Scenario', y='Annual Cost', 
        color='Scenario', color_discrete_map={'Reactive (Current)': '#ef4444', 'Optimized (Proposed)': '#22c55e'},
        text_auto='.2s',
        title=f"Potential Annual Savings: ${savings:,.0f}"
    )
    fig_cost.update_layout(showlegend=False)
    st.plotly_chart(fig_cost, width="stretch")
    
    st.info(f"**Insight**: By holding {new_safety_stock:,.0f} units of safety stock, we avoid ${cost_stockout_A:,.0f} in potential stockout losses, costing only ${cost_holding_B:,.0f} in holding fees.")

with right_col:
    st.subheader("📈 90-Day Simulation (Sawtooth)")
    
    # Re-run simulation logic
    days = 90
    sim_stock = new_rop + 50
    inventory_history = []
    days_range = list(range(days))
    pending_orders = []
    order_quantity = 150
    
    for day in days_range:
        # Receive
        if len(pending_orders) > 0 and pending_orders[0] == day:
            sim_stock += order_quantity
            pending_orders.pop(0)
        
        # Demand
        daily_dem = np.random.normal(avg_weekly_demand / 7, 2)
        sim_stock -= max(0, daily_dem)
        
        # Reorder
        if sim_stock <= new_rop and len(pending_orders) == 0:
            arrival = day + int(lead_time_days)
            if arrival < days:
                pending_orders.append(arrival)
        
        inventory_history.append(sim_stock)
        
    # Plotly Line Chart
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=days_range, y=inventory_history, mode='lines', name='Stock Level', line=dict(color='#3b82f6', width=3)))
    fig_sim.add_hline(y=new_safety_stock, line_dash="dash", line_color="red", annotation_text="Safety Stock")
    fig_sim.add_hline(y=new_rop, line_dash="dash", line_color="orange", annotation_text="Reorder Point")
    
    fig_sim.update_layout(
        title="Inventory Levels Over Time",
        xaxis_title="Day",
        yaxis_title="Units",
        hovermode="x unified"
    )
    st.plotly_chart(fig_sim, width="stretch")

st.divider()

# Forecast Section
st.subheader("🔮 Demand Forecast (Prophet Model)")
if not forecast_df.empty:
    # Filter for reasonable timeframe if huge
    fig_forecast = px.line(forecast_df, x='ds', y='yhat', title="Predicted Demand Trends")
    fig_forecast.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper'], mode='lines', line=dict(width=0), showlegend=False)
    fig_forecast.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', name='Confidence Interval')
    st.plotly_chart(fig_forecast, width="stretch")
else:
    st.warning("Forecast data not available.")

