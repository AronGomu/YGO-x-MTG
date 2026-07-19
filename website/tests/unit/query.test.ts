import { describe, expect, it } from 'vitest';
import { parseGalleryQuery, serializeGalleryQuery } from '../../src/lib/query';

describe('gallery query contract', () => {
  it('round trips in canonical order', () => {
    const parsed = parseGalleryQuery(
      new URLSearchParams(
        'until=2026-07-19&q=Trishula&wave=latest&since=2026-07-01',
      ),
    );
    expect(serializeGalleryQuery(parsed)).toBe(
      'q=Trishula&since=2026-07-01&until=2026-07-19&wave=latest',
    );
  });
  it('drops invalid dates and unknown wave values', () => {
    expect(
      parseGalleryQuery(
        new URLSearchParams('on=yesterday&since=2026-02-30&wave=old'),
      ),
    ).toEqual({});
  });
});
