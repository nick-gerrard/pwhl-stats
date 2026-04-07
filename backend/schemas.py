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
    first_name: str
    last_name: str
    team_name: str
    goals: int
    assists: int
    shots: int


class GoalieStats(BaseModel):
    first_name: str
    last_name: str
    team_name: str
    wins: int
    shutouts: int
    save_percentage: float


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
