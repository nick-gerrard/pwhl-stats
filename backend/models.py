from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class Team:
    id: int
    api_id: int
    name: str
    city: str
    code: str
    nickname: str | None
    logo_url: str | None


@dataclass
class Season:
    id: int
    api_id: int
    name: str
    start_date: date | None
    end_date: date | None
    created_at: datetime


@dataclass
class Player:
    id: int
    api_id: int
    first_name: str
    last_name: str
    height: int | None
    weight: int | None
    birthdate: date | None
    nationality: str | None
    shoots: str | None
    position: str | None
    active: bool
    created_at: datetime


@dataclass
class Roster:
    id: int
    player_id: int
    team_id: int
    season_id: int
    player_number: int | None
    is_rookie: bool
    created_at: datetime


@dataclass
class Game:
    id: int
    api_id: int
    season_id: int
    home_team_id: int
    visiting_team_id: int
    home_score: int | None
    away_score: int | None
    date: date
    status: str
    venue: str | None
    created_at: datetime


@dataclass
class GamePeriod:
    id: int
    game_id: int
    period: int
    home_score: int
    away_score: int


@dataclass
class SkaterStats:
    id: int
    player_id: int
    team_id: int
    season_id: int
    games_played: int
    goals: int
    assists: int
    pim: int
    plus_minus: int
    shots: int
    avg_toi: str | None
    pp_goals: int
    sh_goals: int
    gw_goals: int
    created_at: datetime


@dataclass
class GoalieStats:
    id: int
    player_id: int
    team_id: int
    season_id: int
    games_played: int
    wins: int
    losses: int
    ot_losses: int
    shutouts: int
    shots_against: int
    goals_against: int
    save_percentage: Decimal | None
    gaa: Decimal | None
    minutes_played: int
    created_at: datetime


@dataclass
class Standings:
    id: int
    team_id: int
    season_id: int
    wins: int
    losses: int
    ot_wins: int
    ot_losses: int
    shootout_wins: int
    shootout_losses: int
    games_played: int
    points: int
    created_at: datetime
