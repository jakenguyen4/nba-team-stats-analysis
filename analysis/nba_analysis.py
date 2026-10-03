import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

stats = pd.read_csv("../data/bref_team_stats_clean.csv")

print("Dataset shape:", stats.shape)
print("\nColumns:")
print(stats.columns.tolist())

correlations = stats.corr(numeric_only=True)["Win_Pct"].sort_values(
    ascending=False
)

print("\nCorrelations with Winning Percentage:")
print(correlations)

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

X = stats[variables]
y = stats["Win_Pct"]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print("\nMultiple Regression Results:")
print(model.summary())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(stats[variables])

X_scaled = sm.add_constant(X_scaled)

standardized_model = sm.OLS(y, X_scaled).fit()

standardized_coefs = pd.Series(
    standardized_model.params[1:],
    index=variables
)

print("\nStandardized Regression Coefficients:")
print(standardized_coefs.sort_values(key=abs, ascending=False))

season_correlations = stats.groupby("Season")[variables + ["Win_Pct"]].corr()["Win_Pct"]

season_correlations = season_correlations.reset_index()

season_correlations = season_correlations[
    season_correlations["level_1"] != "Win_Pct"
]

season_correlations.columns = ["Season", "Variable", "Correlation"]

season_summary = season_correlations.groupby("Variable")["Correlation"].agg(
    ["mean", "std"]
)

print("\nAverage Season-by-Season Correlations:")
print(season_summary.sort_values("mean", ascending=False))
