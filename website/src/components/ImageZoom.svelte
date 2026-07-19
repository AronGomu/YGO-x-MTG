<script lang="ts">
  export let src: string;
  export let alt: string;
  export let width: number;
  export let height: number;
  let dialog: HTMLDialogElement;
  let trigger: HTMLButtonElement;
  let visible = false;
  function open() {
    visible = true;
    dialog.showModal();
    requestAnimationFrame(() =>
      dialog.querySelector<HTMLElement>('button')?.focus(),
    );
  }
  function close() {
    dialog.close();
  }
  function closed() {
    visible = false;
    trigger.focus();
  }
</script>

<button
  class="zoom-trigger"
  bind:this={trigger}
  on:click={open}
  aria-haspopup="dialog">View full-size card</button
>
<dialog
  class="zoom-dialog"
  bind:this={dialog}
  aria-label={`Full-size ${alt}`}
  on:click={(event) => event.target === dialog && close()}
  on:close={closed}
>
  <button on:click={close} aria-label="Close full-size card">Close</button>
  {#if visible}<img {src} {alt} {width} {height} />{/if}
</dialog>

<style>
  .zoom-trigger {
    margin: 1rem auto 0;
    display: block;
  }
  .zoom-dialog {
    width: min(96vw, 52rem);
    height: min(96dvh, 72rem);
    border: 0;
    background: var(--blackfoil);
    padding: 1rem;
  }
  .zoom-dialog button {
    position: sticky;
    top: 0;
    float: right;
  }
  .zoom-dialog img {
    max-height: calc(96dvh - 2rem);
    margin: auto;
    object-fit: contain;
  }
</style>
