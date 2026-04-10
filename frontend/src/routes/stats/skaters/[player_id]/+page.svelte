<script lang="ts">
	import type { PageData } from './$types';
	import type { SkaterCareerInfo } from '$lib/types';

	let { data }: { data: PageData } = $props();

	const career = $derived(data.career as SkaterCareerInfo[]);
	const player = $derived(career.length > 0 ? career[career.length - 1] : null);
	const imageUrl = $derived(player ? `https://assets.leaguestat.com/pwhl/240x240/${player.api_id}.jpg` : null);

	let imgError = $state(false);

	function seasonLabel(startDate: string, endDate: string) {
		const startYear = new Date(startDate).getFullYear();
		const endYear = new Date(endDate).getFullYear();
		if (startYear === endYear) return startYear.toString();
		return `${startYear}-${endYear.toString().slice(2)}`;
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
	<title>{player ? `${player.first_name} ${player.last_name}` : 'Player'} — PWHL Stats</title>
</svelte:head>

{#if !player}
	<p class="text-zinc-500">No data found for this player.</p>
{:else}
	<!-- Header -->
	<div class="mb-8 flex items-center gap-6">
		{#if imageUrl && !imgError}
			<img
				src={imageUrl}
				alt="{player.first_name} {player.last_name}"
				onerror={() => (imgError = true)}
				class="h-24 w-24 rounded-full object-cover ring-2 ring-zinc-700"
			/>
		{/if}
		<div>
			<p class="text-sm font-medium uppercase tracking-widest text-pwhl-light">
				{player.position ?? 'Skater'} · {player.team_name}
			</p>
			<h1 class="mt-1 text-3xl font-bold text-white">
				{player.first_name}
				{player.last_name}
			</h1>
			<div class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-zinc-400">
				{#if player.birthdate}
					<span>Born {formatDate(player.birthdate)}</span>
				{/if}
				{#if player.nationality}
					<span>{player.nationality}</span>
				{/if}
				{#if player.shoots}
					<span>Shoots {player.shoots}</span>
				{/if}
				{#if player.height}
					<span>{player.height} in</span>
				{/if}
				{#if player.weight}
					<span>{player.weight} lbs</span>
				{/if}
			</div>
		</div>
	</div>

	<!-- Career stats table -->
	<h2 class="mb-3 text-lg font-semibold text-zinc-300">Career Stats</h2>
	<div class="overflow-x-auto rounded-lg border border-zinc-800">
		<table class="w-full text-sm">
			<thead>
				<tr class="border-b border-zinc-800 bg-pwhl-dark text-left text-zinc-300">
					<th class="px-4 py-3 font-medium">Season</th>
					<th class="hidden px-4 py-3 font-medium sm:table-cell">Team</th>
					<th class="px-4 py-3 text-center font-medium">GP</th>
					<th class="px-4 py-3 text-center font-medium">G</th>
					<th class="px-4 py-3 text-center font-medium">A</th>
					<th class="px-4 py-3 text-center font-medium text-white">PTS</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">+/-</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">PIM</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">SOG</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">TOI/G</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">PPG</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">SHG</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">GWG</th>
				</tr>
			</thead>
			<tbody>
				{#each career as row, i}
					<tr
						class="border-b border-zinc-800 last:border-0
							{i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}"
					>
						<td class="px-4 py-3 font-medium text-white"
							>{seasonLabel(row.start_date, row.end_date)}</td
						>
						<td class="hidden px-4 py-3 text-zinc-400 sm:table-cell">{row.team_name}</td>
						<td class="px-4 py-3 text-center text-zinc-300">{row.games_played}</td>
						<td class="px-4 py-3 text-center text-zinc-300">{row.goals}</td>
						<td class="px-4 py-3 text-center text-zinc-300">{row.assists}</td>
						<td class="px-4 py-3 text-center font-bold text-white">{row.goals + row.assists}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell"
							>{row.plus_minus > 0 ? '+' : ''}{row.plus_minus}</td
						>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.pim}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.shots}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.avg_toi ?? '—'}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.pp_goals}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.sh_goals}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.gw_goals}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
