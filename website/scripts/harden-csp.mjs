import { createHash } from 'node:crypto';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(process.env.OUT_DIR ?? 'dist');
const files = [];
async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) await walk(file);
    else if (entry.name.endsWith('.html')) files.push(file);
  }
}
const hash = (value) =>
  `'sha256-${createHash('sha256').update(value).digest('base64')}'`;
await walk(root);
for (const file of files) {
  let html = await readFile(file, 'utf8');
  const scripts = [
    ...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi),
  ].map((match) => hash(match[1]));
  const styles = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map(
    (match) => hash(match[1]),
  );
  html = html
    .replace(
      "script-src 'self' 'unsafe-inline'",
      `script-src 'self' ${[...new Set(scripts)].join(' ')}`.trim(),
    )
    .replace(
      "style-src 'self' 'unsafe-inline'",
      `style-src 'self' ${[...new Set(styles)].join(' ')}`.trim(),
    );
  if (html.includes("'unsafe-inline'"))
    throw new Error(`${file}: CSP hardening incomplete`);
  await writeFile(file, html);
}
process.stdout.write(
  `csp: hashed inline content in ${files.length} HTML files\n`,
);
