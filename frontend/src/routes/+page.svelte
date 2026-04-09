<script lang="ts">
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Standings — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex items-center justify-between">
	<h1 class="text-2xl font-bold">Standings</h1>
	<SeasonSelector seasons={data.regularSeasons} />
</div>

<!-- Desktop table -->
<div class="hidden overflow-x-auto rounded-lg border border-zinc-800 md:block">
	<table class="w-full text-sm">
		<thead>
			<tr class="border-b border-zinc-800 bg-pwhl-dark text-left text-zinc-300">
				<th class="px-4 py-3 font-medium">Team</th>
				<th class="px-4 py-3 text-center font-medium">GP</th>
				<th class="px-4 py-3 text-center font-medium">W</th>
				<th class="px-4 py-3 text-center font-medium">RW</th>
				<th class="px-4 py-3 text-center font-medium">L</th>
				<th class="px-4 py-3 text-center font-medium">OTW</th>
				<th class="px-4 py-3 text-center font-medium">OTL</th>
				<th class="px-4 py-3 text-center font-medium">SOW</th>
				<th class="px-4 py-3 text-center font-medium">SOL</th>
				<th class="px-4 py-3 text-center font-medium text-white">PTS</th>
			</tr>
		</thead>
		<tbody>
			{#each data.standings as row, i}
				<tr class="border-b border-zinc-800 last:border-0 transition-colors
					{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}
					hover:bg-zinc-800">
					<td class="px-4 py-3 font-medium text-white">{row.team_name}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.games_played}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.wins}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.regulation_wins}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.losses}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.ot_wins}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.ot_losses}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.shootout_wins}</td>
					<td class="px-4 py-3 text-center text-zinc-300">{row.shootout_losses}</td>
					<td class="px-4 py-3 text-center font-bold text-white">{row.points}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<!-- Mobile card list -->
<div class="rounded-lg border border-zinc-800 md:hidden">
	{#each data.standings as row, i}
		<div class="flex items-center justify-between border-b border-zinc-800 px-4 py-3 last:border-0
			{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}">
			<div>
				<div class="font-medium text-white">{row.team_name}</div>
				<div class="mt-1 text-xs text-zinc-400">
					GP {row.games_played} · W {row.wins} · RW {row.regulation_wins} · L {row.losses} · OTW {row.ot_wins} · OTL {row.ot_losses} · SOW {row.shootout_wins} · SOL {row.shootout_losses}
				</div>
			</div>
			<div class="ml-4 text-xl font-bold text-white">{row.points} <span class="text-sm font-normal text-zinc-400">PTS</span></div>
		</div>
	{/each}
</div>
