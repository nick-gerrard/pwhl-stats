import { PUBLIC_API_URL } from '$env/static/public';
import type { Game } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const res = await fetch(`${PUBLIC_API_URL}/games/`);
	const games: Game[] = await res.json();
	return { games };
}
