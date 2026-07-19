import catalogJson from '../generated/catalog.json';

export interface CatalogCard {
  id: string;
  sectionSlug: string;
  manifestIndex: number;
  name: string;
  matchNames: string[];
  formerFilenames: string[];
  routeAliases: string[];
  retired: boolean;
  castingCost: string;
  superType: string;
  subType: string;
  rarity: string;
  ruleText: string;
  ruleTextPlain: string;
  flavorText: string;
  flavorTextPlain: string;
  power: string | null;
  toughness: string | null;
  collectionNumber: string;
  created: string | null;
  modified: string;
  support: boolean;
  sourceHash: string;
  route: string;
  width: number;
  height: number;
  renderHash: string;
  render: string;
  galleryWebp: string;
  galleryAvif: string;
}

export type GalleryCard = Pick<
  CatalogCard,
  | 'id'
  | 'name'
  | 'route'
  | 'superType'
  | 'subType'
  | 'rarity'
  | 'ruleTextPlain'
  | 'modified'
  | 'support'
  | 'render'
  | 'galleryWebp'
  | 'galleryAvif'
  | 'width'
  | 'height'
>;

export interface CatalogSection {
  slug: string;
  label: string;
  kind: 'non-archetype' | 'archetype';
  accent: string;
  intro: string;
  diagnostics: Array<{ sourceFile: string; reason: string }>;
  iconicId: string;
  route: string;
  count: number;
  latestModified: string | null;
  image: string;
  cardIds: string[];
}

export interface Snapshot {
  schemaVersion: number;
  id: string;
  sectionSlug: string;
  parent: string | null;
  createdOn: string;
  head: boolean;
  baseline: Array<{ id: string; sourceHash: string; renderHash: string }>;
  selected: Array<CatalogCard & { status: 'new' | 'updated' }>;
  hash: string;
}

export interface Catalog {
  schemaVersion: number;
  generatedAt: string;
  sections: CatalogSection[];
  cards: CatalogCard[];
  explanations: Record<string, string>;
  updates: Array<{
    cardId: string;
    sectionSlug: string;
    status: 'new' | 'updated';
    modified: string;
  }>;
  snapshots: Snapshot[];
  publicationDiagnostics: Array<{
    sectionSlug: string;
    sourceFile: string;
    reason: string;
  }>;
}

export const catalog = catalogJson as Catalog;
export const cardsById = new Map(catalog.cards.map((card) => [card.id, card]));
export const sectionsBySlug = new Map(
  catalog.sections.map((section) => [section.slug, section]),
);

export function withBase(base: string, route: string): string {
  return `${base.replace(/\/$/, '')}/${route.replace(/^\//, '')}`;
}

export function toGalleryCard(card: CatalogCard): GalleryCard {
  const {
    id,
    name,
    route,
    superType,
    subType,
    rarity,
    ruleTextPlain,
    modified,
    support,
    render,
    galleryWebp,
    galleryAvif,
    width,
    height,
  } = card;
  return {
    id,
    name,
    route,
    superType,
    subType,
    rarity,
    ruleTextPlain,
    modified,
    support,
    render,
    galleryWebp,
    galleryAvif,
    width,
    height,
  };
}

export function formatDate(value: string): string {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);
  if (!match) throw new Error(`Invalid local date: ${value}`);
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  return new Intl.DateTimeFormat('en', { dateStyle: 'long' }).format(
    new Date(year, month - 1, day),
  );
}
