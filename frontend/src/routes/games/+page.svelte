<script lang="ts">
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let teamFilter = $state('');

	// Use Swedish locale for reliable YYYY-MM-DD local date string
	const today = new Date().toLocaleDateString('sv');

	const teams = $derived(
		[...new Set(data.games.flatMap((g) => [g.home_team, g.visiting_team]))].sort()
	);

	const filtered = $derived(
		teamFilter
			? data.games.filter((g) => g.home_team === teamFilter || g.visiting_team === teamFilter)
			: data.games
	);

	function groupByDate(games: typeof data.games) {
		const map = new Map<string, typeof data.games>();
		for (const game of games) {
			const existing = map.get(game.date) ?? [];
			existing.push(game);
			map.set(game.date, existing);
		}
		return map;
	}

	const todayGames = $derived(filtered.filter((g) => g.date === today));
	const upcomingGames = $derived(
		filtered.filter((g) => g.date > today).sort((a, b) => a.date.localeCompare(b.date))
	);
	const pastGames = $derived(
		filtered.filter((g) => g.date < today).sort((a, b) => b.date.localeCompare(a.date))
	);

	const upcomingByDate = $derived(groupByDate(upcomingGames));
	const pastByDate = $derived(groupByDate(pastGames));

	function formatDate(dateStr: string) {
		return new Date(dateStr).toLocaleDateString('en-CA', {
			weekday: 'long',
			month: 'long',
			day: 'numeric'
		});
	}

	function formatScore(home: number | null, away: number | null) {
		if (home === null || away === null) return null;
		return `${home} – ${away}`;
	}
</script>

<svelte:head>
	<title>Games — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Schedule & Scores</h1>
	<div class="flex gap-2">
		<SeasonSelector seasons={data.regularSeasons} />
		<select
			bind:value={teamFilter}
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

{#snippet gameCard(game: (typeof data.games)[0], highlight: boolean)}
	{@const score = formatScore(game.home_score, game.away_score)}
	<div class="rounded-lg border px-4 py-3
		{highlight ? 'border-pwhl bg-pwhl-dark/20' : 'border-zinc-800 bg-zinc-900'}">
		<div class="flex items-center gap-4">
			<span class="flex-1 text-right font-medium text-white">{game.home_team}</span>
			<div class="flex w-28 flex-col items-center">
				{#if score}
					<span class="text-lg font-bold text-white">{score}</span>
				{:else}
					<span class="text-zinc-500">vs</span>
				{/if}
				<span class="mt-0.5 rounded px-2 py-0.5 text-xs
					{game.status === 'Final'
						? 'bg-zinc-700 text-zinc-300'
						: 'bg-pwhl-dark/60 text-pwhl-light'}">
					{game.status}
				</span>
			</div>
			<span class="flex-1 font-medium text-white">{game.visiting_team}</span>
		</div>
	</div>
{/snippet}

{#snippet dateGroup(entries: [string, typeof data.games][], highlight: boolean)}
	{#each entries as [date, games]}
		<div>
			<h2 class="mb-3 text-sm font-semibold uppercase tracking-wider
				{highlight ? 'text-white' : 'text-pwhl-light'}">
				{formatDate(date)}
			</h2>
			<div class="space-y-2">
				{#each games as game}
					{@render gameCard(game, highlight)}
				{/each}
			</div>
		</div>
	{/each}
{/snippet}

<div class="space-y-8">
	{#if todayGames.length > 0}
		<div>
			<h2 class="mb-3 text-sm font-semibold uppercase tracking-wider text-white">
				Today
			</h2>
			<div class="space-y-2">
				{#each todayGames as game}
					{@render gameCard(game, true)}
				{/each}
			</div>
		</div>
	{/if}

	{#if upcomingByDate.size > 0}
		<div class="space-y-8">
			<h2 class="text-lg font-semibold text-zinc-300">Upcoming</h2>
			{@render dateGroup([...upcomingByDate.entries()], false)}
		</div>
	{/if}

	{#if pastByDate.size > 0}
		<div class="space-y-8">
			<h2 class="text-lg font-semibold text-zinc-300">Recent Results</h2>
			{@render dateGroup([...pastByDate.entries()], false)}
		</div>
	{/if}
</div>
