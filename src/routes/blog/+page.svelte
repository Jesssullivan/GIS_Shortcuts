<script lang="ts">
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Blog | transscendsurvival.org</title>
	<meta name="description" content="Blog posts by Jess Sullivan" />
</svelte:head>

<div class="container mx-auto px-4 py-12 max-w-3xl">
	<h1 class="text-3xl font-bold mb-8">Blog</h1>

	{#if data.posts.length === 0}
		<p class="text-surface-500">No posts yet. Content migration in progress.</p>
	{:else}
		<div class="space-y-6">
			{#each data.posts as post}
				<article class="card p-6 hover:ring-2 ring-primary-500 transition-all">
					<a href="/blog/{post.slug}" class="block">
						<time class="text-sm text-surface-500">{new Date(post.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</time>
						<h2 class="text-xl font-semibold mt-1">{post.title}</h2>
						{#if post.description}
							<p class="text-surface-600-400 mt-2">{post.description}</p>
						{/if}
						{#if post.tags.length > 0}
							<div class="flex gap-2 mt-3">
								{#each post.tags as tag}
									<span class="badge preset-outlined-primary-500 text-xs">{tag}</span>
								{/each}
							</div>
						{/if}
					</a>
				</article>
			{/each}
		</div>
	{/if}
</div>
