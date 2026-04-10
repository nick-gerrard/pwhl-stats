import { PUBLIC_API_URL } from '$env/static/public';
import type { SkaterCareerInfo } from '$lib/types';

export const ssr = false;

export async function load({ fetch, params }) {
	const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/${params.player_id}/career`);
	if (!res.ok) return { career: [] as SkaterCareerInfo[] };
	const career: SkaterCareerInfo[] = await res.json();
	return { career };
}
