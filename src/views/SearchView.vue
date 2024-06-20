<template>
	<main>
		<div ref="mask" class="mask"></div>
		<Header></Header>
		<div class="searchbar">
			<Searchbar :include-trademark="true" @search-mode-on="searchMode" @search-mode-off="searchMode(false)">
			</Searchbar>
		</div>
		<div class="search-results">
			<Hint v-for="hint in searchHints" :key="hint._id" :_id="hint._id" :titleId="hint.titleId" :title="hint.nameEng"
				:titleType="hint.titleType" :start-year="hint.startYear" :end-year="hint.endYear" :rating="hint.rating"
				:episode="hint.episode" :season="hint.season" :darkMode="false" />
		</div>
		<div class="nav-cnt">
			<div class="nav">
				<div class="back-control">
					<span class="material-symbols-sharp nav-icon" :class="{ 'disabled': page === 1 }"
						@click="navigate(false)">arrow_back</span>
				</div>
				<p class="nav-info">{{ navInfo }}</p>
				<div class="forth-control">
					<span class="material-symbols-sharp nav-icon" @click="navigate()">arrow_forward</span>
				</div>
			</div>
		</div>
		<Footer :dark-mode=darkMode></Footer>
	</main>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Hint from '@/components/Hint.vue';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import Searchbar from '@/components/Searchbar.vue';

const route = useRoute();
const router = useRouter();
const page = ref<number>(1);
const titleOrId = ref<string>('');
const searchHints = ref<any[]>([]);
const darkMode = ref<boolean>(false);
const findEpisodes = ref<boolean>(false);
const mask = ref<HTMLElement | null>(null);

const fetchData = async (titleOrId: string, page: number, findEpisodes: boolean) => {
	axios.get(`http://localhost:3000/search/${findEpisodes ? 'episodes/' : ''}${titleOrId.toLowerCase()}`, {
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		},
		params: {
			page: page
		}
	}).then(response => {
		searchHints.value = response.data;
	}).catch(error => {
		console.error(error);
	});
};
watch(route, (newRoute) => {
	page.value = Number(newRoute.query.page);
	titleOrId.value = newRoute.params.titleOrId as string;
	findEpisodes.value = newRoute.query.findEpisodes === 'true';
	fetchData(titleOrId.value, page.value, findEpisodes.value);
}, { immediate: true, deep: true });
const navInfo = computed(() => {
	return `#${page.value}`;
});
const searchMode = (isOn: boolean = true) => {
	mask.value!.classList.toggle('active', isOn);
	darkMode.value = isOn;
};
const navigate = (forward: boolean = true) => {
	if (forward || page.value > 1) {
		router.push({
			name: 'search',
			params: {
				titleOrId: titleOrId.value,
			},
			query: {
				page: forward ? page.value + 1 : page.value - 1,
				findEpisodes: String(findEpisodes.value)
			}
		});
	}
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
	@apply w-full h-1/12 flex flex-col items-center justify-end;
}

.search-results {
	@apply w-6/12 h-auto my-4 flex flex-col items-center justify-center border-none;
}

.nav-cnt {
	@apply w-full h-auto flex flex-col grow items-center justify-center;
}

.nav {
	@apply flex flex-row items-center justify-center border rounded-full border-neutral-500;
}

.back-control,
.forth-control {
	@apply w-auto h-auto flex flex-row items-center justify-center cursor-pointer;
}

.nav-icon {
	@apply px-1 font-extralight text-center text-neutral-500 hover:text-neutral-950 duration-200 select-none;
}

.nav-icon.disabled {
	@apply text-neutral-300 cursor-not-allowed;
}

.nav-info {
	@apply px-1 font-montserrat font-normal text-lg text-neutral-500 tracking-widest select-none;
}
</style>
