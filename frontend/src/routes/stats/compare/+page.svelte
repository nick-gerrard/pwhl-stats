<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import type { PageData } from './$types';
	import type { BasePlayers, SkaterCareerInfo } from '$lib/types';

	let { data }: { data: PageData } = $props();
	const players: BasePlayers[] = $derived(data.players);

	let leftQuery = $state('');
	let leftOpen = $state(false);
	let leftCareer = $state<SkaterCareerInfo[] | null>(null);
	let leftLoading = $state(false);
	let leftImgError = $state(false);

	let rightQuery = $state('');
	let rightOpen = $state(false);
	let rightCareer = $state<SkaterCareerInfo[] | null>(null);
	let rightLoading = $state(false);
	let rightImgError = $state(false);

	const leftFiltered = $derived(
		leftQuery.length > 0
			? players.filter((p) => p.name.toLowerCase().includes(leftQuery.toLowerCase())).slice(0, 8)
			: []
	);
	const rightFiltered = $derived(
		rightQuery.length > 0
			? players.filter((p) => p.name.toLowerCase().includes(rightQuery.toLowerCase())).slice(0, 8)
			: []
	);

	const leftPlayer = $derived(
		leftCareer && leftCareer.length > 0 ? leftCareer[leftCareer.length - 1] : null
	);
	const rightPlayer = $derived(
		rightCareer && rightCareer.length > 0 ? rightCareer[rightCareer.length - 1] : null
	);

	function computeTotals(career: SkaterCareerInfo[]) {
		return career.reduce(
			(acc, row) => ({
				games_played: acc.games_played + row.games_played,
				goals: acc.goals + row.goals,
				assists: acc.assists + row.assists,
				pim: acc.pim + row.pim,
				shots: acc.shots + row.shots,
				pp_goals: acc.pp_goals + row.pp_goals,
				sh_goals: acc.sh_goals + row.sh_goals,
				plus_minus: acc.plus_minus + row.plus_minus
			}),
			{
				games_played: 0,
				goals: 0,
				assists: 0,
				pim: 0,
				shots: 0,
				pp_goals: 0,
				sh_goals: 0,
				plus_minus: 0
			}
		);
	}

	const leftTotals = $derived(leftCareer ? computeTotals(leftCareer) : null);
	const rightTotals = $derived(rightCareer ? computeTotals(rightCareer) : null);

	const comparisonRows = $derived(
		leftTotals && rightTotals
			? [
					{ label: 'GP', left: leftTotals.games_played, right: rightTotals.games_played },
					{ label: 'G', left: leftTotals.goals, right: rightTotals.goals },
					{ label: 'A', left: leftTotals.assists, right: rightTotals.assists },
					{
						label: 'PTS',
						left: leftTotals.goals + leftTotals.assists,
						right: rightTotals.goals + rightTotals.assists
					},
					{ label: '+/-', left: leftTotals.plus_minus, right: rightTotals.plus_minus },
					{ label: 'PIM', left: leftTotals.pim, right: rightTotals.pim },
					{ label: 'SOG', left: leftTotals.shots, right: rightTotals.shots },
					{ label: 'PPG', left: leftTotals.pp_goals, right: rightTotals.pp_goals },
					{ label: 'SHG', left: leftTotals.sh_goals, right: rightTotals.sh_goals }
				]
			: []
	);

	function fmt(label: string, val: number) {
		if (label === '+/-' && val > 0) return `+${val}`;
		return `${val}`;
	}

	async function selectLeft(player: BasePlayers) {
		leftQuery = player.name;
		leftOpen = false;
		leftLoading = true;
		leftCareer = null;
		leftImgError = false;
		const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/${player.player_id}/career`);
		if (res.ok) leftCareer = await res.json();
		leftLoading = false;
	}

	async function selectRight(player: BasePlayers) {
		rightQuery = player.name;
		rightOpen = false;
		rightLoading = true;
		rightCareer = null;
		rightImgError = false;
		const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/${player.player_id}/career`);
		if (res.ok) rightCareer = await res.json();
		rightLoading = false;
	}
</script>

<svelte:head>
	<title>Head-to-Head — PWHL Stats</title>
</svelte:head>

<h1 class="mb-6 text-2xl font-bold text-white">Head-to-Head</h1>

<div class="mb-6 grid grid-cols-2 gap-4">
	<!-- Left search -->
	<div class="relative">
		<input
			type="text"
			bind:value={leftQuery}
			onfocus={() => (leftOpen = true)}
			onblur={() => setTimeout(() => (leftOpen = false), 150)}
			placeholder="Search skaters..."
			class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-pwhl-light"
		/>
		{#if leftOpen && leftFiltered.length > 0}
			<div
				class="absolute top-full z-10 mt-1 w-64 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-800 shadow-lg"
			>
				{#each leftFiltered as player}
					<button
						class="w-full px-3 py-2 text-left text-sm text-zinc-300 hover:bg-zinc-700 hover:text-white"
						onmousedown={() => selectLeft(player)}
					>
						{player.name}
					</button>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Right search -->
	<div class="relative">
		<input
			type="text"
			bind:value={rightQuery}
			onfocus={() => (rightOpen = true)}
			onblur={() => setTimeout(() => (rightOpen = false), 150)}
			placeholder="Search skaters..."
			class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-pwhl-light"
		/>
		{#if rightOpen && rightFiltered.length > 0}
			<div
				class="absolute top-full z-10 mt-1 w-64 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-800 shadow-lg"
			>
				{#each rightFiltered as player}
					<button
						class="w-full px-3 py-2 text-left text-sm text-zinc-300 hover:bg-zinc-700 hover:text-white"
						onmousedown={() => selectRight(player)}
					>
						{player.name}
					</button>
				{/each}
			</div>
		{/if}
	</div>
</div>

<!-- Player cards -->
<div class="mb-6 grid grid-cols-2 gap-4">
	<div class="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
		{#if leftLoading}
			<p class="text-sm text-zinc-500">Loading...</p>
		{:else if leftPlayer}
			<div class="flex flex-col items-center gap-2 text-center">
				{#if !leftImgError}
					<img
						src="https://assets.leaguestat.com/pwhl/240x240/{leftPlayer.api_id}.jpg"
						alt="{leftPlayer.first_name} {leftPlayer.last_name}"
						onerror={() => (leftImgError = true)}
						class="h-20 w-20 rounded-full object-cover ring-2 ring-zinc-700"
					/>
				{/if}
				<p class="text-xs font-medium uppercase tracking-wider text-pwhl-light">
					{leftPlayer.team_name}
				</p>
				<h2 class="text-xl font-bold leading-tight text-white">
					{leftPlayer.first_name}
					{leftPlayer.last_name}
				</h2>
			</div>
		{:else}
			<p class="text-sm text-zinc-500">Select a player</p>
		{/if}
	</div>

	<div class="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
		{#if rightLoading}
			<p class="text-sm text-zinc-500">Loading...</p>
		{:else if rightPlayer}
			<div class="flex flex-col items-center gap-2 text-center">
				{#if !rightImgError}
					<img
						src="https://assets.leaguestat.com/pwhl/240x240/{rightPlayer.api_id}.jpg"
						alt="{rightPlayer.first_name} {rightPlayer.last_name}"
						onerror={() => (rightImgError = true)}
						class="h-20 w-20 rounded-full object-cover ring-2 ring-zinc-700"
					/>
				{/if}
				<p class="text-xs font-medium uppercase tracking-wider text-pwhl-light">
					{rightPlayer.team_name}
				</p>
				<h2 class="text-xl font-bold leading-tight text-white">
					{rightPlayer.first_name}
					{rightPlayer.last_name}
				</h2>
			</div>
		{:else}
			<p class="text-sm text-zinc-500">Select a player</p>
		{/if}
	</div>
</div>

<!-- Comparison table -->
{#if comparisonRows.length > 0}
	<div class="overflow-x-auto rounded-lg border border-zinc-800">
		<table class="w-full text-sm">
			<thead>
				<tr class="border-b border-zinc-800 bg-pwhl-dark text-zinc-300">
					<th class="px-4 py-3 text-right font-medium">
						{leftPlayer?.first_name}
						{leftPlayer?.last_name}
					</th>
					<th class="px-4 py-3 text-center text-xs uppercase tracking-wider text-zinc-500">Stat</th>
					<th class="px-4 py-3 text-left font-medium">
						{rightPlayer?.first_name}
						{rightPlayer?.last_name}
					</th>
				</tr>
			</thead>
			<tbody>
				{#each comparisonRows as row, i}
					<tr
						class="border-b border-zinc-800 last:border-0 {i % 2 === 0
							? 'bg-zinc-950'
							: 'bg-zinc-900/50'}"
					>
						<td
							class="px-4 py-3 text-right text-base font-bold {row.left > row.right
								? 'text-white'
								: 'text-zinc-400'}"
						>
							{#if row.left > row.right}<span class="mr-1 text-xs text-pwhl-light">✓</span>{/if}{fmt(row.label, row.left)}
						</td>
						<td class="px-4 py-3 text-center text-xs font-medium uppercase tracking-wider text-zinc-500">
							{row.label}
						</td>
						<td
							class="px-4 py-3 text-left text-base font-bold {row.right > row.left
								? 'text-white'
								: 'text-zinc-400'}"
						>
							{fmt(row.label, row.right)}{#if row.right > row.left}<span class="ml-1 text-xs text-pwhl-light">✓</span>{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
