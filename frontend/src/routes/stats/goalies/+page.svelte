<script lang="ts">
	import type { PageData } from './$types';
	import Pagination from '$lib/components/Pagination.svelte';

	let { data }: { data: PageData } = $props();

	const PAGE_SIZE = 20;

	type SortKey = 'last_name' | 'wins' | 'shutouts' | 'save_percentage';

	let teamFilter = $state('');
	let sortKey = $state<SortKey>('save_percentage');
	let sortDir = $state<'asc' | 'desc'>('desc');
	let currentPage = $state(1);

	const teams = $derived([...new Set(data.goalies.map((g) => g.team_name))].sort());

	const filtered = $derived(
		teamFilter ? data.goalies.filter((g) => g.team_name === teamFilter) : data.goalies
	);

	const sorted = $derived(
		[...filtered].sort((a, b) => {
			const aVal = sortKey === 'last_name' ? a.last_name : a[sortKey];
			const bVal = sortKey === 'last_name' ? b.last_name : b[sortKey];
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

	function formatSvPct(pct: number) {
		return pct.toFixed(3).replace(/^0/, '');
	}
</script>

<svelte:head>
	<title>Goalie Stats — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Goalie Stats</h1>
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
					<button onclick={() => setSort('wins')} class="hover:text-white">
						W{sortIndicator('wins')}
					</button>
				</th>
				<th class="px-4 py-3 text-center font-medium">
					<button onclick={() => setSort('shutouts')} class="hover:text-white">
						SO{sortIndicator('shutouts')}
					</button>
				</th>
				<th class="px-4 py-3 text-center font-medium text-white">
					<button onclick={() => setSort('save_percentage')} class="hover:text-white">
						SV%{sortIndicator('save_percentage')}
					</button>
				</th>
			</tr>
		</thead>
		<tbody>
			{#each paginated as goalie, i}
				<tr class="border-b border-zinc-800 last:border-0 transition-colors
					{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}
					hover:bg-zinc-800">
					<td class="px-4 py-3 font-medium text-white"
						>{goalie.first_name} {goalie.last_name}</td>
					<td class="px-4 py-3 text-zinc-400">{goalie.team_name}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{goalie.wins}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{goalie.shutouts}</td>
					<td class="px-4 py-3 text-center font-bold text-white"
						>{formatSvPct(goalie.save_percentage)}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<div class="mt-4">
	<Pagination {currentPage} {totalPages} onPageChange={(n) => (currentPage = n)} />
</div>
