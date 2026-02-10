<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<div class="min-h-screen flex flex-col">
	<header class="bg-surface-100-900 border-b border-surface-300-700">
		<nav class="container mx-auto px-4 py-3 flex items-center justify-between max-w-4xl">
			<a href="/" class="text-xl font-bold hover:text-primary-500 transition-colors">
				transscendsurvival.org
			</a>
			<div class="flex gap-4 text-sm">
				<a href="/blog" class="hover:text-primary-500 transition-colors">Blog</a>
				<a href="/cv" class="hover:text-primary-500 transition-colors">CV</a>
				<a href="/about" class="hover:text-primary-500 transition-colors">About</a>
				<a href="https://github.com/Jesssullivan" class="hover:text-primary-500 transition-colors" target="_blank" rel="noopener">GitHub</a>
			</div>
		</nav>
	</header>

	<main class="flex-1">
		{@render children()}
	</main>

	<footer class="bg-surface-100-900 border-t border-surface-300-700 py-6 text-center text-sm text-surface-500">
		<div class="container mx-auto px-4">
			<p>&copy; {new Date().getFullYear()} Jess Sullivan</p>
		</div>
	</footer>
</div>
