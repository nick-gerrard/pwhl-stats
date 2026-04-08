<script lang="ts">
	import '../app.css';
	import Nav from '$lib/components/Nav.svelte';

	let { children } = $props();
</script>

<Nav />
<main class="mx-auto max-w-6xl px-4 py-8">
	{@render children()}
</main>
