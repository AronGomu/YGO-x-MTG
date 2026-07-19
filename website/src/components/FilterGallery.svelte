<script lang="ts">
  import { onMount } from 'svelte';
  import type { GalleryCard } from '../lib/catalog';
  import { parseGalleryQuery, serializeGalleryQuery } from '../lib/query';

  export let cards: GalleryCard[];
  export let base: string;
  export let accent: string;

  let nameQuery = '';
  let textQuery = '';
  let type = '';
  let rarity = '';
  let on = '';
  let since = '';
  let until = '';
  let waveLatest = false;
  let liveMessage = '';
  let presentation: HTMLDialogElement;
  let presentationTrigger: HTMLButtonElement;
  let current = 0;
  let clean = false;
  let fullscreenDenied = false;
  let initialized = false;
  let fullscreenActive = false;
  let controlsVisible = true;
  let presentationOpen = false;
  let hideTimer: ReturnType<typeof setTimeout> | undefined;

  const href = (route: string) =>
    `${base.replace(/\/$/, '')}/${route.replace(/^\//, '')}`;
  const asset = (route: string) => href(route);
  const date = (value: string) => value.slice(0, 10);
  const types = [...new Set(cards.map((card) => card.superType))].sort();
  const rarities = [...new Set(cards.map((card) => card.rarity))].sort();
  const latestDay =
    [...cards.map((card) => date(card.modified))].sort().at(-1) ?? '';

  $: filtered = cards.filter((card) => {
    const cardDate = date(card.modified);
    return (
      (!nameQuery ||
        card.name.toLowerCase().includes(nameQuery.toLowerCase())) &&
      (!textQuery ||
        card.ruleTextPlain.toLowerCase().includes(textQuery.toLowerCase())) &&
      (!type || card.superType === type) &&
      (!rarity || card.rarity === rarity) &&
      (!on || cardDate === on) &&
      (!since || cardDate >= since) &&
      (!until || cardDate <= until) &&
      (!waveLatest || cardDate === latestDay)
    );
  });
  $: visibleRanks = new Map(filtered.map((card, index) => [card.id, index]));
  $: groups = Object.entries(
    Object.groupBy(filtered, (card) => date(card.modified)),
  ).sort(([a], [b]) => b.localeCompare(a));
  $: liveMessage = `${filtered.length} ${filtered.length === 1 ? 'card' : 'cards'} shown`;
  $: syncQuery(
    initialized,
    nameQuery,
    textQuery,
    type,
    rarity,
    on,
    since,
    until,
    waveLatest,
  );
  $: currentCard = filtered[current];

  function syncQuery(..._dependencies: unknown[]) {
    if (!initialized || typeof window === 'undefined') return;
    const value = serializeGalleryQuery({
      q: nameQuery,
      text: textQuery,
      type,
      rarity,
      on,
      since,
      until,
      ...(waveLatest ? { wave: 'latest' as const } : {}),
    });
    history.replaceState(
      null,
      '',
      value ? `${location.pathname}?${value}` : location.pathname,
    );
  }

  onMount(() => {
    const params = parseGalleryQuery(location.search);
    nameQuery = params.q ?? '';
    textQuery = params.text ?? '';
    type = types.includes(params.type ?? '') ? (params.type ?? '') : '';
    rarity = rarities.includes(params.rarity ?? '')
      ? (params.rarity ?? '')
      : '';
    on = params.on ?? '';
    since = params.since ?? '';
    until = params.until ?? '';
    waveLatest = params.wave === 'latest';
    initialized = true;
    const fullscreenChanged = () => {
      fullscreenActive = document.fullscreenElement === presentation;
    };
    document.addEventListener('fullscreenchange', fullscreenChanged);
    return () =>
      document.removeEventListener('fullscreenchange', fullscreenChanged);
  });

  function clear() {
    nameQuery = '';
    textQuery = '';
    type = '';
    rarity = '';
    on = '';
    since = '';
    until = '';
    waveLatest = false;
    document.getElementById('filter-name')?.focus();
  }
  function openPresentation() {
    if (!filtered.length) return;
    current = 0;
    clean = false;
    controlsVisible = true;
    presentationOpen = true;
    presentation.showModal();
    requestAnimationFrame(() =>
      presentation.querySelector<HTMLElement>('button')?.focus(),
    );
  }
  function closePresentation() {
    presentation.close();
  }
  function presentationClosed() {
    presentationOpen = false;
    presentationTrigger.focus();
  }
  function scheduleControls() {
    if (hideTimer) clearTimeout(hideTimer);
    controlsVisible = true;
    if (clean)
      hideTimer = setTimeout(() => {
        const controls = presentation.querySelector('.presentation-controls');
        if (!controls?.contains(document.activeElement))
          controlsVisible = false;
      }, 1800);
  }
  function toggleClean() {
    clean = !clean;
    if (clean) scheduleControls();
    else controlsVisible = true;
  }
  function move(delta: number) {
    if (!filtered.length) return;
    current = (current + delta + filtered.length) % filtered.length;
  }
  async function toggleFullscreen() {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await presentation.requestFullscreen();
      fullscreenDenied = false;
    } catch {
      fullscreenDenied = true;
    }
  }
  function presentationKeydown(event: KeyboardEvent) {
    if (!presentation.open) return;
    scheduleControls();
    const target = event.target;
    if (
      target instanceof HTMLElement &&
      target.closest('button, input, select, textarea, a')
    )
      return;
    if (event.key.toLowerCase() === 'c') {
      event.preventDefault();
      toggleClean();
      return;
    }
    if (event.key === 'ArrowRight' || event.key === ' ') {
      event.preventDefault();
      move(1);
    }
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      move(-1);
    }
    if (event.key === 'Home') {
      event.preventDefault();
      current = 0;
    }
    if (event.key === 'End') {
      event.preventDefault();
      current = filtered.length - 1;
    }
  }
</script>

<svelte:window on:keydown={presentationKeydown} />
<section class="filters" aria-labelledby="filter-title">
  <div class="filter-heading">
    <h2 id="filter-title">Refine this section</h2>
    <button type="button" on:click={clear}>Clear filters</button>
  </div>
  <div class="filter-grid">
    <label
      >Name <input
        id="filter-name"
        bind:value={nameQuery}
        type="search"
        autocomplete="off"
      /></label
    >
    <label
      >Parsed card text <input
        bind:value={textQuery}
        type="search"
        autocomplete="off"
      /></label
    >
    <label
      >Type <select bind:value={type}
        ><option value="">All types</option>{#each types as item (item)}<option
            value={item}>{item}</option
          >{/each}</select
      ></label
    >
    <label
      >Rarity <select bind:value={rarity}
        ><option value="">All rarities</option
        >{#each rarities as item (item)}<option value={item}>{item}</option
          >{/each}</select
      ></label
    >
  </div>
  <details>
    <summary>Date filters</summary>
    <div class="date-filters">
      <label>On <input bind:value={on} type="date" /></label><label
        >Since <input bind:value={since} type="date" /></label
      ><label>Until <input bind:value={until} type="date" /></label><label
        class="check"
        ><input bind:checked={waveLatest} type="checkbox" /> Latest wave only</label
      >
    </div>
  </details>
  <p class="result-count" aria-live="polite">{liveMessage}</p>
  <button
    class="presentation-trigger"
    bind:this={presentationTrigger}
    on:click={openPresentation}
    disabled={!filtered.length}>Present filtered cards <kbd>↵</kbd></button
  >
</section>

{#each groups as [day, dayCards] (day)}
  <section class="day-group" aria-labelledby={`day-${day}`}>
    <h2 id={`day-${day}`}>
      {new Intl.DateTimeFormat('en', { dateStyle: 'long' }).format(
        new Date(`${day}T12:00:00`),
      )}
    </h2>
    <div class="card-grid">
      {#each dayCards as card (card.id)}
        <a
          class="gallery-card"
          href={href(card.route)}
          style={`--card-order:${visibleRanks.get(card.id) ?? 0}`}
        >
          <picture
            ><source
              srcset={asset(card.galleryAvif)}
              type="image/avif"
            /><source srcset={asset(card.galleryWebp)} type="image/webp" /><img
              src={asset(card.render)}
              alt=""
              width={card.width}
              height={card.height}
              loading={(visibleRanks.get(card.id) ?? 4) < 4 ? 'eager' : 'lazy'}
              decoding="async"
            /></picture
          >
          <span class="card-caption"
            ><strong>{card.name}</strong><span>{card.superType}</span
            >{#if card.support}<small>Support card</small>{/if}</span
          >
        </a>
      {/each}
    </div>
  </section>
{:else}
  <section class="empty-state">
    <h2>No cards match</h2>
    <p>Change or clear filters to return to this section.</p>
    <button type="button" on:click={clear}>Clear filters</button>
  </section>
{/each}

<dialog
  class:clean
  class:controls-hidden={clean && !controlsVisible}
  class="presentation-dialog"
  bind:this={presentation}
  aria-labelledby="presentation-title"
  on:close={presentationClosed}
  on:mousemove={scheduleControls}
>
  {#if currentCard && presentationOpen}
    <div class="presentation-stage">
      <img
        src={asset(currentCard.render)}
        alt={`${currentCard.name} card render`}
        width={currentCard.width}
        height={currentCard.height}
      />
      <aside>
        <p class="presentation-position" aria-live="polite">
          {currentCard.name}. Card {current + 1} of {filtered.length}
        </p>
        <h2 id="presentation-title">{currentCard.name}</h2>
        <p>
          {currentCard.superType}{currentCard.subType
            ? ` — ${currentCard.subType}`
            : ''}
        </p>
        <p>
          {new Intl.DateTimeFormat('en', { dateStyle: 'long' }).format(
            new Date(`${date(currentCard.modified)}T12:00:00`),
          )}
        </p>
      </aside>
      <div
        class="presentation-controls"
        role="group"
        aria-label="Presentation controls"
      >
        <button on:click={() => move(-1)} aria-label="Previous card">←</button
        ><button on:click={() => move(1)} aria-label="Next card">→</button
        ><button on:click={toggleClean} aria-pressed={clean}>Clean mode</button
        ><button on:click={toggleFullscreen} aria-pressed={fullscreenActive}
          >{fullscreenActive ? 'Exit fullscreen' : 'Fullscreen'}</button
        ><button on:click={closePresentation}>Close</button>
      </div>
      {#if fullscreenDenied}<p class="fullscreen-error" role="status">
          Fullscreen unavailable. Presentation remains open in this window.
        </p>{/if}
    </div>
  {/if}
</dialog>
