import { PUBLIC_API_URL } from '$env/static/public';
import type { BasePlayers } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/all`);
	const players: BasePlayers[] = res.ok ? await res.json() : [];
	return { players };
}
