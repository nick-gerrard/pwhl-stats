import { PUBLIC_API_URL } from '$env/static/public';
import type { Season } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const res = await fetch(`${PUBLIC_API_URL}/seasons/`);
	const seasons: Season[] = await res.json();
	return {
		regularSeasons: seasons.filter((s) => s.season_type === 'regular'),
		playoffSeasons: seasons.filter((s) => s.season_type === 'playoff'),
		allSeasons: seasons
	};
}
