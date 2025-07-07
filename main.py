from simulation import run_simulation

# Run the simulation
df = run_simulation()

# Print the first 10 rows of results
print(df.head(10))

# Save results to a single CSV file (overwrites each time)
df.to_csv("simulation_results.csv", index=False)

print("\n✅ Simulation results saved to 'simulation_results.csv'!")
