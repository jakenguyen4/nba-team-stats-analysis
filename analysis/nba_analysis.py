import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

# Load NBA team statistics
stats = pd.read_csv("../data/bref_team_stats_clean.csv")

# Display basic information about the dataset
print("Dataset shape:", stats.shape)
print("\nColumns:")
print(stats.columns.tolist())

# Calculate correlations with winning percentage
correlations = stats.corr(numeric_only=True)["Win_Pct"].sort_values(
    ascending=False
)

print("\nCorrelations with Winning Percentage:")
print(correlations)
