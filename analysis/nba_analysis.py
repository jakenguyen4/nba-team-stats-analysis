import pandas as pd

# Loads NBA game data
df = pd.read_csv("../data/Games.csv")

# Show the first 5 games
print(df.head())

# Show all column names
print(df.columns)

# Show number of rows and columns
print(df.shape)

