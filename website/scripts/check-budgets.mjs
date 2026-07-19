import { readdir, stat } from 'node:fs/promises';
import path from 'node:path';

const dist = path.resolve(process.env.OUT_DIR ?? 'dist');
const files = [];
async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) await walk(file);
    else files.push({ file, size: (await stat(file)).size });
  }
}
await walk(dist);
const js = files.filter(({ file }) => file.endsWith('.js'));
const html = files.filter(({ file }) => file.endsWith('.html'));
const images = files.filter(({ file }) => /\.(?:png|webp|avif)$/.test(file));
const sum = (items) => items.reduce((total, item) => total + item.size, 0);
const issues = [];
if (sum(js) > 350 * 1024) issues.push(`JS total ${sum(js)} > 350 KiB`);
for (const item of html)
  if (item.size > 500 * 1024) issues.push(`${item.file}: HTML > 500 KiB`);
for (const item of images)
  if (item.size > 3 * 1024 * 1024) issues.push(`${item.file}: image > 3 MiB`);
if (sum(images) > 180 * 1024 * 1024)
  issues.push(`image total ${sum(images)} > 180 MiB`);
if (issues.length)
  throw new Error(`Artifact budgets exceeded:\n${issues.join('\n')}`);
process.stdout.write(
  `budgets: ${js.length} JS, ${html.length} HTML, ${images.length} images within limits\n`,
);
