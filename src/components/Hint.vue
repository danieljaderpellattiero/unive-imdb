<template>
	<RouterLink :to="{ name: 'title', params: { id: _id } }" class="hint-cnt">
		<div class="hint-graphic">
			<img :src="previewImage" alt="preview_img" />
		</div>
		<div class="hint-info-cnt">
			<div class="hint-info-panel">
				<p class="hint-title">{{ title }}</p>
				<p class="hint-year">{{ year }}</p>
				<div class="hint-rating">
					<span class="material-symbols-sharp hint-rating-icon">star</span>
					<p class="hint-rating-points">{{ Number.isInteger(rating) ? `${rating}.0` : rating }}/10</p>
				</div>
			</div>
			<div class="hint-info-panel">
				<p class="hint-genre">{{ titleType }}</p>
				<p v-if="season && episode" class="hint-episode-info">S{{ season }}, E{{ episode }}</p>
			</div>
		</div>
	</RouterLink>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps<{
	_id: string;
	title: string;
	titleType: string;
	year: number;
	rating: number;
	episode: number | null;
	season: number | null;
}>();
const previewImage = ref<string>('');

onMounted(() => {
	axios.get(`http://img.omdbapi.com/?apikey=${import.meta.env.VITE_API_OMDB}&i=${props._id}`, { responseType: 'blob' })
		.then(response => {
			previewImage.value = URL.createObjectURL(response.data);
		})
		.catch(error => {
			console.error(error);
		});
})
</script>

<style scoped>
img {
	@apply select-none;
}

.hint-cnt {
	@apply w-full h-auto flex flex-row items-center py-2 border-b border-neutral-500 cursor-pointer;
}

.hint-cnt:hover .hint-title {
	@apply text-unive-red;
}

/* ! */
.hint-graphic {
	@apply aspect-auto h-full flex items-center justify-center size-16;
}

.hint-info-cnt {
	@apply w-full h-auto flex flex-col items-center;
}

.hint-info-panel {
	@apply w-full h-auto px-2 flex flex-row items-center;
}

.hint-title {
	@apply font-montserrat font-medium text-base text-start text-neutral-700 tracking-normal outline-none select-none duration-200;
}

.hint-year {
	@apply ml-2 grow shrink font-montserrat font-normal text-sm text-start text-neutral-500 tracking-normal outline-none select-none;
}

.hint-rating {
	@apply flex flex-row items-center;
}

.hint-rating-icon {
	@apply font-extralight text-center text-neutral-700 select-none;
}

.hint-rating-points {
	@apply font-montserrat font-normal text-base text-end text-neutral-700 tracking-widest outline-none select-none;
}

.hint-genre {
	@apply font-montserrat font-normal text-sm text-start text-neutral-500 tracking-normal outline-none select-none;
}

.hint-episode-info {
	@apply ml-2 font-montserrat font-normal text-sm text-start text-neutral-500 tracking-normal outline-none select-none;
}
</style>
