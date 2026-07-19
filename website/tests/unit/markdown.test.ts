import { describe, expect, it } from 'vitest';
import { renderSafeMarkdown } from '../../src/lib/markdown';

describe('authored Markdown renderer', () => {
  it('escapes HTML while rendering supported prose', () => {
    const html = renderSafeMarkdown(
      '## Intent\n\n**Safe** <script>alert(1)</script>',
    );
    expect(html).toContain('<h2>Intent</h2>');
    expect(html).toContain('<strong>Safe</strong> &lt;script&gt;');
    expect(html).not.toContain('<script>');
  });
  it('prefixes internal links for repository-base deployments', () => {
    expect(
      renderSafeMarkdown('[Nekroz](/archetypes/nekroz/)', '/YGO-x-MTG/'),
    ).toContain('href="/YGO-x-MTG/archetypes/nekroz/"');
  });
  it('rejects unsafe URL schemes', () => {
    expect(() => renderSafeMarkdown('[bad](javascript:alert(1))')).toThrow(
      'Unsafe Markdown URL',
    );
  });
});
