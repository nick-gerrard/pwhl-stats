<script lang="ts">
	let { size = 32 }: { size?: number } = $props();
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	viewBox="0 0 100 100"
	width={size}
	height={size}
	aria-label="PWHL Stats logo"
>
	<!-- Back stick (right-to-left) -->
	<polyline
		points="76,5 47,63 25,71"
		fill="none"
		stroke="#3f3f46"
		stroke-width="9"
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
	<!-- Front stick (left-to-right) -->
	<polyline
		points="24,5 53,63 75,71"
		fill="none"
		stroke="#d4d4d8"
		stroke-width="9"
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
	<!-- Puck -->
	<ellipse cx="50" cy="82" rx="23" ry="13" fill="#09090b" stroke="#3f3f46" stroke-width="1.5" />
	<ellipse cx="50" cy="79" rx="18" ry="8" fill="#27272a" />
</svg>
