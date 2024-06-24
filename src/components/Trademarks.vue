<template>
	<div class="trademarks-cnt">
		<div class="unive-trademark">
			<img src="@/assets/unive_logo.svg" alt="unive_logo" />
		</div>
		<div class="imdb-trademark">
			<img src="@/assets/IMDb_logo.svg" alt="IMDb_logo" />
		</div>
	</div>
</template>

<script setup lang="ts"></script>

<style scoped>
img {
	@apply select-none;
}

.trademarks-cnt {
	@apply w-4/12 h-auto flex flex-row items-center justify-evenly;
}

.imdb-trademark {
	@apply w-4/12 h-auto;
}

.unive-trademark {
	@apply w-5/12 h-auto;
}
</style>
