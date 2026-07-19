function escapeHtml(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function inline(value: string, base: string): string {
  let html = escapeHtml(value);
  html = html.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    (_match, label: string, rawUrl: string) => {
      const url = rawUrl.trim();
      if (!/^(?:https:\/\/|mailto:|#|\/)/i.test(url))
        throw new Error(`Unsafe Markdown URL: ${url}`);
      const href = url.startsWith('/')
        ? `${base.replace(/\/$/, '')}${url}`
        : url;
      const external = url.startsWith('https://')
        ? ' rel="noopener noreferrer"'
        : '';
      return `<a href="${escapeHtml(href)}"${external}>${label}</a>`;
    },
  );
  html = html
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/_([^_]+)_/g, '<em>$1</em>');
  return html;
}

export function renderSafeMarkdown(value: string, base = '/'): string {
  return value
    .split(/\n\s*\n/)
    .filter(Boolean)
    .map((block) => {
      const lines = block.split('\n');
      if (lines.every((line) => /^-\s+/.test(line)))
        return `<ul>${lines.map((line) => `<li>${inline(line.replace(/^-\s+/, ''), base)}</li>`).join('')}</ul>`;
      const heading = /^(#{2,3})\s+(.+)$/.exec(block);
      if (heading) {
        const level = heading[1]!.length;
        return `<h${level}>${inline(heading[2]!, base)}</h${level}>`;
      }
      return `<p>${lines.map((line) => inline(line, base)).join('<br>')}</p>`;
    })
    .join('');
}
