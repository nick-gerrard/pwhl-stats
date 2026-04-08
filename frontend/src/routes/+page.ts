import { PUBLIC_API_URL } from '$env/static/public';
import type { Standing } from '$lib/types';

export const ssr = false;

export async function load({ fetch }) {
	const res = await fetch(`${PUBLIC_API_URL}/standings/`);
	const standings: Standing[] = await res.json();
	return { standings };
}
