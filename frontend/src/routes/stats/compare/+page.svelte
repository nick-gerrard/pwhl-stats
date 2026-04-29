<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import type { PageData } from './$types';
	import type { BasePlayers, SkaterCareerInfo, GoalieCareerInfo } from '$lib/types';

	let { data }: { data: PageData } = $props();

	type Mode = 'skaters' | 'goalies';
	type ComparisonRow = {
		label: string;
		left: number;
		right: number;
		leftDisplay: string;
		rightDisplay: string;
		higherIsBetter: boolean | null;
	};

	let mode = $state<Mode>('skaters');

	const playerList = $derived<BasePlayers[]>(mode === 'skaters' ? data.skaters : data.goalies);

	let leftQuery = $state('');
	let leftOpen = $state(false);
	let leftSkaterCareer = $state<SkaterCareerInfo[] | null>(null);
	let leftGoalieCareer = $state<GoalieCareerInfo[] | null>(null);
	let leftLoading = $state(false);
	let leftImgError = $state(false);

	let rightQuery = $state('');
	let rightOpen = $state(false);
	let rightSkaterCareer = $state<SkaterCareerInfo[] | null>(null);
	let rightGoalieCareer = $state<GoalieCareerInfo[] | null>(null);
	let rightLoading = $state(false);
	let rightImgError = $state(false);

	const leftFiltered = $derived(
		leftQuery.length > 0
			? playerList.filter((p) => p.name.toLowerCase().includes(leftQuery.toLowerCase())).slice(0, 8)
			: []
	);
	const rightFiltered = $derived(
		rightQuery.length > 0
			? playerList.filter((p) => p.name.toLowerCase().includes(rightQuery.toLowerCase())).slice(0, 8)
			: []
	);

	const leftPlayer = $derived(
		mode === 'skaters'
			? (leftSkaterCareer?.length ? leftSkaterCareer[leftSkaterCareer.length - 1] : null)
			: (leftGoalieCareer?.length ? leftGoalieCareer[leftGoalieCareer.length - 1] : null)
	);
	const rightPlayer = $derived(
		mode === 'skaters'
			? (rightSkaterCareer?.length ? rightSkaterCareer[rightSkaterCareer.length - 1] : null)
			: (rightGoalieCareer?.length ? rightGoalieCareer[rightGoalieCareer.length - 1] : null)
	);

	function computeSkaterTotals(career: SkaterCareerInfo[]) {
		return career.reduce(
			(acc, row) => ({
				games_played: acc.games_played + row.games_played,
				goals: acc.goals + row.goals,
				assists: acc.assists + row.assists,
				pim: acc.pim + row.pim,
				shots: acc.shots + row.shots,
				pp_goals: acc.pp_goals + row.pp_goals,
				sh_goals: acc.sh_goals + row.sh_goals,
				plus_minus: acc.plus_minus + row.plus_minus
			}),
			{ games_played: 0, goals: 0, assists: 0, pim: 0, shots: 0, pp_goals: 0, sh_goals: 0, plus_minus: 0 }
		);
	}

	function computeGoalieTotals(career: GoalieCareerInfo[]) {
		const sums = career.reduce(
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
		);
		const save_percentage =
			sums.shots_against > 0
				? (sums.shots_against - sums.goals_against) / sums.shots_against
				: null;
		const gaa = sums.minutes_played > 0 ? (sums.goals_against / sums.minutes_played) * 60 : null;
		return { ...sums, save_percentage, gaa };
	}

	function fmtSvPct(val: number | null) {
		if (val === null) return '—';
		return val.toFixed(3).replace(/^0/, '');
	}

	function fmtGaa(val: number | null) {
		if (val === null) return '—';
		return val.toFixed(2);
	}

	function buildSkaterRows(
		lt: ReturnType<typeof computeSkaterTotals>,
		rt: ReturnType<typeof computeSkaterTotals>
	): ComparisonRow[] {
		const n = (v: number) => `${v}`;
		const pm = (v: number) => (v > 0 ? `+${v}` : `${v}`);
		return [
			{ label: 'GP', left: lt.games_played, right: rt.games_played, leftDisplay: n(lt.games_played), rightDisplay: n(rt.games_played), higherIsBetter: null },
			{ label: 'G', left: lt.goals, right: rt.goals, leftDisplay: n(lt.goals), rightDisplay: n(rt.goals), higherIsBetter: true },
			{ label: 'A', left: lt.assists, right: rt.assists, leftDisplay: n(lt.assists), rightDisplay: n(rt.assists), higherIsBetter: true },
			{ label: 'PTS', left: lt.goals + lt.assists, right: rt.goals + rt.assists, leftDisplay: n(lt.goals + lt.assists), rightDisplay: n(rt.goals + rt.assists), higherIsBetter: true },
			{ label: '+/-', left: lt.plus_minus, right: rt.plus_minus, leftDisplay: pm(lt.plus_minus), rightDisplay: pm(rt.plus_minus), higherIsBetter: true },
			{ label: 'PIM', left: lt.pim, right: rt.pim, leftDisplay: n(lt.pim), rightDisplay: n(rt.pim), higherIsBetter: null },
			{ label: 'SOG', left: lt.shots, right: rt.shots, leftDisplay: n(lt.shots), rightDisplay: n(rt.shots), higherIsBetter: true },
			{ label: 'PPG', left: lt.pp_goals, right: rt.pp_goals, leftDisplay: n(lt.pp_goals), rightDisplay: n(rt.pp_goals), higherIsBetter: true },
			{ label: 'SHG', left: lt.sh_goals, right: rt.sh_goals, leftDisplay: n(lt.sh_goals), rightDisplay: n(rt.sh_goals), higherIsBetter: true }
		];
	}

	function buildGoalieRows(
		lt: ReturnType<typeof computeGoalieTotals>,
		rt: ReturnType<typeof computeGoalieTotals>
	): ComparisonRow[] {
		const n = (v: number) => `${v}`;
		return [
			{ label: 'GP', left: lt.games_played, right: rt.games_played, leftDisplay: n(lt.games_played), rightDisplay: n(rt.games_played), higherIsBetter: null },
			{ label: 'W', left: lt.wins, right: rt.wins, leftDisplay: n(lt.wins), rightDisplay: n(rt.wins), higherIsBetter: true },
			{ label: 'L', left: lt.losses, right: rt.losses, leftDisplay: n(lt.losses), rightDisplay: n(rt.losses), higherIsBetter: false },
			{ label: 'OTL', left: lt.ot_losses, right: rt.ot_losses, leftDisplay: n(lt.ot_losses), rightDisplay: n(rt.ot_losses), higherIsBetter: false },
			{ label: 'SO', left: lt.shutouts, right: rt.shutouts, leftDisplay: n(lt.shutouts), rightDisplay: n(rt.shutouts), higherIsBetter: true },
			{ label: 'SV%', left: lt.save_percentage ?? 0, right: rt.save_percentage ?? 0, leftDisplay: fmtSvPct(lt.save_percentage), rightDisplay: fmtSvPct(rt.save_percentage), higherIsBetter: true },
			{ label: 'GAA', left: lt.gaa ?? 0, right: rt.gaa ?? 0, leftDisplay: fmtGaa(lt.gaa), rightDisplay: fmtGaa(rt.gaa), higherIsBetter: false },
			{ label: 'SA', left: lt.shots_against, right: rt.shots_against, leftDisplay: n(lt.shots_against), rightDisplay: n(rt.shots_against), higherIsBetter: null },
			{ label: 'GA', left: lt.goals_against, right: rt.goals_against, leftDisplay: n(lt.goals_against), rightDisplay: n(rt.goals_against), higherIsBetter: false }
		];
	}

	const leftSkaterTotals = $derived(leftSkaterCareer ? computeSkaterTotals(leftSkaterCareer) : null);
	const rightSkaterTotals = $derived(rightSkaterCareer ? computeSkaterTotals(rightSkaterCareer) : null);
	const leftGoalieTotals = $derived(leftGoalieCareer ? computeGoalieTotals(leftGoalieCareer) : null);
	const rightGoalieTotals = $derived(rightGoalieCareer ? computeGoalieTotals(rightGoalieCareer) : null);

	const comparisonRows = $derived.by<ComparisonRow[]>(() => {
		if (mode === 'skaters') {
			return leftSkaterTotals && rightSkaterTotals
				? buildSkaterRows(leftSkaterTotals, rightSkaterTotals)
				: [];
		} else {
			return leftGoalieTotals && rightGoalieTotals
				? buildGoalieRows(leftGoalieTotals, rightGoalieTotals)
				: [];
		}
	});

	function isLeftWinner(row: ComparisonRow) {
		if (row.higherIsBetter === true) return row.left > row.right;
		if (row.higherIsBetter === false) return row.left < row.right;
		return false;
	}

	function isRightWinner(row: ComparisonRow) {
		if (row.higherIsBetter === true) return row.right > row.left;
		if (row.higherIsBetter === false) return row.right < row.left;
		return false;
	}

	function switchMode(newMode: Mode) {
		mode = newMode;
		leftQuery = '';
		leftSkaterCareer = null;
		leftGoalieCareer = null;
		leftImgError = false;
		rightQuery = '';
		rightSkaterCareer = null;
		rightGoalieCareer = null;
		rightImgError = false;
	}

	async function selectLeft(player: BasePlayers) {
		leftQuery = player.name;
		leftOpen = false;
		leftLoading = true;
		leftImgError = false;
		if (mode === 'skaters') {
			leftSkaterCareer = null;
			const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/${player.player_id}/career`);
			if (res.ok) leftSkaterCareer = await res.json();
		} else {
			leftGoalieCareer = null;
			const res = await fetch(`${PUBLIC_API_URL}/stats/goalies/${player.player_id}/career`);
			if (res.ok) leftGoalieCareer = await res.json();
		}
		leftLoading = false;
	}

	async function selectRight(player: BasePlayers) {
		rightQuery = player.name;
		rightOpen = false;
		rightLoading = true;
		rightImgError = false;
		if (mode === 'skaters') {
			rightSkaterCareer = null;
			const res = await fetch(`${PUBLIC_API_URL}/stats/skaters/${player.player_id}/career`);
			if (res.ok) rightSkaterCareer = await res.json();
		} else {
			rightGoalieCareer = null;
			const res = await fetch(`${PUBLIC_API_URL}/stats/goalies/${player.player_id}/career`);
			if (res.ok) rightGoalieCareer = await res.json();
		}
		rightLoading = false;
	}
</script>

<svelte:head>
	<title>Head-to-Head — PWHL Stats</title>
</svelte:head>

<div class="mb-6 flex items-center justify-between">
	<h1 class="text-2xl font-bold text-white">Head-to-Head</h1>
	<div class="flex rounded-lg border border-zinc-700 p-0.5">
		<button
			onclick={() => switchMode('skaters')}
			class="rounded-md px-4 py-1.5 text-sm font-medium transition-colors
				{mode === 'skaters' ? 'bg-zinc-700 text-white' : 'text-zinc-400 hover:text-white'}"
		>
			Skaters
		</button>
		<button
			onclick={() => switchMode('goalies')}
			class="rounded-md px-4 py-1.5 text-sm font-medium transition-colors
				{mode === 'goalies' ? 'bg-zinc-700 text-white' : 'text-zinc-400 hover:text-white'}"
		>
			Goalies
		</button>
	</div>
</div>

<div class="mb-6 grid grid-cols-2 gap-4">
	<!-- Left search -->
	<div class="relative">
		<input
			type="text"
			bind:value={leftQuery}
			onfocus={() => (leftOpen = true)}
			onblur={() => setTimeout(() => (leftOpen = false), 150)}
			placeholder="Search {mode}..."
			class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-pwhl-light"
		/>
		{#if leftOpen && leftFiltered.length > 0}
			<div class="absolute top-full z-10 mt-1 w-64 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-800 shadow-lg">
				{#each leftFiltered as player}
					<button
						class="w-full px-3 py-2 text-left text-sm text-zinc-300 hover:bg-zinc-700 hover:text-white"
						onmousedown={() => selectLeft(player)}
					>
						{player.name}
					</button>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Right search -->
	<div class="relative">
		<input
			type="text"
			bind:value={rightQuery}
			onfocus={() => (rightOpen = true)}
			onblur={() => setTimeout(() => (rightOpen = false), 150)}
			placeholder="Search {mode}..."
			class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-pwhl-light"
		/>
		{#if rightOpen && rightFiltered.length > 0}
			<div class="absolute top-full z-10 mt-1 w-64 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-800 shadow-lg">
				{#each rightFiltered as player}
					<button
						class="w-full px-3 py-2 text-left text-sm text-zinc-300 hover:bg-zinc-700 hover:text-white"
						onmousedown={() => selectRight(player)}
					>
						{player.name}
					</button>
				{/each}
			</div>
		{/if}
	</div>
</div>

<!-- Player cards -->
<div class="mb-6 grid grid-cols-2 gap-4">
	<div class="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
		{#if leftLoading}
			<p class="text-sm text-zinc-500">Loading...</p>
		{:else if leftPlayer}
			<div class="flex flex-col items-center gap-2 text-center">
				{#if !leftImgError}
					<img
						src="https://assets.leaguestat.com/pwhl/240x240/{leftPlayer.api_id}.jpg"
						alt="{leftPlayer.first_name} {leftPlayer.last_name}"
						onerror={() => (leftImgError = true)}
						class="h-20 w-20 rounded-full object-cover ring-2 ring-zinc-700"
					/>
				{/if}
				<p class="text-xs font-medium uppercase tracking-wider text-pwhl-light">
					{leftPlayer.team_name}
				</p>
				<h2 class="text-xl font-bold leading-tight text-white">
					{leftPlayer.first_name}
					{leftPlayer.last_name}
				</h2>
			</div>
		{:else}
			<p class="text-sm text-zinc-500">Select a player</p>
		{/if}
	</div>

	<div class="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
		{#if rightLoading}
			<p class="text-sm text-zinc-500">Loading...</p>
		{:else if rightPlayer}
			<div class="flex flex-col items-center gap-2 text-center">
				{#if !rightImgError}
					<img
						src="https://assets.leaguestat.com/pwhl/240x240/{rightPlayer.api_id}.jpg"
						alt="{rightPlayer.first_name} {rightPlayer.last_name}"
						onerror={() => (rightImgError = true)}
						class="h-20 w-20 rounded-full object-cover ring-2 ring-zinc-700"
					/>
				{/if}
				<p class="text-xs font-medium uppercase tracking-wider text-pwhl-light">
					{rightPlayer.team_name}
				</p>
				<h2 class="text-xl font-bold leading-tight text-white">
					{rightPlayer.first_name}
					{rightPlayer.last_name}
				</h2>
			</div>
		{:else}
			<p class="text-sm text-zinc-500">Select a player</p>
		{/if}
	</div>
</div>

<!-- Comparison table -->
{#if comparisonRows.length > 0}
	<div class="overflow-x-auto rounded-lg border border-zinc-800">
		<table class="w-full text-sm">
			<thead>
				<tr class="border-b border-zinc-800 bg-pwhl-dark text-zinc-300">
					<th class="px-4 py-3 text-right font-medium">
						{leftPlayer?.first_name}
						{leftPlayer?.last_name}
					</th>
					<th class="px-4 py-3 text-center text-xs uppercase tracking-wider text-zinc-500">Stat</th>
					<th class="px-4 py-3 text-left font-medium">
						{rightPlayer?.first_name}
						{rightPlayer?.last_name}
					</th>
				</tr>
			</thead>
			<tbody>
				{#each comparisonRows as row, i}
					<tr class="border-b border-zinc-800 last:border-0 {i % 2 === 0 ? 'bg-zinc-950' : 'bg-zinc-900/50'}">
						<td class="px-4 py-3 text-right text-base font-bold {isLeftWinner(row) ? 'text-white' : 'text-zinc-400'}">
							{#if isLeftWinner(row)}<span class="mr-1 text-xs text-pwhl-light">✓</span>{/if}{row.leftDisplay}
						</td>
						<td class="px-4 py-3 text-center text-xs font-medium uppercase tracking-wider text-zinc-500">
							{row.label}
						</td>
						<td class="px-4 py-3 text-left text-base font-bold {isRightWinner(row) ? 'text-white' : 'text-zinc-400'}">
							{row.rightDisplay}{#if isRightWinner(row)}<span class="ml-1 text-xs text-pwhl-light">✓</span>{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
