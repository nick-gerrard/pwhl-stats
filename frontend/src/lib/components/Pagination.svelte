<script lang="ts">
	let {
		currentPage,
		totalPages,
		onPageChange
	}: {
		currentPage: number;
		totalPages: number;
		onPageChange: (n: number) => void;
	} = $props();
</script>

<div class="flex items-center justify-between text-sm text-zinc-400">
	<span>{totalPages === 0 ? 'No results' : `Page ${currentPage} of ${totalPages}`}</span>
	<div class="flex gap-2">
		<button
			onclick={() => onPageChange(currentPage - 1)}
			disabled={currentPage <= 1}
			class="rounded px-3 py-1.5 transition-colors
				enabled:hover:bg-zinc-800 enabled:hover:text-white
				disabled:cursor-not-allowed disabled:opacity-40"
		>
			← Prev
		</button>
		<button
			onclick={() => onPageChange(currentPage + 1)}
			disabled={currentPage >= totalPages}
			class="rounded px-3 py-1.5 transition-colors
				enabled:hover:bg-zinc-800 enabled:hover:text-white
				disabled:cursor-not-allowed disabled:opacity-40"
		>
			Next →
		</button>
	</div>
</div>
