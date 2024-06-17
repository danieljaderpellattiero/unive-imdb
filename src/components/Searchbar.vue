<template>
	<div class="searchbar-cnt">
		<div class="searchbar-wrapper">
			<span ref="searchbarIcon" class="material-symbols-sharp searchbar-icon">search</span>
			<input ref="searchbarInput" class="searchbar-input" type="text" inputmode="text" :placeholder="placeholderText"
				@input="search" @focus="onFocus" @blur="onBlur" />
			<button class="searchbar-btn" @click="clearSearchbar">
				<span class="material-symbols-sharp searchbar-btn-icon">close</span>
			</button>
		</div>
	</div>
	<div class="search-results-cnt">
		<div class="search-results">
			<Hint v-for="hint in searchHints" :key="hint.titleId" :_id="hint.titleId" :title="hint.nameEng"
				:titleType="hint.titleType" :year="hint.startYear" :rating="hint.rating" :episode="hint.episode"
				:season="hint.season" />
		</div>
	</div>
</template>

<script setup lang="ts">
import axios from 'axios';
import Hint from '@/components/Hint.vue';
import { ref, onMounted, onUnmounted } from 'vue';

const searchHints = ref<any[]>([]);
const placeholderText = ref<string>('Search for a ');
const searchbarIcon = ref<HTMLSpanElement | null>(null);
const searchbarInput = ref<HTMLInputElement | null>(null);
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
const search = async (event: Event) => {
	const searchValue = (event.target as HTMLInputElement).value.toLowerCase();
	if (searchValue && searchValue !== '') {
		searchbarIcon.value!.classList.add('focused');
		axios.get(`http://localhost:3000/search/preview/${searchValue}`, {
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
		searchbarIcon.value!.classList.remove('focused');
	}
};
const clearSearchbar = () => {
	if (searchbarInput.value!.value) {
		searchbarInput.value!.value = '';
		placeholderText.value = 'Search for a ';
		searchbarIcon.value!.classList.remove('focused');
		searchHints.value = [];
		restartPlaceholderAnimation();
	}
};
const typeText = async (text: string, delay: number) => {
	for (const char of text) {
		if (!typingInterval.value) break;
		placeholderText.value += char;
		await new Promise(resolve => setTimeout(resolve, delay));
	}
};
const deleteText = async (delay: number) => {
	while (placeholderText.value.length > 'Search for a '.length) {
		placeholderText.value = placeholderText.value.slice(0, -1);
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
const onFocus = () => {
	placeholderText.value = '';
	if (typingInterval.value) {
		clearInterval(typingInterval.value);
		typingInterval.value = null;
	}
};
const onBlur = () => {
	if (searchbarInput.value && !searchbarInput.value.value) {
		restartPlaceholderAnimation();
	}
};
const restartPlaceholderAnimation = () => {
	placeholderText.value = 'Search for a ';
	typingInterval.value = setInterval(animatePlaceholder, 1000);
};
</script>

<style scoped>
.searchbar-cnt {
	@apply w-4/12 h-8;
}

.searchbar-wrapper {
	@apply w-full h-full flex flex-row items-center border rounded-full border-neutral-500 hover:border-neutral-950 duration-200;
}

.searchbar-wrapper:hover .searchbar-icon {
	@apply text-neutral-950;
}

.searchbar-icon {
	@apply px-1 font-extralight text-center text-neutral-500 duration-200 select-none;
}

.searchbar-icon.focused {
	@apply text-neutral-950;
}

.searchbar-input {
	@apply w-full rounded-r-full bg-transparent font-montserrat font-light text-base text-start text-neutral-950 tracking-wider outline-none select-none;
}

.searchbar-input::placeholder {
	@apply text-base font-light text-neutral-500 tracking-wider select-none;
}

.searchbar-btn {
	@apply flex flex-row items-center;
}

.searchbar-btn-icon {
	@apply px-1 font-extralight text-center text-neutral-500 duration-200 select-none;
}

.searchbar-btn:hover .searchbar-btn-icon {
	@apply lg:text-neutral-950;
}

.search-results-cnt {
	@apply relative w-full h-0 flex flex-col items-center;
}

.search-results {
	@apply absolute top-full mt-2 w-4/12 h-auto flex flex-col items-center shadow-xl;
}
</style>
