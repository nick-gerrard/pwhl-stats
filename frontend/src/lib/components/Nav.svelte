<script lang="ts">
	import { page } from '$app/state';
	import Logo from '$lib/components/Logo.svelte';

	const links = [
		{ href: '/', label: 'Standings' },
		{ href: '/games', label: 'Games' },
		{ href: '/playoffs', label: 'Playoffs' },
		{ href: '/stats/skaters', label: 'Skaters' },
		{ href: '/stats/goalies', label: 'Goalies' },
		{ href: '/about', label: 'About' }
	];

	let menuOpen = $state(false);
</script>

<nav class="border-b border-zinc-800 bg-zinc-900">
	<div class="mx-auto max-w-6xl px-4">
		<div class="flex h-14 items-center justify-between">
			<a href="/" class="flex items-center gap-2 text-lg font-bold tracking-tight text-pwhl-light">
				<Logo size={28} />
				PWHL Stats
			</a>

			<!-- Desktop nav -->
			<ul class="hidden gap-1 sm:flex">
				{#each links as link}
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
				{#each links as link}
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
