export interface Standing {
	team_name: string;
	games_played: number;
	wins: number;
	losses: number;
	ot_wins: number;
	ot_losses: number;
	shootout_wins: number;
	shootout_losses: number;
	points: number;
}

export interface SkaterStats {
	first_name: string;
	last_name: string;
	team_name: string;
	goals: number;
	assists: number;
	shots: number;
}

export interface GoalieStats {
	first_name: string;
	last_name: string;
	team_name: string;
	wins: number;
	shutouts: number;
	save_percentage: number;
}

export interface Game {
	home_team: string;
	visiting_team: string;
	home_score: number | null;
	away_score: number | null;
	date: string;
	status: string;
}
