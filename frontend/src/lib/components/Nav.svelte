<script lang="ts">
	import { page } from '$app/state';

	const links = [
		{ href: '/', label: 'Standings' },
		{ href: '/games', label: 'Games' },
		{ href: '/stats/skaters', label: 'Skaters' },
		{ href: '/stats/goalies', label: 'Goalies' },
		{ href: '/about', label: 'About' }
	];
</script>

<nav class="border-b border-zinc-800 bg-zinc-900">
	<div class="mx-auto max-w-6xl px-4">
		<div class="flex h-14 items-center justify-between">
			<a href="/" class="text-lg font-bold tracking-tight text-pwhl-light">
				PWHL Stats
			</a>
			<ul class="flex gap-1">
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
		</div>
	</div>
</nav>
