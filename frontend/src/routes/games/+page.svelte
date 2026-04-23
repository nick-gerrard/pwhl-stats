<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_API_URL } from '$env/static/public';
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';
	import type { LiveGame } from '$lib/types';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let liveScores: Record<string, LiveGame> = $state({});

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
		const [year, month, day] = dateStr.split('-').map(Number);
		return new Date(year, month - 1, day).toLocaleDateString('en-CA', {
			weekday: 'long',
			month: 'long',
			day: 'numeric'
		});
	}

	function formatTime(startTime: string | null) {
		if (!startTime) return null;
		return new Date(startTime).toLocaleTimeString('en-CA', {
			hour: 'numeric',
			minute: '2-digit',
			timeZoneName: 'short'
		});
	}

	function formatScore(home: number | null, away: number | null) {
		if (home === null || away === null) return null;
		return `${home} – ${away}`;
	}

	let tickedClocks: Record<string, string> = $state({});
	let runningGames: Record<string, boolean> = $state({});
	let expandedGames: Set<string> = $state(new Set());

	function toggleExpanded(gameId: string) {
		const next = new Set(expandedGames);
		if (next.has(gameId)) next.delete(gameId);
		else next.add(gameId);
		expandedGames = next;
	}

	function parseClockSeconds(clock: string): number {
		const [min, sec] = clock.split(':').map(Number);
		return min * 60 + sec;
	}

	function formatClock(totalSeconds: number): string {
		const s = Math.max(0, totalSeconds);
		return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
	}

	$effect(() => {
		if (todayGames.length === 0) return;

		const es = new EventSource(`${PUBLIC_API_URL}/live`);
		es.onmessage = (e) => {
			liveScores = JSON.parse(e.data);
		};

		return () => es.close();
	});

	$effect(() => {
		for (const [id, game] of Object.entries(liveScores)) {
			tickedClocks[id] = game.clock;
			runningGames[id] = game.clock_running;
		}
	});

	onMount(() => {
		const interval = setInterval(() => {
			for (const [id, running] of Object.entries(runningGames)) {
				if (running && tickedClocks[id]) {
					tickedClocks[id] = formatClock(parseClockSeconds(tickedClocks[id]) - 1);
				}
			}
		}, 1000);
		return () => clearInterval(interval);
	});
</script>

<svelte:head>
	<title>Games — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
	<h1 class="text-2xl font-bold">Schedule & Scores</h1>
	<div class="flex w-full gap-2 sm:w-auto">
		<SeasonSelector seasons={data.regularSeasons} class="min-w-0 flex-1 sm:flex-none" />
		<select
			bind:value={teamFilter}
			class="min-w-0 flex-1 rounded border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-300
				focus:border-pwhl-light focus:outline-none sm:flex-none"
		>
			<option value="">All Teams</option>
			{#each teams as team}
				<option value={team}>{team}</option>
			{/each}
		</select>
	</div>
</div>

{#snippet teamName(name: string, logo: string | null, align: 'left' | 'right')}
	<div class="flex flex-1 items-center gap-2 {align === 'right' ? 'flex-row-reverse' : ''}">
		{#if logo}
			<img src={logo} alt={name} class="h-8 w-8 object-contain" />
		{/if}
		<span class="font-medium text-white">{name}</span>
	</div>
{/snippet}

{#snippet liveGameCard(game: (typeof data.games)[0])}
	{@const live = liveScores[String(game.api_id)]}
	{@const score = formatScore(game.home_score, game.away_score)}
	{@const gameId = String(game.api_id)}
	{@const expanded = expandedGames.has(gameId)}
	{@const hasGoals = (live?.goals?.length ?? 0) > 0}
	<div class="rounded-lg border px-4 py-4
		{live?.status .startsWith('In Progress') ? 'border-pwhl bg-pwhl-dark/20' : 'border-zinc-800 bg-zinc-900'}">
		<!-- Mobile layout -->
		<div class="flex items-center gap-3 sm:hidden">
			<div class="flex flex-1 flex-col gap-2">
				<div class="flex items-center gap-2">
					{#if game.home_team_logo}
						<img src={game.home_team_logo} alt={game.home_team} class="h-6 w-6 shrink-0 object-contain" />
					{/if}
					<span class="font-medium text-white">{game.home_team}</span>
					{#if live?.power_play.home}
						<span class="rounded bg-pwhl-light/20 px-1.5 py-0.5 text-xs font-semibold text-pwhl-light">PP</span>
					{/if}
				</div>
				<div class="flex items-center gap-2">
					{#if game.visiting_team_logo}
						<img src={game.visiting_team_logo} alt={game.visiting_team} class="h-6 w-6 shrink-0 object-contain" />
					{/if}
					<span class="font-medium text-white">{game.visiting_team}</span>
					{#if live?.power_play.visitor}
						<span class="rounded bg-pwhl-light/20 px-1.5 py-0.5 text-xs font-semibold text-pwhl-light">PP</span>
					{/if}
				</div>
			</div>
			<div class="flex shrink-0 flex-col items-end gap-0.5">
				{#if live}
					<span class="text-lg font-bold text-white">{live.home_score} – {live.visitor_score}</span>
					{#if live.status .startsWith('In Progress')}
						<div class="flex items-center gap-1">
							<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-red-500"></span>
							<span class="text-xs text-zinc-300">{live.period} · {tickedClocks[String(game.api_id)] ?? live.clock}</span>
						</div>
						<span class="text-xs text-zinc-500">{live.home_shots}–{live.visitor_shots} SOG</span>
					{:else}
						<span class="rounded bg-zinc-700 px-2 py-0.5 text-xs text-zinc-300">Final</span>
					{/if}
				{:else if score}
					<span class="text-lg font-bold text-white">{score}</span>
					<span class="text-xs text-zinc-400">{game.status}</span>
				{:else}
					<span class="text-sm text-zinc-400">vs</span>
					{@const time = formatTime(game.start_time)}
					{#if time}<span class="text-xs text-zinc-300">{time}</span>{/if}
				{/if}
			</div>
		</div>
		<!-- Desktop layout -->
		<div class="hidden sm:flex sm:items-center sm:gap-4">
			<div class="flex flex-1 items-center justify-end gap-2">
				{#if live?.power_play.home}
					<span class="rounded bg-pwhl-light/20 px-1.5 py-0.5 text-xs font-semibold text-pwhl-light">PP</span>
				{/if}
				{@render teamName(game.home_team, game.home_team_logo, 'right')}
			</div>
			<div class="flex w-36 shrink-0 flex-col items-center">
				{#if live}
					<span class="text-lg font-bold text-white">{live.home_score} – {live.visitor_score}</span>
					{#if live.status .startsWith('In Progress')}
						<div class="mt-0.5 flex items-center gap-1.5">
							<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-red-500"></span>
							<span class="text-xs text-zinc-300">{live.period} · {tickedClocks[String(game.api_id)] ?? live.clock}</span>
						</div>
					{:else}
						<span class="mt-0.5 rounded bg-zinc-700 px-2 py-0.5 text-xs text-zinc-300">Final</span>
					{/if}
				{:else if score}
					<span class="text-lg font-bold text-white">{score}</span>
					<span class="mt-0.5 rounded bg-zinc-700 px-2 py-0.5 text-xs text-zinc-300">{game.status}</span>
				{:else}
					<span class="text-zinc-400">vs</span>
					{@const time = formatTime(game.start_time)}
					{#if time}<span class="mt-0.5 text-xs text-zinc-300">{time}</span>{/if}
				{/if}
			</div>
			<div class="flex flex-1 items-center gap-2">
				{@render teamName(game.visiting_team, game.visiting_team_logo, 'left')}
				{#if live?.power_play.visitor}
					<span class="rounded bg-pwhl-light/20 px-1.5 py-0.5 text-xs font-semibold text-pwhl-light">PP</span>
				{/if}
			</div>
		</div>
		{#if live?.status .startsWith('In Progress')}
			<div class="mt-2 hidden text-center text-xs text-zinc-500 sm:block">
				{live.home_shots} – {live.visitor_shots} SOG
			</div>
		{/if}
		{#if hasGoals}
			<button
				onclick={() => toggleExpanded(gameId)}
				class="mt-3 flex w-full items-center justify-center gap-1 border-t border-zinc-800 pt-3 text-xs text-zinc-500 hover:text-zinc-300">
				{expanded ? 'Hide goals ▲' : 'Show goals ▾'}
			</button>
			{#if expanded}
				<div class="mt-3 space-y-2">
					{#each live.goals as goal}
						<div class="flex items-start justify-between gap-2 text-xs">
							<div class="flex items-start gap-2">
								<span class="w-16 shrink-0 text-zinc-500">{goal.period} · {goal.time}</span>
								<div>
									<span class="font-medium text-white">{goal.scorer}</span>
									{#if goal.power_play}
										<span class="ml-1 rounded bg-pwhl-light/20 px-1 py-0.5 text-xs font-semibold text-pwhl-light">PP</span>
									{/if}
									{#if goal.empty_net}
										<span class="ml-1 rounded bg-zinc-700 px-1 py-0.5 text-xs font-semibold text-zinc-400">EN</span>
									{/if}
									{#if goal.assists.length > 0}
										<p class="text-zinc-500">{goal.assists.join(', ')}</p>
									{/if}
								</div>
							</div>
							<span class="shrink-0 text-zinc-500">{goal.is_home ? game.home_team : game.visiting_team}</span>
						</div>
					{/each}
				</div>
			{/if}
		{/if}
	</div>
{/snippet}

{#snippet gameCard(game: (typeof data.games)[0], highlight: boolean)}
	{@const score = formatScore(game.home_score, game.away_score)}
	<div class="rounded-lg border px-4 py-4
		{highlight ? 'border-pwhl bg-pwhl-dark/20' : 'border-zinc-800 bg-zinc-900'}">
		<!-- Mobile layout -->
		<div class="flex items-center gap-3 sm:hidden">
			<div class="flex flex-1 flex-col gap-2">
				<div class="flex items-center gap-2">
					{#if game.home_team_logo}
						<img src={game.home_team_logo} alt={game.home_team} class="h-6 w-6 shrink-0 object-contain" />
					{/if}
					<span class="font-medium text-white">{game.home_team}</span>
				</div>
				<div class="flex items-center gap-2">
					{#if game.visiting_team_logo}
						<img src={game.visiting_team_logo} alt={game.visiting_team} class="h-6 w-6 shrink-0 object-contain" />
					{/if}
					<span class="font-medium text-white">{game.visiting_team}</span>
				</div>
			</div>
			<div class="flex shrink-0 flex-col items-end gap-0.5">
				{#if score}
					<span class="text-lg font-bold text-white">{score}</span>
					<span class="text-xs text-zinc-400">{game.status}</span>
				{:else}
					<span class="text-sm text-zinc-400">vs</span>
					{@const time = formatTime(game.start_time)}
					{#if time}<span class="text-xs text-zinc-300">{time}</span>{/if}
				{/if}
			</div>
		</div>
		<!-- Desktop layout -->
		<div class="hidden sm:flex sm:items-center sm:gap-4">
			<div class="flex flex-1 justify-end">
				{@render teamName(game.home_team, game.home_team_logo, 'right')}
			</div>
			<div class="flex w-36 shrink-0 flex-col items-center">
				{#if score}
					<span class="text-lg font-bold text-white">{score}</span>
					<span class="mt-0.5 rounded px-2 py-0.5 text-xs
						{game.status === 'Final' ? 'bg-zinc-700 text-zinc-300' : 'bg-pwhl-dark/60 text-pwhl-light'}">
						{game.status}
					</span>
				{:else}
					<span class="text-zinc-400">vs</span>
					{@const time = formatTime(game.start_time)}
					{#if time}<span class="mt-0.5 text-xs text-zinc-300">{time}</span>{/if}
				{/if}
			</div>
			<div class="flex flex-1">
				{@render teamName(game.visiting_team, game.visiting_team_logo, 'left')}
			</div>
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
					{@render liveGameCard(game)}
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
