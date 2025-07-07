import numpy as np
import pandas as pd
import numpy_financial as npf

# Constants
NUM_SIMULATIONS = 1000
YEARS = 5
RENT_GROWTH = 0.025  # 2.5% annual rent growth
APPRECIATION_MIN = 0.02  # 1% property appreciation
APPRECIATION_MAX = 0.1  # 4% property appreciation
EXPENSE_MIN = 0.15  # 32% expense ratio
EXPENSE_MAX = 0.45  # 45% expense ratio
EXIT_COST = 0.09  # 9% selling cost

# Tier lookup table (like Excel)
tiers = [
    {"name": "Distressed", "max_value": 100000, "rent_yield": 0.0155, "min_capex": 0.25, "max_capex": 0.40},
    {"name": "Value-Add", "max_value": 180000, "rent_yield": 0.013, "min_capex": 0.16, "max_capex": 0.25},
    {"name": "Mid-Tier", "max_value": 300000, "rent_yield": 0.011, "min_capex": 0.08, "max_capex": 0.15},
    {"name": "Retail-Ready", "max_value": 400000, "rent_yield": 0.009, "min_capex": 0.03, "max_capex": 0.07},
]

# Function to determine tier based on property value
def get_tier(value):
    for tier in tiers:
        if value <= tier["max_value"]:
            return tier
    return tiers[-1]

# Main simulation function
def run_simulation(num_simulations, rent_growth, expense_growth, capex_min, capex_max, appreciation_min, appreciation_max, expense_min, expense_max):
    results = []
   
    for i in range(1, num_simulations + 1):
    # Property value and tier
        property_value = np.random.lognormal(mean=11.9, sigma=0.55)
        property_value = np.clip(property_value, 30000, 400000)
        tier = get_tier(property_value)

        # CapEx from input range
        capex_pct = np.random.uniform(tier["min_capex"], tier["max_capex"])
        capex = property_value * capex_pct
        total_investment = property_value + capex

        # Monthly rent and base metrics
        rent_yield = tier["rent_yield"]
        monthly_rent = property_value * rent_yield
        annual_rent = monthly_rent * 12

        # Random parameters per sim
        expense_ratio_base = np.random.uniform(expense_min, expense_max)
        appreciation_rate = np.random.uniform(appreciation_min, appreciation_max)

        # Cashflow setup
        cashflows = [-total_investment]
        total_noi = 0

        # Yearly cashflows
        for year in range(1, YEARS + 1):
            monthly_rent_year = monthly_rent * ((1 + rent_growth) ** (year - 1))

            if year == 1:
                collected_months = 10
            else:
                collected_months = 12 - np.random.randint(0, 2)
            effective_rent = monthly_rent_year * collected_months
            
            # Separate Fixed and Variable Expenses
            fixed_expense_annual = 2000  # Example: property tax, insurance, etc.
            fixed_expense_growth = 0.02  # Optional annual inflation
            fixed_expense = fixed_expense_annual * ((1 + fixed_expense_growth) ** (year - 1))

            variable_expense_ratio = expense_ratio_base
            variable_expense = effective_rent * variable_expense_ratio * ((1 + expense_growth) ** (year - 1))
            expenses = fixed_expense + variable_expense

            noi = effective_rent - expenses
            cashflows.append(noi)
            total_noi += noi

        # Sale value
        renno_multiplier = np.random.uniform(0.5, 1.25)
        renno_capex = property_value + (renno_multiplier * capex)
        exit_value = renno_capex * ((1 + appreciation_rate) ** YEARS)
        net_sale_proceeds = exit_value * (1 - EXIT_COST)
        cashflows[-1] += net_sale_proceeds

        # Final metrics
        total_profit = total_noi + net_sale_proceeds - total_investment
        roi = total_profit / total_investment
        irr = npf.irr(cashflows)
       
        # Compute Cap Rate based on Year 1 NOI
        year_1_monthly_rent = monthly_rent  # already adjusted at year 1
        collected_months_year_1 = 10  # fixed assumption for year 1
        effective_rent_year_1 = year_1_monthly_rent * collected_months_year_1
        fixed_expense_year_1 = fixed_expense_annual
        variable_expense_year_1 = effective_rent_year_1 * variable_expense_ratio
        total_expense_year_1 = fixed_expense_year_1 + variable_expense_year_1
        noi_year_1 = effective_rent_year_1 - total_expense_year_1
        cap_rate = noi_year_1 / property_value if property_value > 0 else 0

        results.append({
                "Simulation #": i,
                "Property Value": round(property_value, 2),
                "Renovation CapEx": round(capex, 2),
                "Total Investment": round(total_investment, 2),
                "Tier": tier["name"],
                "Monthly Rent": round(monthly_rent, 2),
                "Annual Gross Rent": round(annual_rent, 2),
                "Expenses": round(expenses, 2),
                "Expense Ratio": round(expense_ratio_base, 3),
                "Net Operating Income": round(total_noi, 2),
                "Exit Property Value": round(exit_value, 2),
                "Net Sale Proceeds": round(net_sale_proceeds, 2),
                "ROI %": round(roi * 100, 2),
                "IRR": irr,
                "Cap Rate": round(cap_rate, 4)

                })
    return pd.DataFrame(results)



