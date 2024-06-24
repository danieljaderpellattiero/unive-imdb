<template>
	<div class="header-cnt">
		<div class="unive-trademark">
			<img src="@/assets/unive_emblem.svg" alt="unive_emblem" />
		</div>
	</div>
</template>

<script setup lang="ts"></script>

<style scoped>
img {
	@apply select-none;
}

.header-cnt {
	@apply absolute top-0 mt-2 mr-4 w-full h-auto flex flex-row items-center justify-end z-1;
}

.unive-trademark {
	@apply w-12 h-auto;
}
</style>
