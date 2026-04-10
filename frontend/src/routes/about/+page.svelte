<script lang="ts">
	import Logo from '$lib/components/Logo.svelte';
</script>

<svelte:head>
	<title>About — PWHL Stats</title>
</svelte:head>

<div class="mx-auto max-w-2xl">
	<div class="mb-6 flex items-center gap-4">
		<Logo size={64} />
		<h1 class="text-2xl font-bold">About</h1>
	</div>

	<div class="space-y-4 text-zinc-300">
		<p>
			PWHL Stats is an unofficial fan-made stats site for the
			<a
				href="https://www.thepwhl.com"
				target="_blank"
				rel="noopener noreferrer"
				class="text-blue-400 hover:underline">Professional Women's Hockey League</a
			>. It is not affiliated with or endorsed by the PWHL.
		</p>
		<p>
			Stats are sourced from publicly available data and updated daily. This site exists purely as
			a personal project and has no commercial intent.
		</p>
		<p>
			Built with <a
				href="https://fastapi.tiangolo.com"
				target="_blank"
				rel="noopener noreferrer"
				class="text-blue-400 hover:underline">FastAPI</a
			>,
			<a
				href="https://kit.svelte.dev"
				target="_blank"
				rel="noopener noreferrer"
				class="text-blue-400 hover:underline">SvelteKit</a
			>, and PostgreSQL. Source code available on
			<a
				href="https://github.com/nick-gerrard/pwhl-stats"
				target="_blank"
				rel="noopener noreferrer"
				class="text-blue-400 hover:underline">GitHub</a
			>.
		</p>
	</div>
</div>
