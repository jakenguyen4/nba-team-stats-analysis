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

# Variables used in the regression model
variables = [
    "Off_eFG_Pct",
    "Off_TOV_Pct",
    "ORB_Pct",
    "FTr",
    "Def_eFG_Pct",
    "Def_TOV_Pct",
    "DRB_Pct",
    "3PAr",
    "Pace"
]

# Set predictors and response variable
X = stats[variables]
y = stats["Win_Pct"]

# Add intercept
X = sm.add_constant(X)

# Fit multiple linear regression
model = sm.OLS(y, X).fit()

# Display regression results
print("\nMultiple Regression Results:")
print(model.summary())
