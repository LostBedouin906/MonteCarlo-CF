import streamlit as st 
import pandas as pd 
from simulation import run_simulation # import your simulation function

st.title("Cleveland Group IRR Simulator")
st.write("This app runs a Monte Carlo simulation for real estate cashflow and IRR analysis.")

# Sliders for inputs
num_simulations = st.slider("Number of Simulations", 100, 3000,1000, step=100)
rent_growth = st.slider("Annual Rent Growth (%)", 0.0, 5.0, 2.5, step=0.1) / 100
expense_growth = st.slider("Annual Expense Growth (%)", 0.0, 5.0, 1.2, step=0.1) / 100
st.write("### CapEx % Range (as % of property value)")
capex_min = st.slider("Min CapEx %", 0.0, 0.5, 0.1, step=0.01)
capex_max = st.slider("Max CapEx %", 0.0, 0.5, 0.25, step=0.01)
st.write("### Appreciation Rate Range (Annual %)")
appreciation_min = st.slider("Min Appreciation %", 0.0, 0.1, 0.02, step=0.005)
appreciation_max = st.slider("Max Appreciation %", 0.0, 0.1, 0.035, step=0.005)
st.write("### Expense Ratio Range (Annual % of Rent)")
expense_min = st.slider("Min Expense Ratio %", 0.15, 0.45, 0.25, step=0.01)
expense_max = st.slider("Max Expense Ratio %", 0.15, 0.45, 0.4, step=0.01)

if st.button("Run Simulation"):
    st.write(f"Running {num_simulations} simulations...")

#call your simulation 
    df = run_simulation(num_simulations, rent_growth, expense_growth, capex_min, capex_max, appreciation_min, appreciation_max, expense_min, expense_max)
# Tier Filter via Radio Button
    tiers = df["Tier"].unique().tolist()
    tiers.insert(0, "All")  # Add "All" option at the top

    selected_tier = st.radio("Select Property Tier", tiers)

    if selected_tier != "All": 
        filtered_df = df[df["Tier"] == selected_tier]
    else:
        filtered_df = df

# Summary Stats
    avg_irr = filtered_df["IRR"].mean()
    median_irr = filtered_df["IRR"].median()
    avg_roi = filtered_df["ROI %"].mean()
    avg_noi = filtered_df["Net Operating Income"].mean()

    st.write("### 📊 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg IRR", f"{avg_irr:.2%}")
    col2.metric("Median IRR", f"{median_irr:.2%}")
    col3.metric("Avg ROI", f"{avg_roi:.2f}%")
    col4.metric("Avg 5-Yr NOI", f"${avg_noi:,.0f}")

    st.write("### Sample Results")
    st.dataframe(filtered_df.head())
    st.download_button(
    label="📥 Download Filtered Results (CSV)",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="simulation_results.csv",
    mime="text/csv"
    )

    st.write("### IRR Distribution")
    st.bar_chart(filtered_df["IRR"])