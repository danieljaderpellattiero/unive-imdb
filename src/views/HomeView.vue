<template>
	<main>
		<div class="trademarks">
			<Trademarks></Trademarks>
		</div>
		<div class="searchbar">
			<Searchbar :include-trademark="false"></Searchbar>
		</div>
		<Footer :dark-mode="false"></Footer>
	</main>
</template>

<script setup lang="ts">
import Footer from '@/components/Footer.vue';
import Searchbar from '@/components/Searchbar.vue';
import Trademarks from '@/components/Trademarks.vue';
</script>

<style scoped>
main {
	@apply w-screen h-screen flex flex-col items-center justify-start bg-neutral-200;
	text-rendering: optimizeLegibility;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

.trademarks {
	@apply w-full h-2/6 flex flex-row items-end justify-center;
}

.searchbar {
	@apply w-full h-auto flex grow flex-col items-center justify-start;
}
</style>
