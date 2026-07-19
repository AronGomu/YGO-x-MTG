export interface GalleryQuery {
  q?: string;
  text?: string;
  type?: string;
  rarity?: string;
  on?: string;
  since?: string;
  until?: string;
  wave?: 'latest';
}
const date = /^(\d{4})-(\d{2})-(\d{2})$/;
function validDate(value: string): boolean {
  const match = date.exec(value);
  if (!match) return false;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const parsed = new Date(Date.UTC(year, month - 1, day));
  return (
    parsed.getUTCFullYear() === year &&
    parsed.getUTCMonth() === month - 1 &&
    parsed.getUTCDate() === day
  );
}
export function parseGalleryQuery(
  input: URLSearchParams | string,
): GalleryQuery {
  const params = typeof input === 'string' ? new URLSearchParams(input) : input;
  const result: GalleryQuery = {};
  for (const key of ['q', 'text', 'type', 'rarity'] as const) {
    const value = params.get(key)?.trim();
    if (value) result[key] = value;
  }
  for (const key of ['on', 'since', 'until'] as const) {
    const value = params.get(key);
    if (value && validDate(value)) result[key] = value;
  }
  if (params.get('wave') === 'latest') result.wave = 'latest';
  return result;
}
export function serializeGalleryQuery(query: GalleryQuery): string {
  const params = new URLSearchParams();
  for (const key of [
    'q',
    'text',
    'type',
    'rarity',
    'on',
    'since',
    'until',
    'wave',
  ] as const)
    if (query[key]) params.set(key, query[key]);
  return params.toString();
}
