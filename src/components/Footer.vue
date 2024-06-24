<template>
	<div class="footer-cnt">
		<footer :class="{ 'dark': dark }">
			&copy; 2024 Michele Lotto & Daniel Jader Pellattiero
		</footer>
	</div>
</template>

<script setup lang="ts">
defineProps({
	dark: Boolean,
});
</script>

<style scoped>
footer {
	@apply font-montserrat font-light text-sm text-center text-neutral-500 uppercase tracking-widest duration-200 select-none;
}

footer.dark {
	@apply text-neutral-200;
}

.footer-cnt {
	@apply mb-1 w-screen h-auto flex flex-row justify-center items-center z-1;
}
</style>
