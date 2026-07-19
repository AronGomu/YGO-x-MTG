import { describe, expect, it } from 'vitest';
import { catalog, cardsById } from '../../src/lib/catalog';

describe('English publication graph', () => {
  it('registers ten sections in required navigation order', () => {
    expect(catalog.sections.map((section) => section.label)).toEqual([
      'Creatures',
      'Fusions',
      'Synchro',
      'Xyz',
      'Link',
      'Non-creature',
      'Burning Abyss',
      'Nekroz',
      'Shaddoll',
      'Spellbook',
    ]);
  });
  it('publishes globally unique card ids and names', () => {
    expect(new Set(catalog.cards.map((card) => card.id)).size).toBe(
      catalog.cards.length,
    );
    expect(new Set(catalog.cards.map((card) => card.name)).size).toBe(
      catalog.cards.length,
    );
  });
  it('resolves known ownership collisions to archetype projects', () => {
    expect(
      catalog.cards.find((card) => card.name === 'Herald of the Arc Light')
        ?.sectionSlug,
    ).toBe('nekroz');
    expect(
      catalog.cards.find((card) => card.name === 'Downerd Magician')
        ?.sectionSlug,
    ).toBe('burning-abyss');
    expect(
      catalog.cards.find((card) => card.name === 'Leviair the Sea Dragon')
        ?.sectionSlug,
    ).toBe('burning-abyss');
  });
  it('derives updates from snapshot selections instead of full baselines', () => {
    expect(catalog.updates).toHaveLength(151);
    expect(
      catalog.updates.some(
        (update) => update.cardId === 'herald-of-the-arc-light',
      ),
    ).toBe(false);
    expect(
      catalog.updates.find((update) => update.cardId === 'nekroz-trishula')
        ?.status,
    ).toBe('new');
  });
  it('pins first Nekroz snapshot to 19 baseline and 15 selected cards', () => {
    const snapshot = catalog.snapshots[0]!;
    expect(snapshot.id).toBe('001-2026-07-17');
    expect(snapshot.baseline).toHaveLength(19);
    expect(snapshot.selected).toHaveLength(15);
    expect(snapshot.baseline.every((item) => cardsById.has(item.id))).toBe(
      true,
    );
  });
  it('withholds incomplete source cards fail-closed', () => {
    expect(catalog.publicationDiagnostics).toHaveLength(26);
    expect(catalog.publicationDiagnostics).toContainEqual({
      sectionSlug: 'link',
      sourceFile: 'card cross sheep',
      reason: 'missing super_type; card withheld fail-closed',
    });
    expect(catalog.cards.some((card) => card.name === 'Cross-Sheep')).toBe(
      false,
    );
  });
});
