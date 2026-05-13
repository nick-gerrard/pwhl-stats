<script lang="ts">
	import type { PageData } from './$types';
	import type { GoalieCareerInfo } from '$lib/types';

	let { data }: { data: PageData } = $props();

	const career = $derived(data.career as GoalieCareerInfo[]);
	const player = $derived(career.length > 0 ? career[career.length - 1] : null);
	const imageUrl = $derived(player ? `https://assets.leaguestat.com/pwhl/240x240/${player.api_id}.jpg` : null);

	let imgError = $state(false);

	const totals = $derived(
		career.reduce(
			(acc, row) => ({
				games_played: acc.games_played + row.games_played,
				wins: acc.wins + row.wins,
				losses: acc.losses + row.losses,
				ot_losses: acc.ot_losses + row.ot_losses,
				shutouts: acc.shutouts + row.shutouts,
				shots_against: acc.shots_against + row.shots_against,
				goals_against: acc.goals_against + row.goals_against,
				minutes_played: acc.minutes_played + row.minutes_played
			}),
			{ games_played: 0, wins: 0, losses: 0, ot_losses: 0, shutouts: 0, shots_against: 0, goals_against: 0, minutes_played: 0 }
		)
	);

	function seasonLabel(startDate: string, endDate: string) {
		const startYear = new Date(startDate).getFullYear();
		const endYear = new Date(endDate).getFullYear();
		if (startYear === endYear) return startYear.toString();
		return `${startYear}-${endYear.toString().slice(2)}`;
	}

	function formatSvPct(pct: number | null) {
		if (pct === null) return '—';
		return pct.toFixed(3).replace(/^0/, '');
	}

	function formatGaa(gaa: number | null) {
		if (gaa === null) return '—';
		return gaa.toFixed(2);
	}

	function formatDate(dateStr: string | null) {
		if (!dateStr) return '—';
		return new Date(dateStr).toLocaleDateString('en-CA', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	function formatHeight(inches: number | null) {
		if (!inches) return '—';
		return `${Math.floor(inches / 12)}'${inches % 12}"`;
	}
</script>

<svelte:head>
	<title>{player ? `${player.first_name} ${player.last_name}` : 'Goalie'} — PWHL Stats</title>
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
				Goalie · {player.team_name}
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
					<span>Catches {player.shoots}</span>
				{/if}
				{#if player.height}
					<span>{formatHeight(player.height)}</span>
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
					<th class="px-4 py-3 text-center font-medium">W</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">L</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">OTL</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">SO</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">SA</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">GA</th>
					<th class="px-4 py-3 text-center font-medium text-white">SV%</th>
					<th class="hidden px-4 py-3 text-center font-medium sm:table-cell">GAA</th>
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
						<td class="px-4 py-3 text-center text-zinc-300">{row.wins}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.losses}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.ot_losses}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.shutouts}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.shots_against}</td>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{row.goals_against}</td>
						<td class="px-4 py-3 text-center font-bold text-white"
							>{formatSvPct(row.save_percentage)}</td
						>
						<td class="hidden px-4 py-3 text-center text-zinc-300 sm:table-cell">{formatGaa(row.gaa)}</td>
					</tr>
				{/each}
				{#if career.length > 1}
					<tr class="border-t-2 border-zinc-700 bg-zinc-900">
						<td class="px-4 py-3 font-semibold text-zinc-300">Career</td>
						<td class="hidden px-4 py-3 sm:table-cell"></td>
						<td class="px-4 py-3 text-center font-semibold text-zinc-300">{totals.games_played}</td>
						<td class="px-4 py-3 text-center font-semibold text-zinc-300">{totals.wins}</td>
						<td class="hidden px-4 py-3 text-center font-semibold text-zinc-300 sm:table-cell">{totals.losses}</td>
						<td class="hidden px-4 py-3 text-center font-semibold text-zinc-300 sm:table-cell">{totals.ot_losses}</td>
						<td class="hidden px-4 py-3 text-center font-semibold text-zinc-300 sm:table-cell">{totals.shutouts}</td>
						<td class="hidden px-4 py-3 text-center font-semibold text-zinc-300 sm:table-cell">{totals.shots_against}</td>
						<td class="hidden px-4 py-3 text-center font-semibold text-zinc-300 sm:table-cell">{totals.goals_against}</td>
						<td class="px-4 py-3 text-center font-bold text-white sm:table-cell"></td>
						<td class="hidden px-4 py-3 text-center sm:table-cell"></td>
					</tr>
				{/if}
			</tbody>
		</table>
	</div>
{/if}
