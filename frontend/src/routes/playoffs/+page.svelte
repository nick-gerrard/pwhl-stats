<script lang="ts">
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';
	import type { PageData } from './$types';
	import type { PlayoffSeries } from '$lib/types';

	let { data }: { data: PageData } = $props();

	function seriesWinner(s: PlayoffSeries): 'team1' | 'team2' | null {
		const needed = s.series_name.toLowerCase().includes('final') && !s.series_name.toLowerCase().includes('semi') ? 4 : 3;
		if (s.team1_wins >= needed) return 'team1';
		if (s.team2_wins >= needed) return 'team2';
		return null;
	}

	function winPips(wins: number, needed: number) {
		return Array.from({ length: needed }, (_, i) => i < wins);
	}
</script>

<svelte:head>
	<title>Playoffs — PWHL Stats</title>
</svelte:head>

<div class="mb-8 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Playoffs</h1>
	<SeasonSelector seasons={data.playoffSeasons} />
</div>

{#if data.bracket.length === 0}
	<div class="rounded-lg border border-zinc-800 bg-zinc-900 px-6 py-12 text-center">
		{#if data.hasExplicitSeason}
			<p class="text-zinc-400">No playoff data available for that season.</p>
		{:else}
			<p class="text-lg font-medium text-white">Playoffs haven't started yet.</p>
			<p class="mt-2 text-sm text-zinc-400">Check back when the regular season wraps up.</p>
		{/if}
	</div>
{:else}
	<div class="flex flex-col gap-10 lg:flex-row lg:items-start lg:gap-6">
		{#each data.bracket as round}
			<div class="flex-1">
				<h2 class="mb-4 text-xs font-semibold uppercase tracking-widest text-pwhl-light">
					{round.round_name}
				</h2>
				<div class="space-y-4">
					{#each round.series as series}
						{@const winner = seriesWinner(series)}
						{@const needed = series.series_name.toLowerCase().includes('final') && !series.series_name.toLowerCase().includes('semi') ? 4 : 3}
						<div class="overflow-hidden rounded-lg border border-zinc-800 bg-zinc-900">
							<div class="border-b border-zinc-800 px-3 py-1.5">
								<span class="text-xs font-medium text-zinc-500">Series {series.series_letter}</span>
							</div>

							<!-- Team 1 -->
							<div class="flex items-center gap-3 px-4 py-3 {winner === 'team2' ? 'opacity-40' : ''}">
								<span class="w-10 text-sm font-bold {winner === 'team1' ? 'text-white' : 'text-zinc-300'}">
									{series.team1.code}
								</span>
								<span class="flex-1 text-sm {winner === 'team1' ? 'text-white' : 'text-zinc-400'}">
									{series.team1.name}
								</span>
								<div class="flex gap-1">
									{#each winPips(series.team1_wins, needed) as filled}
										<div class="h-2.5 w-2.5 rounded-full {filled ? 'bg-pwhl-light' : 'bg-zinc-700'}"></div>
									{/each}
								</div>
								<span class="w-4 text-right text-sm font-bold {winner === 'team1' ? 'text-white' : 'text-zinc-400'}">
									{series.team1_wins}
								</span>
							</div>

							<!-- Team 2 -->
							<div class="flex items-center gap-3 px-4 py-3 {winner === 'team1' ? 'opacity-40' : ''}">
								<span class="w-10 text-sm font-bold {winner === 'team2' ? 'text-white' : 'text-zinc-300'}">
									{series.team2.code}
								</span>
								<span class="flex-1 text-sm {winner === 'team2' ? 'text-white' : 'text-zinc-400'}">
									{series.team2.name}
								</span>
								<div class="flex gap-1">
									{#each winPips(series.team2_wins, needed) as filled}
										<div class="h-2.5 w-2.5 rounded-full {filled ? 'bg-pwhl-light' : 'bg-zinc-700'}"></div>
									{/each}
								</div>
								<span class="w-4 text-right text-sm font-bold {winner === 'team2' ? 'text-white' : 'text-zinc-400'}">
									{series.team2_wins}
								</span>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	</div>
{/if}
