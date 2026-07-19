export function normalizeCardName(value: string): string {
  return value
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[’']/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}
export function cardNameScore(name: string, query: string): number {
  const value = normalizeCardName(name);
  const needle = normalizeCardName(query);
  if (!needle) return 0;
  if (value === needle) return 0;
  if (value.startsWith(needle)) return 1;
  if (value.includes(needle)) return 2;
  let cursor = 0;
  for (const character of needle) {
    cursor = value.indexOf(character, cursor);
    if (cursor < 0) return Number.POSITIVE_INFINITY;
    cursor += 1;
  }
  return 3 + (value.length - needle.length) / 100;
}
