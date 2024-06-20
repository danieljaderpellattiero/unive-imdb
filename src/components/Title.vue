<template>
	<div class="title-cnt">
		<div class="title-poster">
			<img :src="poster" alt="title_poster">
		</div>
		<div class="title-info-cnt">
			<div class="title-info-panel">
				<p class="title-eng-name">{{ nameEng }}</p>
				<div class="title-rating">
					<span class="material-symbols-sharp title-rating-icon">star</span>
					<p class="title-rating-points">{{ rating }}/10</p>
					<p class="title-votes">({{ votes }})</p>
				</div>
			</div>
			<div class="title-info-panel">
				<p class="title-name">{{ name }}</p>
			</div>
			<div class="title-info-panel">
				<p class="title-year">{{ year }}</p>
			</div>
			<div class="title-info-panel">
				<p v-if="isEpisode" class="title-episode-info">{{ episodeInfo }}</p>
				<p class="title-runtime">{{ runtime }}</p>
			</div>
			<div class="title-info-panel">
				<p class="title-genres">{{ genres }}</p>
				<span v-if="isAdult" class="material-symbols-sharp title-explicit-icon">explicit</span>
			</div>
			<div class="title-info-panel-separator"></div>
			<div class="title-info-panel">
				<p class="title-directors-prefix">{{ directors.length > 1 ? 'Director' : 'Directors' }}</p>
			</div>
			<div class="title-info-panel">
				<p class="title-directors">{{ directors }}</p>
			</div>
			<div class="title-info-panel">
				<p class="title-writers-prefix">{{ writers.length > 1 ? 'Writer' : 'Writers' }}</p>
			</div>
			<div class="title-info-panel">
				<p class="title-writers">{{ writers }}</p>
			</div>
			<div class="title-info-panel">
				<p class="title-principals-prefix">Cast</p>
			</div>
			<div class="title-info-panel">
				<p class="title-principals">{{ principals }}</p>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import axios from 'axios';
import type Title from '../types/Title';
import { ref, onMounted, watch, computed } from 'vue';

const props = defineProps<{
	id: string;
	isEpisode: boolean;
}>();
const titleInfo = ref<Title>({
	titleId: '',
	name: '',
	nameEng: '',
	genres: [],
	isAdult: -1,
	startYear: -1,
	endYear: -1,
	episode: -1,
	season: -1,
	runtime: -1,
	rating: -1,
	votes: -1,
	directors: [],
	writers: [],
	principals: [],
});
const poster = ref<string>('');

onMounted(() => {
	fetchTitleData(props.id, props.isEpisode);
})
const fetchTitleData = async (id: string, isEpisode: boolean) => {
	axios.get(`http://localhost:3000/${isEpisode ? 'episode' : 'title'}/${id}`, {
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'
		}
	}).then(response => {
		titleInfo.value = response.data[0];
		axios.get(`http://img.omdbapi.com/?apikey=${import.meta.env.VITE_API_OMDB}&i=${isEpisode ? titleInfo.value.titleId : id}`, { responseType: 'blob' })
			.then(response => {
				poster.value = URL.createObjectURL(response.data);
			})
			.catch(() => {
				poster.value = '/public/IMDb_default_poster.png';
			});
	}).catch(error => {
		console.error(error);
	});
}
watch(props, (newProps) => {
	fetchTitleData(newProps.id, newProps.isEpisode);
}, { immediate: true, deep: true });
const nameEng = computed(() => {
	return titleInfo.value.nameEng ? titleInfo.value.nameEng : 'unknown';
});
const name = computed(() => {
	return titleInfo.value.name ? titleInfo.value.name : 'unknown';
});
const rating = computed(() => {
	return Number.isInteger(titleInfo.value.rating) ? `${titleInfo.value.rating}.0` : `${titleInfo.value.rating}`;
});
const votes = computed(() => {
	return titleInfo.value.votes ? titleInfo.value.votes : '-1';
});
const year = computed(() => {
	return (titleInfo.value.startYear === titleInfo.value.endYear) ? titleInfo.value.startYear : `${titleInfo.value.startYear} - ${titleInfo.value.endYear}`;
});
const episodeInfo = computed(() => {
	return `S${titleInfo.value.season}, E${titleInfo.value.episode}`;
});
const runtime = computed(() => {
	return `${Math.floor(titleInfo.value.runtime / 60)}h ${titleInfo.value.runtime % 60}m`;
});
const genres = computed(() => {
	return titleInfo.value.genres.join(', ');
});
const isAdult = computed(() => {
	return titleInfo.value.isAdult === 1;
});
const directors = computed(() => {
	const limit = 5;
	const remaining = titleInfo.value.directors.length - limit;
	return `${titleInfo.value.directors.slice(0, limit).join(', ')}${remaining > 0 ? ` and ${remaining} more` : ''}`;
});
const writers = computed(() => {
	const limit = 8;
	const remaining = titleInfo.value.writers.length - limit;
	return `${titleInfo.value.writers.slice(0, limit).join(', ')}${remaining > 0 ? ` and ${remaining} more` : ''}`;
});
const principals = computed(() => {
	const limit = 10;
	const remaining = titleInfo.value.principals.length - limit;
	return `${titleInfo.value.principals.slice(0, limit).join(', ')}${remaining > 0 ? ` and ${remaining} more` : ''}`;
});
</script>

<style scoped>
.title-cnt {
	@apply flex flex-row items-center justify-start border rounded-md border-neutral-300 w-6/12 h-auto shadow-2xl;
}

.title-poster {
	@apply p-1 flex shrink-0 flex-col items-center aspect-auto w-auto h-max;
}

.title-info-cnt {
	@apply px-1 flex flex-col items-center justify-center w-full h-full;
}

.title-info-panel {
	@apply w-full h-auto flex flex-row items-center;
}

.title-info-panel-separator {
	@apply mt-6 w-full h-0;
}

.title-eng-name {
	@apply grow font-montserrat font-bold text-2xl text-neutral-950 tracking-normal outline-none select-none;
}

.title-rating {
	@apply flex flex-row items-center;
}

.title-rating-icon {
	@apply font-extralight text-center text-imdb-gold select-none;
}

.title-rating-points {
	@apply font-montserrat font-normal text-lg text-neutral-700 tracking-widest outline-none select-none;
}

.title-votes {
	@apply ml-1 font-montserrat font-light text-base text-neutral-500 tracking-wider outline-none select-none;
}

.title-name {
	@apply font-montserrat font-medium text-lg text-neutral-500 tracking-normal outline-none select-none;
}

.title-year {
	@apply font-montserrat font-normal text-base text-neutral-500 tracking-wider outline-none select-none;
}

.title-explicit-icon {
	@apply ml-1 font-normal text-center text-unive-red select-none;
}

.title-episode-info {
	@apply mr-1 font-montserrat font-normal text-base text-neutral-500 tracking-normal outline-none select-none;
}

.title-runtime {
	@apply font-montserrat font-normal text-base text-neutral-500 tracking-normal outline-none select-none;
}

.title-genres {
	@apply font-montserrat font-normal text-base text-neutral-500 tracking-normal outline-none select-none;
}

.title-directors-prefix {
	@apply font-montserrat font-normal text-base text-neutral-700 tracking-normal outline-none select-none;
}

.title-directors {
	@apply font-montserrat font-normal text-sm text-neutral-500 tracking-normal indent-2 outline-none select-none;
}

.title-writers-prefix {
	@apply font-montserrat font-normal text-base text-neutral-700 tracking-normal outline-none select-none;
}

.title-writers {
	@apply font-montserrat font-normal text-sm text-neutral-500 tracking-normal indent-2 outline-none select-none;
}

.title-principals-prefix {
	@apply font-montserrat font-normal text-base text-neutral-700 tracking-normal outline-none select-none;
}

.title-principals {
	@apply font-montserrat font-normal text-sm text-neutral-500 tracking-normal indent-2 outline-none select-none;
}
</style>
