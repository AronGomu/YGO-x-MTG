import { access, readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
const dist = path.resolve(process.env.OUT_DIR ?? 'dist');
const base = process.env.BASE_PATH ?? '/';
const html = [];
async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) await walk(file);
    else if (entry.name.endsWith('.html')) html.push(file);
  }
}
await walk(dist);
const missing = [];
for (const file of html) {
  const text = await readFile(file, 'utf8');
  for (const match of text.matchAll(/(?:href|src)="([^"#?]+)["#?]/g)) {
    const value = match[1];
    if (/^(?:https?:|mailto:|data:)/.test(value)) continue;
    let relative = value.startsWith('/')
      ? value.slice(base.length)
      : path.posix.join(
          path.relative(dist, path.dirname(file)).replaceAll('\\', '/'),
          value,
        );
    relative = relative.replace(/^\//, '');
    const target = path.join(dist, relative);
    try {
      await access(
        path.extname(target) ? target : path.join(target, 'index.html'),
      );
    } catch {
      missing.push(`${path.relative(dist, file)} → ${value}`);
    }
  }
}
if (missing.length)
  throw new Error(
    `Broken internal links:\n${[...new Set(missing)].join('\n')}`,
  );
process.stdout.write(`links: ${html.length} pages clean\n`);
