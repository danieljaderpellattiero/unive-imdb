<template>
	<div class="searchbar-cnt">
		<div v-if="trademarks" class="imdb-trademark">
			<RouterLink :to="{ name: 'home' }" class="imdb-trademark-link">
				<img src="@/assets/IMDb_logo.svg" alt="imdb_logo" />
			</RouterLink>
		</div>
		<div ref="sBarWrapper" class="searchbar-wrapper">
			<span ref="sBarLensIcon" class="material-symbols-sharp searchbar-lens-icon">search</span>
			<input v-model="input" ref="sBarInput" class="searchbar-input" type="text" inputmode="text"
				:placeholder="sBarPHolder" @input="searchHandler" @focus="onFocus" @blur="onBlur" @click="searchMode()"
				@keyup.enter="fullSearch" />
			<button class="searchbar-btn" @mouseenter="isClearHovered = true" @mouseleave="isClearHovered = false"
				@click="clearSearch()">
				<span ref="sBarCloseIcon" class="material-symbols-sharp searchbar-close-icon"
					:class="{ 'focus': isClearHovered && !dark }">close
				</span>
			</button>
		</div>
	</div>
	<div ref="sBarHints" class="searchbar-results-cnt">
		<div v-if="hintsVisible" class="search-results">
			<Hint v-for="hint in hints" :key="hint._id" :_id="hint._id" :titleId="hint.titleId" :title="hint.nameEng"
				:titleType="hint.titleType" :startYear="hint.startYear" :endYear="hint.endYear" :rating="hint.rating"
				:episode="hint.episode" :season="hint.season" :dark="trademarks ? true : false"
				@mouseenter="isHintSelected = true" @mouseleave="isHintSelected = false" @selection="clearSearch(true)" />
		</div>
	</div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { useRouter } from 'vue-router';
import { onMounted, ref, onUnmounted } from 'vue';
import Hint from '@/components/Hint.vue';

const props = defineProps<{
	trademarks: boolean;
}>();
const emit = defineEmits(['searchOn', 'searchOff']);
const router = useRouter();
const hints = ref<any[]>([]);
const input = ref<string>('');
const dark = ref<boolean>(false);
const hintsVisible = ref<boolean>(false);
const isClearHovered = ref<boolean>(false);
const isHintSelected = ref<boolean>(false);
const sBarPHolder = ref<string>('Search for a ');
const sBarHints = ref<HTMLDivElement | null>(null);
const sBarInput = ref<HTMLInputElement | null>(null);
const sBarWrapper = ref<HTMLDivElement | null>(null);
const sBarTimeoutId = ref<number | null>(null);
const sBarLensIcon = ref<HTMLSpanElement | null>(null);
const sBarCloseIcon = ref<HTMLSpanElement | null>(null);
const sBarPHolderItems = ref<string[]>(['tvSerie', 'video', 'short', 'tvMovie', 'videoGame', 'tvShort', 'tvSpecial', 'movie', 'tvMiniSerie', 'tvEpisode']);
let itemIndex = ref<number>(0);
let isTyping = ref<boolean>(false);
let typingInterval = ref<number | null>(null);

onMounted(() => {
	typingInterval.value = window.setInterval(pHolderAnimation, 1000);
});
onUnmounted(() => {
	if (typingInterval.value) {
		window.clearInterval(typingInterval.value);
		typingInterval.value = null;
	}
});
const searchHandler = () => {
	if (sBarTimeoutId.value) {
		window.clearTimeout(sBarTimeoutId.value);
	}
	sBarTimeoutId.value = window.setTimeout(quickSearch, 500);
};
const quickSearch = async () => {
	if (input.value && input.value !== '') {
		axios.get(`http://localhost:3000/search/preview/${input.value.toLowerCase()}`)
			.then(response => {
				hints.value = response.data;
			}).catch(error => {
				console.error(error);
			});
	} else {
		hints.value = [];
		sBarPHolder.value = 'Search for a ';
	}
};
const clearSearch = (selection: boolean = false) => {
	if (input.value) {
		input.value = '';
		hints.value = [];
		sBarPHolder.value = 'Search for a ';
		restartPHolderAnimation();
	}
	if (selection) {
		hintsVisible.value = false;
	}
};
const onFocus = () => {
	sBarPHolder.value = '';
	if (typingInterval.value) {
		clearInterval(typingInterval.value);
		typingInterval.value = null;
	}
};
const onBlur = () => {
	searchMode(false, true);
	sBarWrapper.value!.classList.remove('focus');
	if (sBarInput.value && !input.value) {
		restartPHolderAnimation();
	}
};
const searchMode = (rootCaller: boolean = true, onBlur: boolean = false) => {
	let changeUI = false;
	hintsVisible.value = !onBlur ? true : isHintSelected.value ? true : false;
	sBarWrapper.value!.classList.add('focus');
	if (rootCaller) {
		if (!dark.value && props.trademarks) {
			changeUI = true;
			emit('searchOn');
			dark.value = true;
		}
	} else {
		if (dark.value) {
			changeUI = true;
			emit('searchOff');
			dark.value = false;
		}
	}
	if (changeUI) {
		sBarWrapper.value!.classList.toggle('dark', dark.value);
		sBarInput.value!.classList.toggle('dark', dark.value);
		sBarLensIcon.value!.classList.toggle('dark', dark.value);
		sBarCloseIcon.value!.classList.toggle('dark', dark.value);
	}
};
const fullSearch = () => {
	if (input.value) {
		onBlur();
		router.push({ name: 'search', params: { titleOrId: input.value }, query: { page: 1, findEpisodes: 'false' } });
	}
};
const pHolderAnimation = async () => {
	if (!isTyping.value && sBarInput.value && !sBarInput.value.matches(':focus')) {
		isTyping.value = true;
		const text = sBarPHolderItems.value[itemIndex.value];
		await animateType(text, 150);
		await animateType('...', 500);
		await new Promise(resolve => setTimeout(resolve, 2000));
		await animateDelete(100);
		itemIndex.value = (itemIndex.value + 1) % sBarPHolderItems.value.length;
		isTyping.value = false;
	}
};
const animateType = async (text: string, delay: number) => {
	for (const char of text) {
		if (!typingInterval.value) break;
		sBarPHolder.value += char;
		await new Promise(resolve => setTimeout(resolve, delay));
	}
};
const animateDelete = async (delay: number) => {
	while (sBarPHolder.value.length > 'Search for a '.length) {
		sBarPHolder.value = sBarPHolder.value.slice(0, -1);
		await new Promise(resolve => setTimeout(resolve, delay));
	}
};
const restartPHolderAnimation = () => {
	sBarPHolder.value = 'Search for a ';
	typingInterval.value = window.setInterval(pHolderAnimation, 1000);
};
</script>

<style scoped>
img {
	@apply select-none;
}

.searchbar-cnt {
	@apply w-4/12 h-8 flex flex-row items-center space-x-2 z-1;
}

.imdb-trademark {
	@apply w-14 h-auto;
}

.imdb-trademark-link {
	@apply flex flex-row items-center justify-center;
}

.searchbar-wrapper {
	@apply w-full h-full flex flex-row items-center border rounded-full border-neutral-500 hover:border-neutral-950 duration-200;
}

.searchbar-wrapper.focus {
	@apply border-neutral-950;
}

.searchbar-wrapper.dark {
	@apply border-neutral-200 bg-neutral-950 bg-opacity-50;
}

.searchbar-lens-icon {
	@apply px-1 font-extralight text-center text-neutral-500 duration-200 select-none;
}

.searchbar-lens-icon.dark {
	@apply text-neutral-200;
}

.searchbar-input {
	@apply w-full bg-transparent font-montserrat font-light text-base text-start text-neutral-950 tracking-wider outline-none duration-200 select-none;
}

.searchbar-input.dark {
	@apply text-neutral-200;
}

.searchbar-input::sBarPHolder {
	@apply text-base font-light text-neutral-500 tracking-wider select-none;
}

.searchbar-btn {
	@apply flex flex-row items-center;
}

.searchbar-close-icon {
	@apply px-1 font-extralight text-center text-neutral-500 duration-200 select-none;
}

.searchbar-close-icon.dark {
	@apply text-imdb-gold;
}

.searchbar-close-icon.focus {
	@apply text-neutral-950;
}

.searchbar-results-cnt {
	@apply relative w-full h-0 flex flex-col items-center z-1;
}

.search-results {
	@apply absolute top-full mt-2 w-4/12 h-auto flex flex-col items-center shadow-xl;
}
</style>
