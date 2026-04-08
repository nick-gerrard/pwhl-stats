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
	player_id: number;
	first_name: string;
	last_name: string;
	team_name: string;
	goals: number;
	assists: number;
	shots: number;
}

export interface PlayerInfo {
	first_name: string;
	last_name: string;
	team_name: string;
	games_played: number;
	goals: number;
	assists: number;
	pim: number;
	plus_minus: number;
	shots: number;
	avg_toi: string;
	pp_goals: number;
	sh_goals: number;
	gw_goals: number;
	height: number | null;
	weight: number | null;
	birthdate: string | null;
	nationality: string | null;
	shoots: string | null;
	position: string | null;
	active: boolean;
}

export interface GoalieStats {
	player_id: number;
	first_name: string;
	last_name: string;
	team_name: string;
	wins: number;
	shutouts: number;
	save_percentage: number;
}

export interface GoalieInfo {
	first_name: string;
	last_name: string;
	team_name: string;
	games_played: number;
	wins: number;
	losses: number;
	ot_losses: number;
	shutouts: number;
	shots_against: number;
	goals_against: number;
	save_percentage: number | null;
	gaa: number | null;
	minutes_played: number;
	height: number | null;
	weight: number | null;
	birthdate: string | null;
	nationality: string | null;
	shoots: string | null;
	position: string | null;
	active: boolean;
}

export interface Game {
	home_team: string;
	visiting_team: string;
	home_score: number | null;
	away_score: number | null;
	date: string;
	status: string;
}
