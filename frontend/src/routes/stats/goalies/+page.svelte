<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import type { PageData } from './$types';
	import type { GoalieInfo } from '$lib/types';
	import Pagination from '$lib/components/Pagination.svelte';

	let { data }: { data: PageData } = $props();

	const PAGE_SIZE = 20;

	type SortKey = 'last_name' | 'wins' | 'shutouts' | 'save_percentage';

	let teamFilter = $state('');
	let sortKey = $state<SortKey>('save_percentage');
	let sortDir = $state<'asc' | 'desc'>('desc');
	let currentPage = $state(1);

	let selectedGoalie = $state<GoalieInfo | null>(null);
	let modalOpen = $state(false);
	let loading = $state(false);

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

	function formatSvPct(pct: number | null) {
		if (pct === null) return '—';
		return pct.toFixed(3).replace(/^0/, '');
	}

	function formatGaa(gaa: number | null) {
		if (gaa === null) return '—';
		return gaa.toFixed(2);
	}

	function formatDate(dateStr: string | null) {
		if (!dateStr) return '—';
		return new Date(dateStr).toLocaleDateString('en-CA', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	async function openGoalie(player_id: number) {
		modalOpen = true;
		loading = true;
		selectedGoalie = null;
		const res = await fetch(`${PUBLIC_API_URL}/stats/goalies/${player_id}`);
		selectedGoalie = await res.json();
		loading = false;
	}

	function closeModal() {
		modalOpen = false;
		selectedGoalie = null;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') closeModal();
	}
</script>

<svelte:head>
	<title>Goalie Stats — PWHL Stats</title>
</svelte:head>

<svelte:window onkeydown={handleKeydown} />

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
				<tr
					onclick={() => openGoalie(goalie.player_id)}
					class="cursor-pointer border-b border-zinc-800 last:border-0 transition-colors
						{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}
						hover:bg-zinc-800"
				>
					<td class="px-4 py-3 font-medium text-white"
						>{goalie.first_name} {goalie.last_name}</td
					>
					<td class="px-4 py-3 text-zinc-400">{goalie.team_name}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{goalie.wins}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{goalie.shutouts}</td>
					<td class="px-4 py-3 text-center font-bold text-white"
						>{formatSvPct(goalie.save_percentage)}</td
					>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<div class="mt-4">
	<Pagination {currentPage} {totalPages} onPageChange={(n) => (currentPage = n)} />
</div>

<!-- Modal -->
{#if modalOpen}
	<div
		class="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
		onclick={closeModal}
		role="presentation"
	></div>

	<div
		class="fixed inset-x-0 bottom-0 z-50 mx-auto max-w-2xl rounded-t-2xl border border-zinc-700
			bg-zinc-950 p-6 shadow-2xl sm:inset-auto sm:left-1/2 sm:top-1/2 sm:-translate-x-1/2
			sm:-translate-y-1/2 sm:rounded-2xl"
		role="dialog"
		aria-modal="true"
	>
		<button
			onclick={closeModal}
			class="absolute right-4 top-4 text-zinc-500 transition-colors hover:text-white"
			aria-label="Close"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
				<path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
			</svg>
		</button>

		{#if loading}
			<div class="flex h-48 items-center justify-center text-zinc-500">Loading...</div>
		{:else if selectedGoalie}
			<div class="mb-6">
				<p class="text-sm font-medium uppercase tracking-widest text-pwhl-light">
					Goalie · {selectedGoalie.team_name}
				</p>
				<h2 class="mt-1 text-3xl font-bold text-white">
					{selectedGoalie.first_name} {selectedGoalie.last_name}
				</h2>
			</div>

			<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
				<!-- Record -->
				<div class="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
					<p class="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Record</p>
					<div class="grid grid-cols-3 gap-y-3 text-center">
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.games_played}</p>
							<p class="text-xs text-zinc-500">GP</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.wins}</p>
							<p class="text-xs text-zinc-500">W</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.losses}</p>
							<p class="text-xs text-zinc-500">L</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.ot_losses}</p>
							<p class="text-xs text-zinc-500">OTL</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.shutouts}</p>
							<p class="text-xs text-zinc-500">SO</p>
						</div>
					</div>
				</div>

				<!-- Goaltending -->
				<div class="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
					<p class="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Goaltending</p>
					<div class="grid grid-cols-2 gap-y-3 text-center">
						<div class="col-span-2">
							<p class="text-2xl font-bold text-pwhl-light">{formatSvPct(selectedGoalie.save_percentage)}</p>
							<p class="text-xs text-zinc-500">SV%</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{formatGaa(selectedGoalie.gaa)}</p>
							<p class="text-xs text-zinc-500">GAA</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.shots_against}</p>
							<p class="text-xs text-zinc-500">SA</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedGoalie.goals_against}</p>
							<p class="text-xs text-zinc-500">GA</p>
						</div>
					</div>
				</div>

				<!-- Profile -->
				<div class="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
					<p class="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Profile</p>
					<div class="space-y-2.5 text-sm">
						<div class="flex justify-between">
							<span class="text-zinc-500">Born</span>
							<span class="text-zinc-200">{formatDate(selectedGoalie.birthdate)}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Nation</span>
							<span class="text-zinc-200">{selectedGoalie.nationality ?? '—'}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Height</span>
							<span class="text-zinc-200">{selectedGoalie.height ? `${selectedGoalie.height} in` : '—'}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Weight</span>
							<span class="text-zinc-200">{selectedGoalie.weight ? `${selectedGoalie.weight} lbs` : '—'}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Catches</span>
							<span class="text-zinc-200">{selectedGoalie.shoots ?? '—'}</span>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
{/if}
