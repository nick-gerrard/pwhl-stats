<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Standings — PWHL Stats</title>
</svelte:head>

<h1 class="mb-6 text-2xl font-bold">Standings</h1>

<div class="overflow-x-auto rounded-lg border border-zinc-800">
	<table class="w-full text-sm">
		<thead>
			<tr class="border-b border-zinc-800 bg-pwhl-dark text-left text-zinc-300">
				<th class="px-4 py-3 font-medium">Team</th>
				<th class="px-4 py-3 text-center font-medium">GP</th>
				<th class="px-4 py-3 text-center font-medium">W</th>
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
