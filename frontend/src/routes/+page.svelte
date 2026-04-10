<script lang="ts">
	import SeasonSelector from '$lib/components/SeasonSelector.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Standings — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
	<h1 class="text-2xl font-bold">Standings</h1>
	<SeasonSelector seasons={data.regularSeasons} class="w-full sm:w-auto" />
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
		<div class="border-b border-zinc-800 px-4 py-4 last:border-0
			{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}">
			<div class="mb-3 flex items-center justify-between">
				<span class="font-medium text-white">{row.team_name}</span>
				<span class="text-xl font-bold text-white">{row.points} <span class="text-sm font-normal text-zinc-400">PTS</span></span>
			</div>
			<div class="grid grid-cols-4 gap-y-2 text-center text-xs">
				<div><p class="text-zinc-500">GP</p><p class="font-medium text-zinc-200">{row.games_played}</p></div>
				<div><p class="text-zinc-500">W</p><p class="font-medium text-zinc-200">{row.wins}</p></div>
				<div><p class="text-zinc-500">RW</p><p class="font-medium text-zinc-200">{row.regulation_wins}</p></div>
				<div><p class="text-zinc-500">L</p><p class="font-medium text-zinc-200">{row.losses}</p></div>
				<div><p class="text-zinc-500">OTW</p><p class="font-medium text-zinc-200">{row.ot_wins}</p></div>
				<div><p class="text-zinc-500">OTL</p><p class="font-medium text-zinc-200">{row.ot_losses}</p></div>
				<div><p class="text-zinc-500">SOW</p><p class="font-medium text-zinc-200">{row.shootout_wins}</p></div>
				<div><p class="text-zinc-500">SOL</p><p class="font-medium text-zinc-200">{row.shootout_losses}</p></div>
			</div>
		</div>
	{/each}
</div>
