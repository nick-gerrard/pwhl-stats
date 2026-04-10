import { PUBLIC_API_URL } from '$env/static/public';
import type { GoalieCareerInfo } from '$lib/types';

export const ssr = false;

export async function load({ fetch, params }) {
	const res = await fetch(`${PUBLIC_API_URL}/stats/goalies/${params.player_id}/career`);
	if (!res.ok) return { career: [] as GoalieCareerInfo[] };
	const career: GoalieCareerInfo[] = await res.json();
	return { career };
}
