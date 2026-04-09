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

export interface Season {
	id: number;
	name: string;
	season_type: string;
}

export interface PlayoffTeam {
	name: string;
	code: string;
}

export interface PlayoffSeries {
	series_letter: string;
	series_name: string;
	team1: PlayoffTeam;
	team2: PlayoffTeam;
	team1_wins: number;
	team2_wins: number;
	is_active: boolean;
}

export interface PlayoffRound {
	round_number: number;
	round_name: string;
	series: PlayoffSeries[];
}

export interface Game {
	api_id: number;
	home_team: string;
	home_team_logo: string | null;
	visiting_team: string;
	visiting_team_logo: string | null;
	home_score: number | null;
	away_score: number | null;
	date: string;
	status: string;
	start_time: string | null;
}

export interface LiveGoal {
	period: string;
	time: string;
	scorer: string;
	assists: string[];
	is_home: boolean;
	power_play: boolean;
	empty_net: boolean;
}

export interface LiveGame {
	game_id: string;
	status: string;
	period: string;
	clock: string;
	home_score: number;
	visitor_score: number;
	power_play: { home: boolean; visitor: boolean };
	goals: LiveGoal[];
	home_shots: number;
	visitor_shots: number;
}
