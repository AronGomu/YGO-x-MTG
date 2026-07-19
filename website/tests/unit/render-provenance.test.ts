import { describe, expect, it } from 'vitest';
import { isSupportedRenderProvenance } from '../../scripts/render-provenance.mjs';

describe('render provenance compatibility', () => {
  it('accepts legacy schema v1 during migration', () => {
    expect(isSupportedRenderProvenance({ schemaVersion: 1 })).toBe(true);
  });

  it('accepts schema v2 with the transparent-corner transform', () => {
    expect(
      isSupportedRenderProvenance({
        schemaVersion: 2,
        renderTransform: {
          id: 'transparent-white-corners',
          version: 1,
        },
      }),
    ).toBe(true);
  });

  it.each([
    undefined,
    { id: 'other-transform', version: 1 },
    { id: 'transparent-white-corners', version: 2 },
  ])('rejects schema v2 transform %j', (renderTransform) => {
    expect(
      isSupportedRenderProvenance({ schemaVersion: 2, renderTransform }),
    ).toBe(false);
  });
});
