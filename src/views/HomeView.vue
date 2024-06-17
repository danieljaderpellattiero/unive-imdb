<template>
	<main>
		<div class="trademarks-wrapper">
			<Trademarks></Trademarks>
		</div>
		<Searchbar></Searchbar>
		<Footer></Footer>
	</main>
</template>

<script setup lang="ts">
import Footer from '@/components/Footer.vue';
import Searchbar from '@/components/Searchbar.vue';
import Trademarks from '@/components/Trademarks.vue';
</script>

<style scoped>
main {
	@apply w-screen h-screen flex flex-col items-center justify-center bg-neutral-200;
	text-rendering: optimizeLegibility;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

.trademarks-wrapper {
	@apply absolute w-screen flex flex-row justify-center -translate-y-3/4;
}
</style>
