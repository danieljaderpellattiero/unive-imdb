<template>
	<main>
		<div ref="mask" class="mask"></div>
		<Header></Header>
		<div class="searchbar">
			<Searchbar :trademarks="true" @search-on="searchMode" @search-off="searchMode(false)">
			</Searchbar>
		</div>
		<div class="content">
			<Title :id="id" :is-episode="isEpisode"></Title>
		</div>
		<Footer :dark="dark"></Footer>
	</main>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { onMounted, ref, watch } from 'vue';
import Title from '@/components/Title.vue';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import Searchbar from '@/components/Searchbar.vue';

const route = useRoute();
const id = ref<string>('');
const dark = ref<boolean>(false);
const isEpisode = ref<boolean>(false);
const mask = ref<HTMLElement | null>(null);

onMounted(() => {
	id.value = route.params.id as string;
	isEpisode.value = route.query.isEpisode === 'true';
});
watch(route, (newRoute) => {
	id.value = newRoute.params.id as string;
	isEpisode.value = newRoute.query.isEpisode === 'true';
}, { immediate: true, deep: true });
const searchMode = (isOn: boolean = true) => {
	mask.value!.classList.toggle('active', isOn);
	dark.value = isOn;
};
</script>

<style scoped>
main {
	@apply w-screen h-screen flex flex-col items-center justify-start bg-neutral-200;
	text-rendering: optimizeLegibility;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

.mask {
	@apply w-full h-full absolute bg-neutral-950 opacity-0 duration-200 -z-1;
}

.mask.active {
	@apply opacity-80 z-1;
}

.searchbar {
	@apply w-full h-1/6 flex flex-col items-center justify-end;
}

.content {
	@apply pt-40 w-full h-auto flex grow flex-col items-center justify-start;
}
</style>
