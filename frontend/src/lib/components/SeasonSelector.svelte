<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import type { Season } from '$lib/types';

	let { seasons, class: className = '' }: { seasons: Season[]; class?: string } = $props();

	const current = $derived(page.url.searchParams.get('season_id') ?? '');

	function onChange(e: Event) {
		const val = (e.target as HTMLSelectElement).value;
		goto(val ? `?season_id=${val}` : page.url.pathname, { replaceState: true });
	}
</script>

<select
	value={current}
	onchange={onChange}
	class="rounded border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-300
		focus:border-pwhl-light focus:outline-none {className}"
>
	<option value="">Current Season</option>
	{#each seasons as season}
		<option value={String(season.id)}>{season.name}</option>
	{/each}
</select>
