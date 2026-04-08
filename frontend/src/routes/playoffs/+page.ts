import { PUBLIC_API_URL } from '$env/static/public';
import type { PlayoffRound } from '$lib/types';

export const ssr = false;

export async function load({ fetch, url }) {
	const seasonId = url.searchParams.get('season_id');
	const query = seasonId ? `?season_id=${seasonId}` : '';
	const res = await fetch(`${PUBLIC_API_URL}/playoffs/bracket${query}`);
	const bracket: PlayoffRound[] = await res.json();
	return { bracket, hasExplicitSeason: !!seasonId };
}
