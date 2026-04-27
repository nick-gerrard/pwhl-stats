<script lang="ts">
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';
	import type { PageData } from './$types';
	import type { PlayoffSeries, PlayoffTeam } from '$lib/types';

	let { data }: { data: PageData } = $props();

	const WINS_NEEDED = 3;

	function seriesWinner(s: PlayoffSeries): 'team1' | 'team2' | null {
		if (s.team1_wins >= WINS_NEEDED) return 'team1';
		if (s.team2_wins >= WINS_NEEDED) return 'team2';
		return null;
	}

	function winPips(wins: number) {
		return Array.from({ length: WINS_NEEDED }, (_, i) => i < wins);
	}

	const semisRound = data.bracket[0] ?? null;
	const finalsRound = data.bracket[1] ?? null;
</script>

<svelte:head>
	<title>Playoffs — PWHL Stats</title>
</svelte:head>

{#snippet teamRow(team: PlayoffTeam, wins: number, dimmed: boolean)}
	<div class="flex items-center gap-3 px-4 py-3 {dimmed ? 'opacity-40' : ''}">
		{#if team.logo_url}
			<img src={team.logo_url} alt={team.code} class="h-8 w-8 object-contain" />
		{:else}
			<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-400">
				{team.code}
			</div>
		{/if}
		<span class="min-w-0 flex-1 truncate text-sm {dimmed ? 'text-zinc-500' : 'text-zinc-100'}">
			{team.name}
		</span>
		<div class="flex gap-1">
			{#each winPips(wins) as filled}
				<div class="h-2.5 w-2.5 rounded-full {filled ? 'bg-pwhl-light' : 'bg-zinc-700'}"></div>
			{/each}
		</div>
		<span class="w-5 text-right text-sm font-bold tabular-nums {dimmed ? 'text-zinc-600' : 'text-zinc-300'}">
			{wins}
		</span>
	</div>
{/snippet}

{#snippet tbdRow()}
	<div class="flex items-center gap-3 px-4 py-3 opacity-40">
		<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-600">
			?
		</div>
		<span class="flex-1 text-sm text-zinc-500">TBD</span>
		<div class="flex gap-1">
			{#each winPips(0) as _}
				<div class="h-2.5 w-2.5 rounded-full bg-zinc-800"></div>
			{/each}
		</div>
		<span class="w-5 text-right text-sm font-bold text-zinc-700">0</span>
	</div>
{/snippet}

{#snippet seriesCard(series: PlayoffSeries | null, letter: string)}
	{@const winner = series ? seriesWinner(series) : null}
	<div class="w-full overflow-hidden rounded-lg border border-zinc-800 bg-zinc-900">
		<div class="flex items-center gap-2 border-b border-zinc-800 px-3 py-1.5">
			<span class="text-xs font-medium text-zinc-500">Series {letter}</span>
			{#if winner && series}
				<span class="text-xs text-pwhl-light">
					— {winner === 'team1' ? series.team1.name : series.team2.name} wins
				</span>
			{/if}
		</div>
		{#if series}
			{@render teamRow(series.team1, series.team1_wins, winner === 'team2')}
			<div class="mx-4 border-t border-zinc-800"></div>
			{@render teamRow(series.team2, series.team2_wins, winner === 'team1')}
		{:else}
			{@render tbdRow()}
			<div class="mx-4 border-t border-zinc-800"></div>
			{@render tbdRow()}
		{/if}
	</div>
{/snippet}

<div class="mb-8 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Playoffs</h1>
	<SeasonSelector seasons={data.playoffSeasons} />
</div>

{#if !semisRound}
	<div class="rounded-lg border border-zinc-800 bg-zinc-900 px-6 py-12 text-center">
		{#if data.hasExplicitSeason}
			<p class="text-zinc-400">No playoff data available for that season.</p>
		{:else}
			<p class="text-lg font-medium text-white">Playoffs haven't started yet.</p>
			<p class="mt-2 text-sm text-zinc-400">Check back when the regular season wraps up.</p>
		{/if}
	</div>
{:else}
	<!-- Mobile: stacked rounds -->
	<div class="flex flex-col gap-8 lg:hidden">
		<div>
			<h2 class="mb-3 text-xs font-semibold uppercase tracking-widest text-pwhl-light">
				{semisRound.round_name}
			</h2>
			<div class="flex flex-col gap-3">
				{#each semisRound.series as series}
					{@render seriesCard(series, series.series_letter)}
				{/each}
			</div>
		</div>
		<div>
			<h2 class="mb-3 text-xs font-semibold uppercase tracking-widest text-pwhl-light">
				{finalsRound?.round_name ?? 'Walter Cup Finals'}
			</h2>
			{#if finalsRound}
				{#each finalsRound.series as series}
					{@render seriesCard(series, series.series_letter)}
				{/each}
			{:else}
				{@render seriesCard(null, 'C')}
			{/if}
		</div>
	</div>

	<!-- Desktop: 3-column bracket (semi | finals | semi) -->
	<div class="hidden lg:flex lg:flex-col lg:items-center">
		<!-- Title row aligned to columns -->
		<div class="mb-3 flex">
			<div class="w-72 shrink-0 text-xs font-semibold uppercase tracking-widest text-pwhl-light">
				Semi-Finals
			</div>
			<div class="w-16 shrink-0"></div>
			<div class="w-72 shrink-0 text-center text-xs font-semibold uppercase tracking-widest text-pwhl-light">
				Walter Cup Finals
			</div>
			<div class="w-16 shrink-0"></div>
			<div class="w-72 shrink-0 text-right text-xs font-semibold uppercase tracking-widest text-pwhl-light">
				Semi-Finals
			</div>
		</div>

		<!-- Cards + horizontal connectors, vertically centered -->
		<div class="flex items-center">
			<div class="w-72 shrink-0">
				{@render seriesCard(semisRound.series[0], semisRound.series[0].series_letter)}
			</div>
			<div class="h-px w-16 shrink-0 bg-zinc-700"></div>
			<div class="w-72 shrink-0">
				{#if finalsRound}
					{@render seriesCard(finalsRound.series[0], finalsRound.series[0].series_letter)}
				{:else}
					{@render seriesCard(null, 'C')}
				{/if}
			</div>
			<div class="h-px w-16 shrink-0 bg-zinc-700"></div>
			<div class="w-72 shrink-0">
				{@render seriesCard(semisRound.series[1], semisRound.series[1].series_letter)}
			</div>
		</div>
	</div>
{/if}
