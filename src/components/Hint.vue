<template>
	<RouterLink :to="{ name: 'title', params: { id: _id }, query: { isEpisode: (episode && season) ? 'true' : 'false' } }"
		@mouseenter="isHintHovered = true" @mouseleave="isHintHovered = false" @click="emit('selection')" class="hint-cnt"
		:class="{ 'dark': dark }">
		<div class="hint-poster">
			<img :src="posterPreview" alt="poster_preview" />
		</div>
		<div class="hint-info-cnt">
			<div class="hint-info-panel">
				<p class="hint-title"
					:class="{ 'dark': dark, 'focus': isHintHovered && !dark, 'focus-dark': isHintHovered && dark }">
					{{ title }}</p>
				<p class="hint-year" :class="{ 'dark': dark }">{{ year }}</p>
				<div class="hint-rating">
					<span class="material-symbols-sharp hint-rating-icon">star</span>
					<p class="hint-rating-points" :class="{ 'dark': dark }">
						{{ Number.isInteger(rating) ? `${rating}.0` : rating }}/10</p>
				</div>
			</div>
			<div class="hint-info-panel">
				<p class="hint-title-type" :class="{ 'dark': dark }">{{ titleType }}</p>
				<p v-if="season && episode" class="hint-episode-info">S{{ season }}, E{{ episode }}</p>
			</div>
		</div>
	</RouterLink>
</template>

<script setup lang="ts">
import axios from 'axios';
import { RouterLink } from 'vue-router';
import { onMounted, ref, computed } from 'vue';
import defaultPoster from '@/assets/IMDb_default_poster.png';

const props = defineProps<{
	_id: string;
	titleId: string | null;
	title: string;
	titleType: string;
	startYear: number;
	endYear: number;
	rating: number;
	episode: number | null;
	season: number | null;
	dark: boolean;
}>();
const emit = defineEmits(['selection']);
const posterPreview = ref<string>('');
const isHintHovered = ref<boolean>(false);

onMounted(() => {
	axios.get(`http://img.omdbapi.com/?apikey=${import.meta.env.VITE_API_OMDB}&i=${props.titleType !== 'episode' ? props._id : props.titleId}`,
		{ responseType: 'blob' })
		.then(response => {
			posterPreview.value = URL.createObjectURL(response.data);
		})
		.catch(() => {
			posterPreview.value = defaultPoster;
		});
})
const year = computed(() => {
	return (props.startYear === props.endYear) ? props.startYear : `${props.startYear} - ${props.endYear}`;
});
</script>

<style scoped>
img {
	@apply select-none;
}

.hint-cnt {
	@apply py-2 w-full h-auto flex flex-row items-center rounded-none border-b border-neutral-500 bg-neutral-200 cursor-pointer shadow-2xl;
}

.hint-cnt.dark {
	@apply border-imdb-gold bg-neutral-950 bg-opacity-100;
}

.hint-poster {
	@apply pl-2 aspect-auto h-full flex items-center justify-center size-16;
}

.hint-info-cnt {
	@apply w-full h-auto flex flex-col items-center;
}

.hint-info-panel {
	@apply px-2 w-full h-auto flex flex-row items-center;
}

.hint-title {
	@apply font-montserrat font-medium text-base text-start text-neutral-700 tracking-normal outline-none duration-200 select-none;
}

.hint-title.dark {
	@apply text-neutral-200;
}

.hint-title.focus {
	@apply text-unive-red;
}

.hint-title.focus-dark {
	@apply text-imdb-gold;
}

.hint-year {
	@apply ml-2 grow shrink font-montserrat font-normal text-sm text-start text-neutral-500 tracking-normal outline-none select-none;
}

.hint-year.dark {
	@apply text-neutral-400;
}

.hint-rating {
	@apply flex flex-row items-center;
}

.hint-rating-icon {
	@apply font-extralight text-center text-imdb-gold select-none;
}

.hint-rating-points {
	@apply font-montserrat font-normal text-base text-end text-neutral-700 tracking-widest outline-none select-none;
}

.hint-rating-points.dark {
	@apply text-neutral-200;
}

.hint-title-type {
	@apply font-montserrat font-normal text-sm text-start text-neutral-500 tracking-normal outline-none select-none;
}

.hint-title-type.dark {
	@apply text-neutral-400;
}

.hint-episode-info {
	@apply ml-2 font-montserrat font-normal text-sm text-start text-neutral-500 tracking-normal outline-none select-none;
}

.hint-episode-info.dark {
	@apply text-neutral-400;
}
</style>
