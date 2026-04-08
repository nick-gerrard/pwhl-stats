import { PUBLIC_API_URL } from '$env/static/public';
import type { SkaterStats } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const res = await fetch(`${PUBLIC_API_URL}/stats/skaters`);
	const skaters: SkaterStats[] = await res.json();
	return { skaters };
}
