<script lang="ts">
	import { goto } from '$app/navigation';
</script>

<svelte:head>
	<title>transscendsurvival.org</title>
	<meta name="description" content="Jess Sullivan - Blog and portfolio" />
</svelte:head>

<div class="container mx-auto px-4 py-12 max-w-3xl">
	<section class="mb-12">
		<h1 class="text-4xl font-bold mb-4">Jess Sullivan</h1>
		<p class="text-lg text-surface-600-400 mb-6">
			Hardware hacker, FOSS contributor, birder. Building things with Chapel, Futhark, SvelteKit, and whatever else is interesting.
		</p>
		<p class="text-surface-500 mb-8">
			After spending a year completely offline (late 2023 &ndash; end 2024), I'm back and rebuilding my digital presence.
		</p>
		<div class="flex gap-3">
			<a href="/blog" class="btn preset-filled-primary-500">Read the Blog</a>
			<a href="/about" class="btn preset-outlined-primary-500">About Me</a>
		</div>
	</section>

	<section class="mb-12">
		<h2 class="text-2xl font-semibold mb-4">Recent Posts</h2>
		<p class="text-surface-500">Blog posts coming soon &mdash; migrating content from the old WordPress site.</p>
	</section>

	<section>
		<h2 class="text-2xl font-semibold mb-4">FOSS Highlights</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<a href="https://github.com/Jesssullivan/quickchpl" class="card p-4 hover:ring-2 ring-primary-500 transition-all" target="_blank" rel="noopener">
				<h3 class="font-semibold">quickchpl</h3>
				<p class="text-sm text-surface-500">Property-Based Testing for Chapel</p>
			</a>
			<a href="https://github.com/Jesssullivan/GloriousFlywheel" class="card p-4 hover:ring-2 ring-primary-500 transition-all" target="_blank" rel="noopener">
				<h3 class="font-semibold">GloriousFlywheel</h3>
				<p class="text-sm text-surface-500">Recursive IaC flywheel for GitLab</p>
			</a>
			<a href="https://github.com/Jesssullivan/XoxdWM" class="card p-4 hover:ring-2 ring-primary-500 transition-all" target="_blank" rel="noopener">
				<h3 class="font-semibold">XoxdWM</h3>
				<p class="text-sm text-surface-500">Eye-gesture VR & BCI XWayland Emacs WM</p>
			</a>
			<a href="https://github.com/Jesssullivan/MerlinAI-Interpreters" class="card p-4 hover:ring-2 ring-primary-500 transition-all" target="_blank" rel="noopener">
				<h3 class="font-semibold">MerlinAI-Interpreters</h3>
				<p class="text-sm text-surface-500">Birdsong ML identification</p>
			</a>
		</div>
	</section>
</div>
