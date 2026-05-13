import { PUBLIC_API_URL } from '$env/static/public';
import type { BasePlayers } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const [skatersRes, goaliesRes] = await Promise.all([
		fetch(`${PUBLIC_API_URL}/stats/skaters/all`),
		fetch(`${PUBLIC_API_URL}/stats/goalies/all`)
	]);
	const skaters: BasePlayers[] = skatersRes.ok ? await skatersRes.json() : [];
	const goalies: BasePlayers[] = goaliesRes.ok ? await goaliesRes.json() : [];
	return { skaters, goalies };
}
