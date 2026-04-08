from datetime import date

from pydantic import BaseModel


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
    games_played: int
    wins: int
    losses: int
    ot_wins: int
    ot_losses: int
    shootout_wins: int
    shootout_losses: int
    points: int


class Game(BaseModel):
    home_team: str
    visiting_team: str
    home_score: int | None
    away_score: int | None
    date: date
    status: str
