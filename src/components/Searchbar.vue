<template>
	<div class="searchbar-cnt">
		<div v-if="includeTrademark" class="imdb-trademark">
			<RouterLink :to="{ name: 'home' }">
				<img src="@/assets/imdb/imdb_logo.svg" alt="imdb_logo" />
			</RouterLink>
		</div>
		<div ref="searchbarWrapper" class="searchbar-wrapper">
			<span ref="searchbarLensIcon" class="material-symbols-sharp searchbar-lens-icon">search</span>
			<input v-model="userInput" ref="searchbarInput" class="searchbar-input" type="text" inputmode="text"
				:placeholder="placeholder" @input="handleInput" @focus="onFocus" @blur="onBlur" @click="searchMode()" @keyup.enter="textSearch" />
			<button class="searchbar-btn" @mouseenter="clearBtnHovered = true" @mouseleave="clearBtnHovered = false"
				@click="clearSearch()">
				<span ref="searchbarCloseIcon" class="material-symbols-sharp searchbar-close-icon"
					:class="{ 'focus': clearBtnHovered && !darkMode }">close
				</span>
			</button>
		</div>
	</div>
	<div ref="searchbarResults" class="searchbar-results-cnt">
		<div v-if="showResults" class="search-results">
			<Hint v-for="hint in searchHints" :key="hint.titleId" :_id="hint.titleId" :title="hint.nameEng"
				:titleType="hint.titleType" :year="hint.startYear" :rating="hint.rating" :episode="hint.episode"
				:season="hint.season" :darkMode="includeTrademark ? true : false" @mouseenter="selectingResult = true"
				@mouseleave="selectingResult = false" @hintSelected="clearSearch(true)" />
		</div>
	</div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref, onMounted, onUnmounted } from 'vue';
import Hint from '@/components/Hint.vue';

const props = defineProps<{
	includeTrademark: boolean;
}>();
const emit = defineEmits(['searchModeOn', 'searchModeOff']);
const router = useRouter();
const userInput = ref<string>('');
const searchHints = ref<any[]>([]);
const darkMode = ref<boolean>(false);
const showResults = ref<boolean>(false);
const clearBtnHovered = ref<boolean>(false);
const selectingResult = ref<boolean>(false);
const placeholder = ref<string>('Search for a ');
const searchbarTimeoutId = ref<number | null>(null);
const searchbarResults = ref<HTMLDivElement | null>(null);
const searchbarInput = ref<HTMLInputElement | null>(null);
const searchbarWrapper = ref<HTMLDivElement | null>(null);
const searchbarLensIcon = ref<HTMLSpanElement | null>(null);
const searchbarCloseIcon = ref<HTMLSpanElement | null>(null);
const contentTypes = ref<string[]>(['tvSerie', 'video', 'short', 'tvMovie', 'videoGame', 'tvShort', 'tvSpecial', 'movie', 'tvMiniSerie', 'tvEpisode']);
let contentIndex = ref<number>(0);
let isUserTyping = ref<boolean>(false);
let typingInterval = ref<number | null>(null);

onMounted(() => {
	typingInterval.value = setInterval(animatePlaceholder, 1000);
});
onUnmounted(() => {
	if (typingInterval.value) {
		clearInterval(typingInterval.value);
		typingInterval.value = null;
	}
});
const handleInput = () => {
	if (searchbarTimeoutId.value) {
		clearTimeout(searchbarTimeoutId.value);
	}
	searchbarTimeoutId.value = setTimeout(search, 500);
};
const search = async () => {
	if (userInput.value && userInput.value !== '') {
		axios.get(`http://localhost:3000/search/preview/${userInput.value.toLowerCase()}`, {
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			}
		}).then(response => {
			searchHints.value = response.data;
		}).catch(error => {
			console.error(error);
		});
	} else {
		searchHints.value = [];
		placeholder.value = 'Search for a ';
	}
};
const clearSearch = (selection: boolean = false) => {
	if (userInput.value) {
		userInput.value = '';
		searchHints.value = [];
		placeholder.value = 'Search for a ';
		restartPlaceholderAnimation();
	}
	if (selection) {
		showResults.value = false;
	}
};
const textSearch = () => {
	if (userInput.value) {
		router.push({ name: 'search', params: { title: userInput.value}, query: { page: 1}});
	}
};
const typeText = async (text: string, delay: number) => {
	for (const char of text) {
		if (!typingInterval.value) break;
		placeholder.value += char;
		await new Promise(resolve => setTimeout(resolve, delay));
	}
};
const deleteText = async (delay: number) => {
	while (placeholder.value.length > 'Search for a '.length) {
		placeholder.value = placeholder.value.slice(0, -1);
		await new Promise(resolve => setTimeout(resolve, delay));
	}
};
const animatePlaceholder = async () => {
	if (!isUserTyping.value && searchbarInput.value && !searchbarInput.value.matches(':focus')) {
		isUserTyping.value = true;
		const text = contentTypes.value[contentIndex.value];
		await typeText(text, 150);
		await typeText('...', 500);
		await new Promise(resolve => setTimeout(resolve, 2000));
		await deleteText(100);
		contentIndex.value = (contentIndex.value + 1) % contentTypes.value.length;
		isUserTyping.value = false;
	}
};
const restartPlaceholderAnimation = () => {
	placeholder.value = 'Search for a ';
	typingInterval.value = setInterval(animatePlaceholder, 1000);
};
const onFocus = () => {
	placeholder.value = '';
	if (typingInterval.value) {
		clearInterval(typingInterval.value);
		typingInterval.value = null;
	}
};
const onBlur = () => {
	searchMode(false, true);
	searchbarWrapper.value!.classList.remove('focus');
	if (searchbarInput.value && !userInput.value) {
		restartPlaceholderAnimation();
	}
};
const searchMode = (rootCaller: boolean = true, onBlur: boolean = false) => {
	let changeUI = false;
	showResults.value = !onBlur ? true : selectingResult.value ? true : false;
	searchbarWrapper.value!.classList.add('focus');
	if (rootCaller) {
		if (!darkMode.value && props.includeTrademark) {
			changeUI = true;
			emit('searchModeOn');
			darkMode.value = true;
		}
	} else {
		if (darkMode.value) {
			changeUI = true;
			emit('searchModeOff');
			darkMode.value = false;
		}
	}
	if (changeUI) {
		searchbarWrapper.value!.classList.toggle('dark', darkMode.value);
		searchbarInput.value!.classList.toggle('dark', darkMode.value);
		searchbarLensIcon.value!.classList.toggle('dark', darkMode.value);
		searchbarCloseIcon.value!.classList.toggle('dark', darkMode.value);
	}
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
	@apply w-full rounded-r-full bg-transparent font-montserrat font-light text-base text-start text-neutral-950 tracking-wider outline-none duration-200 select-none;
}

.searchbar-input.dark {
	@apply text-neutral-200;
}

.searchbar-input::placeholder {
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
