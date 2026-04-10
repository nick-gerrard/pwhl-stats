import { PUBLIC_API_URL } from '$env/static/public';
import type { SkaterLeaderboard, GoalieLeaderboard } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const [goals, assists, points, wins, savePct, shutouts] = await Promise.all([
		fetch(`${PUBLIC_API_URL}/stats/skaters/leaderboard?stat=goals`).then((r) => r.json()),
		fetch(`${PUBLIC_API_URL}/stats/skaters/leaderboard?stat=assists`).then((r) => r.json()),
		fetch(`${PUBLIC_API_URL}/stats/skaters/leaderboard?stat=points`).then((r) => r.json()),
		fetch(`${PUBLIC_API_URL}/stats/goalies/leaderboard?stat=wins`).then((r) => r.json()),
		fetch(`${PUBLIC_API_URL}/stats/goalies/leaderboard?stat=save_percentage`).then((r) => r.json()),
		fetch(`${PUBLIC_API_URL}/stats/goalies/leaderboard?stat=shutouts`).then((r) => r.json())
	]);
	return {
		skaterLeaders: { goals, assists, points } as {
			goals: SkaterLeaderboard[];
			assists: SkaterLeaderboard[];
			points: SkaterLeaderboard[];
		},
		goalieLeaders: { wins, savePct, shutouts } as {
			wins: GoalieLeaderboard[];
			savePct: GoalieLeaderboard[];
			shutouts: GoalieLeaderboard[];
		}
	};
}
