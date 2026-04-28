<script lang="ts">
	import { page } from '$app/state';
	import Logo from '$lib/components/Logo.svelte';

	const topLinks = [
		{ href: '/', label: 'Standings' },
		{ href: '/games', label: 'Games' },
		{ href: '/playoffs', label: 'Playoffs' }
	];

	const statsLinks = [
		{ href: '/stats/skaters', label: 'Skaters' },
		{ href: '/stats/goalies', label: 'Goalies' },
		{ href: '/stats/leaders', label: 'Leaders' },
		{ href: '/stats/compare', label: 'Compare' }
	];

	const allLinks = [...topLinks, ...statsLinks, { href: '/about', label: 'About' }];

	let menuOpen = $state(false);
	let statsOpen = $state(false);

	const statsActive = $derived(page.url.pathname.startsWith('/stats'));

	function handleWindowClick(e: MouseEvent) {
		if (!(e.target as Element).closest('[data-stats-dropdown]')) {
			statsOpen = false;
		}
	}
</script>

<svelte:window onclick={handleWindowClick} />

<nav class="border-b border-zinc-800 bg-zinc-900">
	<div class="mx-auto max-w-6xl px-4">
		<div class="flex h-14 items-center justify-between">
			<a href="/" class="flex items-center gap-2 text-lg font-bold tracking-tight text-pwhl-light">
				<Logo size={28} />
				PWHL Stats
			</a>

			<!-- Desktop nav -->
			<ul class="hidden items-center gap-1 sm:flex">
				{#each topLinks as link}
					<li>
						<a
							href={link.href}
							class="rounded px-3 py-1.5 text-sm transition-colors
								{page.url.pathname === link.href
								? 'bg-pwhl text-white'
								: 'text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
						>
							{link.label}
						</a>
					</li>
				{/each}

				<!-- Stats dropdown -->
				<li class="relative" data-stats-dropdown>
					<button
						onclick={() => (statsOpen = !statsOpen)}
						class="flex items-center gap-1 rounded px-3 py-1.5 text-sm transition-colors
							{statsActive
							? 'bg-pwhl text-white'
							: 'text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
					>
						Stats
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-3 w-3 transition-transform {statsOpen ? 'rotate-180' : ''}"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
					{#if statsOpen}
						<div
							class="absolute right-0 top-full z-50 mt-1 w-40 overflow-hidden rounded-lg border border-zinc-700 bg-zinc-800 shadow-lg"
						>
							{#each statsLinks as link}
								<a
									href={link.href}
									onclick={() => (statsOpen = false)}
									class="block px-3 py-2 text-sm transition-colors
										{page.url.pathname === link.href
										? 'bg-pwhl/20 text-white'
										: 'text-zinc-300 hover:bg-zinc-700 hover:text-white'}"
								>
									{link.label}
								</a>
							{/each}
						</div>
					{/if}
				</li>

				<li>
					<a
						href="/about"
						class="rounded px-3 py-1.5 text-sm transition-colors
							{page.url.pathname === '/about'
							? 'bg-pwhl text-white'
							: 'text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
					>
						About
					</a>
				</li>
			</ul>

			<!-- Hamburger button -->
			<button
				onclick={() => (menuOpen = !menuOpen)}
				class="flex items-center justify-center rounded p-2 text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white sm:hidden"
				aria-label="Toggle menu"
			>
				{#if menuOpen}
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
					</svg>
				{:else}
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
					</svg>
				{/if}
			</button>
		</div>
	</div>

	<!-- Mobile menu -->
	{#if menuOpen}
		<div class="border-t border-zinc-800 sm:hidden">
			<ul class="flex flex-col px-4 py-2">
				{#each allLinks as link}
					<li>
						<a
							href={link.href}
							onclick={() => (menuOpen = false)}
							class="block rounded px-3 py-2 text-sm transition-colors
								{page.url.pathname === link.href
								? 'bg-pwhl text-white'
								: 'text-zinc-400 hover:bg-zinc-800 hover:text-white'}"
						>
							{link.label}
						</a>
					</li>
				{/each}
			</ul>
		</div>
	{/if}
</nav>
