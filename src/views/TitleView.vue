<template>
	<main>
		<Header></Header>
		<Footer></Footer>
	</main>
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
</script>

<style scoped>
main {
	@apply w-screen h-screen flex flex-col items-center justify-start bg-neutral-200;
	text-rendering: optimizeLegibility;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}
</style>
