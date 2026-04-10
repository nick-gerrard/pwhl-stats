<script lang="ts">
	import type { PageData } from './$types';
	import type { SkaterLeaderboard, GoalieLeaderboard } from '$lib/types';

	let { data }: { data: PageData } = $props();

	function formatSvPct(pct: number | null) {
		if (pct === null) return '—';
		return pct.toFixed(3).replace(/^0/, '');
	}

	const skaterCards = [
		{
			title: 'Goals',
			players: data.skaterLeaders.goals.map((p: SkaterLeaderboard) => ({
				name: `${p.first_name} ${p.last_name}`,
				team: p.team_name,
				display: p.goals.toString()
			}))
		},
		{
			title: 'Assists',
			players: data.skaterLeaders.assists.map((p: SkaterLeaderboard) => ({
				name: `${p.first_name} ${p.last_name}`,
				team: p.team_name,
				display: p.assists.toString()
			}))
		},
		{
			title: 'Points',
			players: data.skaterLeaders.points.map((p: SkaterLeaderboard) => ({
				name: `${p.first_name} ${p.last_name}`,
				team: p.team_name,
				display: p.points.toString()
			}))
		}
	];

	const goalieCards = [
		{
			title: 'Wins',
			players: data.goalieLeaders.wins.map((p: GoalieLeaderboard) => ({
				name: `${p.first_name} ${p.last_name}`,
				team: p.team_name,
				display: p.wins.toString()
			}))
		},
		{
			title: 'Save %',
			players: data.goalieLeaders.savePct.map((p: GoalieLeaderboard) => ({
				name: `${p.first_name} ${p.last_name}`,
				team: p.team_name,
				display: formatSvPct(p.save_percentage)
			}))
		},
		{
			title: 'Shutouts',
			players: data.goalieLeaders.shutouts.map((p: GoalieLeaderboard) => ({
				name: `${p.first_name} ${p.last_name}`,
				team: p.team_name,
				display: p.shutouts.toString()
			}))
		}
	];
</script>

<svelte:head>
	<title>Leaders — PWHL Stats</title>
</svelte:head>

<h1 class="mb-8 text-2xl font-bold">Leaders</h1>

{#snippet leaderCard(title: string, players: { name: string; team: string; display: string }[])}
	<div class="rounded-xl border border-zinc-800 bg-zinc-900">
		<div class="border-b border-zinc-800 px-4 py-3">
			<h3 class="font-semibold text-white">{title}</h3>
		</div>
		<ol>
			{#each players as player, i}
				<li
					class="flex items-center gap-3 px-4 py-2.5
						{i < players.length - 1 ? 'border-b border-zinc-800/50' : ''}
						{i % 2 === 0 ? '' : 'bg-zinc-950/40'}"
				>
					<span class="w-5 shrink-0 text-center text-sm text-zinc-500">{i + 1}</span>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-medium text-white">{player.name}</p>
						<p class="truncate text-xs text-zinc-500">{player.team}</p>
					</div>
					<span class="shrink-0 text-sm font-bold text-pwhl-light">{player.display}</span>
				</li>
			{/each}
		</ol>
	</div>
{/snippet}

<section class="mb-10">
	<h2 class="mb-4 text-lg font-semibold text-zinc-300">Skaters</h2>
	<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
		{#each skaterCards as card}
			{@render leaderCard(card.title, card.players)}
		{/each}
	</div>
</section>

<section>
	<h2 class="mb-4 text-lg font-semibold text-zinc-300">Goalies</h2>
	<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
		{#each goalieCards as card}
			{@render leaderCard(card.title, card.players)}
		{/each}
	</div>
</section>
