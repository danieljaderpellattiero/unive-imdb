<template>
	<div class="footer-cnt">
		<footer>
			© 2024 Michele Lotto & Daniel Jader Pellattiero
		</footer>
	</div>
</template>

<script setup lang="ts">
</script>

<style scoped>
footer {
	@apply font-montserrat font-light text-sm text-center text-neutral-500 uppercase tracking-widest select-none;
}

.footer-cnt {
	@apply absolute bottom-0 mb-1 w-screen flex flex-row justify-center items-center;
}
</style>
