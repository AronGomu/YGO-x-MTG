import { describe, expect, it } from 'vitest';
import { renderMseMarkup } from '../../src/lib/mse-markup';

describe('safe MSE markup', () => {
  it('renders semantic tags and strips editor-only wrappers', () => {
    expect(
      renderMseMarkup(
        '<b>On Enter</b> — <i-auto><kw-a><nospellcheck><key>Flash</key></nospellcheck></kw-a></i-auto>',
      ),
    ).toBe('<strong>On Enter</strong> — <em>Flash</em>');
  });
  it('rejects unknown payload tags before rendering', () => {
    expect(() =>
      renderMseMarkup('<b>safe</b> <script>alert(1)</script>'),
    ).toThrow('Unknown MSE tag: script');
  });
  it('rejects unbalanced allowlisted tags', () => {
    expect(() => renderMseMarkup('<b>broken</i>')).toThrow('Unbalanced');
  });
});
