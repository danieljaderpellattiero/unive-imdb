<template>
	<main>
		<div ref="mask" class="bg-mask"></div>
		<Header></Header>
		<div class="searchbar">
			<Searchbar :include-trademark="true" @search-mode-on="searchMode" @search-mode-off="searchMode(false)">
			</Searchbar>
		</div>
		<Footer :dark-mode=darkMode></Footer>
	</main>
</template>

<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import Searchbar from '@/components/Searchbar.vue';

const props = defineProps<{
	title: string;
	page: number;
}>();
const darkMode = ref<boolean>(false);
const searchResults = ref<any[]>([]);
const mask = ref<HTMLElement | null>(null);

onMounted(() => {
	axios.get(`http://localhost:3000/search/${props.title}`, {
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		},
		params: {
			page: props.page
		}
	}).then(response => {
		searchResults.value = response.data;
	}).catch(error => {
		console.error(error);
	});
});
const searchMode = (isOn: boolean = true) => {
	mask.value!.classList.toggle('active', isOn);
	darkMode.value = isOn;
};
</script>

<style scoped>
main {
	@apply w-screen h-screen flex flex-col items-center justify-start bg-neutral-200;
	text-rendering: optimizeLegibility;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

.bg-mask {
	@apply w-full h-full absolute bg-neutral-950 opacity-0 z-1 duration-200;
}

.bg-mask.active {
	@apply opacity-80;
}

.searchbar {
	@apply w-full h-1/6 flex flex-col items-center justify-end;
}
</style>
