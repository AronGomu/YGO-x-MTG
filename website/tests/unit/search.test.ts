import { describe, expect, it } from 'vitest';
import { cardNameScore, normalizeCardName } from '../../src/lib/search';

describe('card-name search', () => {
  it('normalizes punctuation, apostrophes, accents, and spacing', () => {
    expect(normalizeCardName('D.D. Crow’s  Café')).toBe('d d crows cafe');
  });
  it('ranks exact before prefix before contains before fuzzy', () => {
    expect(
      cardNameScore('Nekroz - Trishula', 'Nekroz - Trishula'),
    ).toBeLessThan(cardNameScore('Nekroz - Trishula', 'Nek'));
    expect(cardNameScore('Nekroz - Trishula', 'Nek')).toBeLessThan(
      cardNameScore('The Nekroz - Trishula', 'Nek'),
    );
    const fuzzy = cardNameScore('Nekroz - Trishula', 'nktrsh');
    expect(Number.isFinite(fuzzy)).toBe(true);
    expect(fuzzy).toBeGreaterThan(2);
  });
  it('rejects non-subsequence fuzzy matches', () => {
    expect(cardNameScore('Nekroz - Trishula', 'zzzz')).toBe(
      Number.POSITIVE_INFINITY,
    );
  });
});
