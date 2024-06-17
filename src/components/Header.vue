<template>
	<div class="header-cnt">
		<div class="unive-trademark">
			<img src="@/assets/unive/unive_symbol.svg" alt="unive_logo" />
		</div>
		<div class="imdb-trademark">
			<img src="@/assets/imdb/imdb_logo.svg" alt="imdb_logo" />
		</div>
	</div>
</template>

<script setup lang="ts"></script>

<style scoped>
img {
	@apply select-none;
}

.header-cnt {
	@apply mt-1 w-full h-auto flex flex-row items-center justify-center;
}

.imdb-trademark {
	@apply w-16 h-auto pl-2 border-l rounded-none border-neutral-500;
}

.unive-trademark {
	@apply w-16 h-auto pr-2;
}
</style>
