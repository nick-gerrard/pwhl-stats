<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { page } from '$app/state';
	import type { PageData } from './$types';
	import type { PlayerInfo } from '$lib/types';
	import Pagination from '$lib/components/Pagination.svelte';
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';

	let { data }: { data: PageData } = $props();

	const PAGE_SIZE = 20;

	type SortKey = 'last_name' | 'goals' | 'assists' | 'points' | 'shots';

	let teamFilter = $state('');
	let sortKey = $state<SortKey>('points');
	let sortDir = $state<'asc' | 'desc'>('desc');
	let currentPage = $state(1);

	let selectedPlayer = $state<PlayerInfo | null>(null);
	let modalOpen = $state(false);
	let loading = $state(false);

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

	async function openPlayer(player_id: number) {
		modalOpen = true;
		loading = true;
		selectedPlayer = null;
		const seasonId = page.url.searchParams.get('season_id');
		const query = seasonId ? `?season_id=${seasonId}` : '';
		const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/${player_id}${query}`);
		selectedPlayer = await res.json();
		loading = false;
	}

	function closeModal() {
		modalOpen = false;
		selectedPlayer = null;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') closeModal();
	}

	function formatDate(dateStr: string | null) {
		if (!dateStr) return '—';
		return new Date(dateStr).toLocaleDateString('en-CA', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}
</script>

<svelte:head>
	<title>Skater Stats — PWHL Stats</title>
</svelte:head>

<svelte:window onkeydown={handleKeydown} />

<div class="mb-6 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Skater Stats</h1>
	<div class="flex gap-2">
		<SeasonSelector seasons={data.regularSeasons} />
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
				<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">
					<button onclick={() => setSort('shots')} class="hover:text-white">
						SOG{sortIndicator('shots')}
					</button>
				</th>
			</tr>
		</thead>
		<tbody>
			{#each paginated as skater, i}
				<tr
					onclick={() => openPlayer(skater.player_id)}
					class="cursor-pointer border-b border-zinc-800 last:border-0 transition-colors
						{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}
						hover:bg-zinc-800"
				>
					<td class="px-4 py-3 font-medium text-white"
						>{skater.first_name} {skater.last_name}</td
					>
					<td class="px-4 py-3 text-zinc-400">{skater.team_name}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{skater.goals}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{skater.assists}</td>
					<td class="px-4 py-3 text-center font-bold text-white"
						>{skater.goals + skater.assists}</td
					>
					<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{skater.shots}</td>
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
	<!-- Backdrop -->
	<div
		class="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
		onclick={closeModal}
		role="presentation"
	></div>

	<!-- Panel -->
	<div
		class="fixed inset-x-0 bottom-0 z-50 mx-auto max-w-2xl rounded-t-2xl border border-zinc-700
			bg-zinc-950 p-6 shadow-2xl sm:inset-auto sm:left-1/2 sm:top-1/2 sm:-translate-x-1/2
			sm:-translate-y-1/2 sm:rounded-2xl"
		role="dialog"
		aria-modal="true"
	>
		<!-- Close button -->
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
		{:else if selectedPlayer}
			<!-- Header -->
			<div class="mb-6">
				<p class="text-sm font-medium uppercase tracking-widest text-pwhl-light">
					{selectedPlayer.position ?? 'Skater'} · {selectedPlayer.team_name}
				</p>
				<h2 class="mt-1 text-3xl font-bold text-white">
					{selectedPlayer.first_name} {selectedPlayer.last_name}
				</h2>
			</div>

			<!-- Cards -->
			<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
				<!-- Season stats -->
				<div class="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
					<p class="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Season</p>
					<div class="grid grid-cols-3 gap-y-3 text-center">
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.games_played}</p>
							<p class="text-xs text-zinc-500">GP</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.goals}</p>
							<p class="text-xs text-zinc-500">G</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.assists}</p>
							<p class="text-xs text-zinc-500">A</p>
						</div>
						<div>
							<p class="text-xl font-bold text-pwhl-light">
								{selectedPlayer.goals + selectedPlayer.assists}
							</p>
							<p class="text-xs text-zinc-500">PTS</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">
								{selectedPlayer.plus_minus > 0 ? '+' : ''}{selectedPlayer.plus_minus}
							</p>
							<p class="text-xs text-zinc-500">+/-</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.pim}</p>
							<p class="text-xs text-zinc-500">PIM</p>
						</div>
					</div>
				</div>

				<!-- Shooting -->
				<div class="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
					<p class="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Shooting</p>
					<div class="grid grid-cols-2 gap-y-3 text-center">
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.shots}</p>
							<p class="text-xs text-zinc-500">SOG</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.avg_toi}</p>
							<p class="text-xs text-zinc-500">TOI/G</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.pp_goals}</p>
							<p class="text-xs text-zinc-500">PP G</p>
						</div>
						<div>
							<p class="text-xl font-bold text-white">{selectedPlayer.sh_goals}</p>
							<p class="text-xs text-zinc-500">SH G</p>
						</div>
						<div class="col-span-2">
							<p class="text-xl font-bold text-white">{selectedPlayer.gw_goals}</p>
							<p class="text-xs text-zinc-500">GW G</p>
						</div>
					</div>
				</div>

				<!-- Profile -->
				<div class="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
					<p class="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Profile</p>
					<div class="space-y-2.5 text-sm">
						<div class="flex justify-between">
							<span class="text-zinc-500">Born</span>
							<span class="text-zinc-200">{formatDate(selectedPlayer.birthdate)}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Nation</span>
							<span class="text-zinc-200">{selectedPlayer.nationality ?? '—'}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Height</span>
							<span class="text-zinc-200">{selectedPlayer.height ? `${selectedPlayer.height} in` : '—'}</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Weight</span>
							<span class="text-zinc-200">
								{selectedPlayer.weight ? `${selectedPlayer.weight} lbs` : '—'}
							</span>
						</div>
						<div class="flex justify-between">
							<span class="text-zinc-500">Shoots</span>
							<span class="text-zinc-200">{selectedPlayer.shoots ?? '—'}</span>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
{/if}
