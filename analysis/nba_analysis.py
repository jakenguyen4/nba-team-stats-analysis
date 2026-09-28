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

# Standardize predictors so their coefficients can be compared
scaler = StandardScaler()
X_scaled = scaler.fit_transform(stats[variables])

# Add intercept
X_scaled = sm.add_constant(X_scaled)

# Fit standardized regression
standardized_model = sm.OLS(y, X_scaled).fit()

# Display standardized coefficients
standardized_coefs = pd.Series(
    standardized_model.params[1:],
    index=variables
)

print("\nStandardized Regression Coefficients:")
print(standardized_coefs.sort_values(key=abs, ascending=False))

# Calculate correlations with winning percentage for each season
season_correlations = stats.groupby("Season")[variables + ["Win_Pct"]].corr()["Win_Pct"]

season_correlations = season_correlations.reset_index()

# Remove the correlation of Win_Pct with itself
season_correlations = season_correlations[
    season_correlations["level_1"] != "Win_Pct"
]

season_correlations.columns = ["Season", "Variable", "Correlation"]

# Calculate the average correlation and variation across seasons
season_summary = season_correlations.groupby("Variable")["Correlation"].agg(
    ["mean", "std"]
)

print("\nAverage Season-by-Season Correlations:")
print(season_summary.sort_values("mean", ascending=False))
