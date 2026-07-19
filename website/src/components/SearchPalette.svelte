<script lang="ts">
  import type { CatalogCard } from '../lib/catalog';
  import { cardNameScore, normalizeCardName } from '../lib/search';

  export let cards: Array<
    Pick<
      CatalogCard,
      'id' | 'name' | 'matchNames' | 'route' | 'sectionSlug' | 'manifestIndex'
    >
  >;
  export let base: string;

  let dialog: HTMLDialogElement;
  let input: HTMLInputElement;
  let trigger: HTMLButtonElement;
  let query = '';
  let active = 0;

  $: needle = normalizeCardName(query);
  $: results = needle
    ? cards
        .map((card) => ({
          card,
          score: Math.min(
            ...card.matchNames.map((name) => cardNameScore(name, needle)),
          ),
        }))
        .filter((item) => Number.isFinite(item.score))
        .sort(
          (a, b) =>
            a.score - b.score ||
            a.card.manifestIndex - b.card.manifestIndex ||
            a.card.id.localeCompare(b.card.id),
        )
        .slice(0, 12)
    : cards.slice(0, 12).map((card) => ({ card, score: 0 }));
  $: active = Math.min(active, Math.max(0, results.length - 1));
  $: keepActiveVisible(active, results);

  const href = (route: string) =>
    `${base.replace(/\/$/, '')}/${route.replace(/^\//, '')}`;
  function open() {
    query = '';
    active = 0;
    dialog.showModal();
    requestAnimationFrame(() => input.focus());
  }
  function close() {
    dialog.close();
    trigger.focus();
  }
  function onWindowKeydown(event: KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      if (dialog.open) close();
      else open();
    }
  }
  function navigate(route: string) {
    window.location.href = href(route);
  }
  function keepActiveVisible(index: number, items: typeof results) {
    if (!dialog?.open || !items[index]) return;
    requestAnimationFrame(() =>
      document
        .getElementById(`search-result-${items[index]?.card.id}`)
        ?.scrollIntoView({ block: 'nearest' }),
    );
  }
  function onInputKeydown(event: KeyboardEvent) {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      active = Math.min(active + 1, results.length - 1);
    }
    if (event.key === 'ArrowUp') {
      event.preventDefault();
      active = Math.max(active - 1, 0);
    }
    if (event.key === 'Enter' && results[active])
      navigate(results[active].card.route);
  }
</script>

<svelte:window on:keydown={onWindowKeydown} />
<button
  class="search-trigger"
  bind:this={trigger}
  on:click={open}
  aria-haspopup="dialog"
>
  <span aria-hidden="true">⌕</span><span>Find a card</span><kbd>⌘ K</kbd>
</button>

<dialog
  class="search-dialog"
  bind:this={dialog}
  aria-labelledby="search-title"
  on:click={(event) => event.target === dialog && close()}
  on:close={() => trigger?.focus()}
>
  <div class="search-panel">
    <header>
      <h2 id="search-title">Find a card</h2>
      <button on:click={close} aria-label="Close search">×</button>
    </header>
    <label for="global-card-search">Search current or former card name</label>
    <input
      id="global-card-search"
      bind:this={input}
      bind:value={query}
      on:keydown={onInputKeydown}
      role="combobox"
      aria-autocomplete="list"
      aria-expanded={results.length > 0}
      aria-controls={results.length ? 'search-results' : undefined}
      aria-activedescendant={results[active]
        ? `search-result-${results[active].card.id}`
        : undefined}
      autocomplete="off"
    />
    <p class="sr-only" aria-live="polite">
      {results.length}
      {results.length === 1 ? 'result' : 'results'}
    </p>
    {#if results.length}
      <ul id="search-results" role="listbox" aria-label="Card search results">
        {#each results as result, index (result.card.id)}
          <li
            id={`search-result-${result.card.id}`}
            role="option"
            tabindex="-1"
            aria-selected={active === index}
            on:mousemove={() => (active = index)}
            on:click={() => navigate(result.card.route)}
            on:keydown={(event) =>
              event.key === 'Enter' && navigate(result.card.route)}
          >
            <strong>{result.card.name}</strong><span
              >{result.card.sectionSlug.replaceAll('-', ' ')}</span
            >
          </li>
        {/each}
      </ul>
    {:else}
      <p id="search-results" class="search-empty">
        No card name matches “{query}”.
      </p>
    {/if}
  </div>
</dialog>
