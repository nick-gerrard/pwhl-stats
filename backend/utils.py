PLAYOFF_CUTOFF = 3  # index of last playoff team (0-based), update when expansion arrives


def compute_eliminations(standings: list, remaining_games: dict) -> list:
    cutoff_points = standings[PLAYOFF_CUTOFF]["points"]

    bubble_team = standings[PLAYOFF_CUTOFF + 1]
    bubble_max = bubble_team["points"] + remaining_games.get(bubble_team["team_id"], 0) * 3

    for team in standings:
        games_left = remaining_games.get(team["team_id"], 0)
        team["eliminated"] = team["points"] + games_left * 3 < cutoff_points
        team["clinched"] = team["points"] > bubble_max

    return standings
