import { PUBLIC_API_URL } from '$env/static/public';
import type { GoalieStats } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const res = await fetch(`${PUBLIC_API_URL}/stats/goalies`);
	const goalies: GoalieStats[] = await res.json();
	return { goalies };
}
