import pandas as pd

# Loads NBA game data
df = pd.read_csv("../data/Games.csv")

# Keeps regular season games only
regular = df[df["gameType"] == "Regular Season"].copy()

# Convert game date to datetime
regular["gameDate"] = pd.to_datetime(regular["gameDate"])

# Create the season year
regular["Season"] = regular["gameDate"].dt.year

# Create home team results
home = regular[["Season", "hometeamName", "homeScore", "awayScore"]].copy()

home = home.rename(columns={
    "hometeamName": "Team",
    "homeScore": "PointsFor",
    "awayScore": "PointsAgainst"
})

home["Win"] = (home["PointsFor"] > home["PointsAgainst"]).astype(int)

# Create away team results
away = regular[["Season", "awayteamName", "awayScore", "homeScore"]].copy()

away = away.rename(columns={
    "awayteamName": "Team",
    "awayScore": "PointsFor",
    "homeScore": "PointsAgainst"
})

away["Win"] = (away["PointsFor"] > away["PointsAgainst"]).astype(int)

# Combine home and away games
team_games = pd.concat([home, away])

# Calculate team-season statistics
team_season = team_games.groupby(["Team", "Season"]).agg(
    Wins=("Win", "sum"),
    Games=("Win", "count"),
    PointsFor=("PointsFor", "sum"),
    PointsAgainst=("PointsAgainst", "sum")
).reset_index()

# Calculate winning percentage
team_season["Win_Pct"] = team_season["Wins"] / team_season["Games"]

# Calculate points per game
team_season["PPG"] = team_season["PointsFor"] / team_season["Games"]

# Calculate opponent points per game
team_season["Opp_PPG"] = team_season["PointsAgainst"] / team_season["Games"]

# Calculate point differential per game
team_season["Point_Diff"] = team_season["PPG"] - team_season["Opp_PPG"]

print(team_season.head(20))
