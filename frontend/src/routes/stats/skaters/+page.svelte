<script lang="ts">
	import type { PageData } from './$types';
	import Pagination from '$lib/components/Pagination.svelte';

	let { data }: { data: PageData } = $props();

	const PAGE_SIZE = 20;

	type SortKey = 'last_name' | 'goals' | 'assists' | 'points' | 'shots';

	let teamFilter = $state('');
	let sortKey = $state<SortKey>('points');
	let sortDir = $state<'asc' | 'desc'>('desc');
	let currentPage = $state(1);

	const teams = $derived([...new Set(data.skaters.map((s) => s.team_name))].sort());

	const filtered = $derived(
		teamFilter ? data.skaters.filter((s) => s.team_name === teamFilter) : data.skaters
	);

	const sorted = $derived(
		[...filtered].sort((a, b) => {
			const aVal =
				sortKey === 'points'
					? a.goals + a.assists
					: sortKey === 'last_name'
						? a.last_name
						: a[sortKey];
			const bVal =
				sortKey === 'points'
					? b.goals + b.assists
					: sortKey === 'last_name'
						? b.last_name
						: b[sortKey];
			if (typeof aVal === 'string')
				return sortDir === 'asc'
					? aVal.localeCompare(bVal as string)
					: (bVal as string).localeCompare(aVal);
			return sortDir === 'asc'
				? (aVal as number) - (bVal as number)
				: (bVal as number) - (aVal as number);
		})
	);

	const totalPages = $derived(Math.max(1, Math.ceil(sorted.length / PAGE_SIZE)));
	const paginated = $derived(sorted.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE));

	function setSort(key: SortKey) {
		if (sortKey === key) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDir = 'desc';
		}
		currentPage = 1;
	}

	function sortIndicator(key: SortKey) {
		if (sortKey !== key) return '';
		return sortDir === 'desc' ? ' ↓' : ' ↑';
	}
</script>

<svelte:head>
	<title>Skater Stats — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Skater Stats</h1>
	<select
		bind:value={teamFilter}
		onchange={() => (currentPage = 1)}
		class="rounded border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-300
			focus:border-pwhl-light focus:outline-none"
	>
		<option value="">All Teams</option>
		{#each teams as team}
			<option value={team}>{team}</option>
		{/each}
	</select>
</div>

<div class="overflow-x-auto rounded-lg border border-zinc-800">
	<table class="w-full text-sm">
		<thead>
			<tr class="border-b border-zinc-800 bg-pwhl-dark text-left text-zinc-300">
				<th class="px-4 py-3 font-medium">
					<button onclick={() => setSort('last_name')} class="hover:text-white">
						Player{sortIndicator('last_name')}
					</button>
				</th>
				<th class="px-4 py-3 font-medium">Team</th>
				<th class="px-4 py-3 text-center font-medium">
					<button onclick={() => setSort('goals')} class="hover:text-white">
						G{sortIndicator('goals')}
					</button>
				</th>
				<th class="px-4 py-3 text-center font-medium">
					<button onclick={() => setSort('assists')} class="hover:text-white">
						A{sortIndicator('assists')}
					</button>
				</th>
				<th class="px-4 py-3 text-center font-medium text-white">
					<button onclick={() => setSort('points')} class="hover:text-white">
						PTS{sortIndicator('points')}
					</button>
				</th>
				<th class="px-4 py-3 text-center font-medium">
					<button onclick={() => setSort('shots')} class="hover:text-white">
						SOG{sortIndicator('shots')}
					</button>
				</th>
			</tr>
		</thead>
		<tbody>
			{#each paginated as skater, i}
				<tr class="border-b border-zinc-800 last:border-0 transition-colors
					{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}
					hover:bg-zinc-800">
					<td class="px-4 py-3 font-medium text-white"
						>{skater.first_name} {skater.last_name}</td>
					<td class="px-4 py-3 text-zinc-400">{skater.team_name}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{skater.goals}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{skater.assists}</td>
					<td class="px-4 py-3 text-center font-bold text-white"
						>{skater.goals + skater.assists}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{skater.shots}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<div class="mt-4">
	<Pagination {currentPage} {totalPages} onPageChange={(n) => (currentPage = n)} />
</div>
