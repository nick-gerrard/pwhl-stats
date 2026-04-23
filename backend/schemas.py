from datetime import date, datetime

from pydantic import BaseModel


class Season(BaseModel):
    id: int
    name: str
    season_type: str


class Team(BaseModel):
    id: int
    api_id: int
    name: str
    city: str
    code: str
    nickname: str
    logo_url: str | None


class Player(BaseModel):
    id: int
    api_id: int
    first_name: str
    last_name: str
    shoots: str | None
    position: str | None


class SkaterStats(BaseModel):
    player_id: int
    first_name: str
    last_name: str
    team_name: str
    goals: int
    assists: int
    shots: int


class PlayerInfo(BaseModel):
    first_name: str
    last_name: str
    team_name: str
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
    height: int | None
    weight: int | None
    birthdate: date | None
    nationality: str | None
    shoots: str | None
    position: str | None
    active: bool


class GoalieStats(BaseModel):
    player_id: int
    first_name: str
    last_name: str
    team_name: str
    wins: int
    shutouts: int
    save_percentage: float

class GoalieInfo(BaseModel):
    first_name: str
    last_name: str
    team_name: str
    games_played: int
    wins: int
    losses: int
    ot_losses: int
    shutouts: int
    shots_against: int
    goals_against: int
    save_percentage: float | None
    gaa: float | None
    minutes_played: int
    height: int | None
    weight: int | None
    birthdate: date | None
    nationality: str | None
    shoots: str | None
    position: str | None
    active: bool



class Standing(BaseModel):
    team_name: str
    logo_url: str
    games_played: int
    wins: int
    regulation_wins: int
    losses: int
    ot_wins: int
    ot_losses: int
    shootout_wins: int
    shootout_losses: int
    points: int


class Game(BaseModel):
    api_id: int
    home_team: str
    home_team_logo: str | None
    visiting_team: str
    visiting_team_logo: str | None
    home_score: int | None
    away_score: int | None
    date: date
    status: str
    start_time: datetime | None


class PlayoffTeam(BaseModel):
    name: str
    code: str


class PlayoffSeries(BaseModel):
    series_letter: str
    series_name: str
    team1: PlayoffTeam
    team2: PlayoffTeam
    team1_wins: int
    team2_wins: int
    is_active: bool


class PlayoffRound(BaseModel):
    round_number: int
    round_name: str
    series: list[PlayoffSeries]
