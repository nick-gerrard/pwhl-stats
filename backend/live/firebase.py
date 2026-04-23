import httpx

LIVE_BASE_URL = "https://leaguestat-b9523.firebaseio.com/svf/pwhl"
LIVE_AUTH = (
    "?auth=uwM69pPkdUhb0UuVAxM8IcA6pBAzATAxOc8979oJ"
    "&key=AIzaSyBVn0Gr6zIFtba-hQy3StkifD8bb7Hi68A"
)
LIVE_URL = f"{LIVE_BASE_URL}.json{LIVE_AUTH}"


def _format_clock(minutes: int, seconds: int) -> str:
    return f"{minutes:02d}:{seconds:02d}"


def _is_active_penalty(penalty: dict) -> bool:
    return (
        penalty["PenaltyShot"] == 0
        and penalty["PowerPlay"] == 1
        and penalty["TimeStartSet"] == 1
    )


def _parse_goals(game_goals: dict) -> tuple[int, int, list]:
    home_score = 0
    visitor_score = 0
    goals = []

    for goal in game_goals.values():
        if goal["IsHome"]:
            home_score += 1
        else:
            visitor_score += 1

        assists = []
        if goal.get("Assist1PlayerLastName"):
            assists.append(
                f"{goal['Assist1PlayerFirstName']} {goal['Assist1PlayerLastName']}"
            )
        if goal.get("Assist2PlayerLastName"):
            assists.append(
                f"{goal['Assist2PlayerFirstName']} {goal['Assist2PlayerLastName']}"
            )

        goals.append(
            {
                "period": goal["PeriodLongName"],
                "time": goal["Time"],
                "scorer": f"{goal['ScorerPlayerFirstName']} {goal['ScorerPlayerLastName']}",
                "assists": assists,
                "is_home": goal["IsHome"],
                "power_play": bool(goal["PowerPlay"]),
                "empty_net": bool(goal["EmptyNet"]),
            }
        )

    return home_score, visitor_score, goals


def _parse_power_play(game_penalties: dict) -> dict:
    active = [p for p in game_penalties.values() if _is_active_penalty(p)]
    home_penalties = sum(1 for p in active if p["Home"] == 1)
    visitor_penalties = sum(1 for p in active if p["Home"] == 0)
    return {
        # home is on PP when visitor has more players in the box
        "home": visitor_penalties > home_penalties,
        # visitor is on PP when home has more players in the box
        "visitor": home_penalties > visitor_penalties,
    }


async def fetch_live_games() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(LIVE_URL)
        response.raise_for_status()
        live_games = response.json()

    published_clock_data = live_games["publishedclock"][1]["games"]
    running_clock_data = live_games["runningclock"]["games"]
    goals_data = live_games["goals"][1]["games"]
    penalty_data = live_games["penalties"][1]["games"]
    shots_data = live_games["shotssummary"][1]["games"]

    games = {}

    for game_id, clock in published_clock_data.items():
        running_clock = running_clock_data.get(game_id, {}).get("Clock", {})
        game_goals = goals_data.get(game_id, {}).get("GameGoals", {})
        game_penalties = penalty_data.get(game_id, {}).get("GamePenalties", {})
        game_shots = shots_data.get(game_id, {})

        home_score, visitor_score, goals = _parse_goals(game_goals)

        clock_minutes = int(running_clock.get("Minutes", clock["ClockMinutes"]))
        clock_seconds = int(running_clock.get("Seconds", clock["ClockSeconds"]))

        games[game_id] = {
            "game_id": game_id,
            "status": clock["ProgressString"],
            "period": clock["PeriodLongName"],
            "clock": _format_clock(clock_minutes, clock_seconds),
            "clock_running": running_clock.get("Running", False),
            "home_score": home_score,
            "visitor_score": visitor_score,
            "power_play": _parse_power_play(game_penalties),
            "goals": goals,
            "home_shots": game_shots.get("HomeShotTotal", 0),
            "visitor_shots": game_shots.get("VisitorShotTotal", 0),
        }

    return games
