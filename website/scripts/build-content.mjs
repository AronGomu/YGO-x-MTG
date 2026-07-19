import { createHash } from 'node:crypto';
import {
  lstat,
  mkdir,
  readFile,
  readdir,
  realpath,
  rm,
  stat,
  writeFile,
} from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import { isSupportedRenderProvenance } from './render-provenance.mjs';

const WEBSITE = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
);
const ROOT = path.resolve(WEBSITE, '..');
const PROJECTS = path.join(ROOT, 'MSE_projects');
const GENERATED_PUBLIC = path.join(WEBSITE, 'public', 'generated');
const GENERATED_SOURCE = path.join(WEBSITE, 'src', 'generated');
const CHECK_ONLY = process.argv.includes('--check');

const LIMITS = Object.freeze({
  setBytes: 2 * 1024 * 1024,
  cardBytes: 512 * 1024,
  cards: 500,
  fieldChars: 100_000,
});
const projects = [
  [
    'creatures',
    'Creatures',
    'non-archetype',
    '03_YGO_Non_Archetype_Creatures.mse-set',
    'docs/01_cube_overview.md',
  ],
  [
    'fusions',
    'Fusion',
    'non-archetype',
    '05_YGO_Staples_Fusion.mse-set',
    'docs/01_cube_overview.md',
  ],
  [
    'synchro',
    'Synchro',
    'non-archetype',
    '06_YGO_Staples_Synchro.mse-set',
    'docs/01_cube_overview.md',
  ],
  [
    'xyz',
    'Xyz',
    'non-archetype',
    '07_YGO_Staples_Xyz.mse-set',
    'docs/01_cube_overview.md',
  ],
  [
    'link',
    'Link',
    'non-archetype',
    '08_YGO_Staples_Link.mse-set',
    'docs/01_cube_overview.md',
  ],
  [
    'non-creature',
    'Non-creature',
    'non-archetype',
    '09_YGO_Non_Archetype_Non_Creatures.mse-set',
    'docs/01_cube_overview.md',
  ],
  [
    'burning-abyss',
    'Burning Abyss',
    'archetype',
    '10_YGO_Burning_Abyss.mse-set',
    'docs/10_archetype_burning_abyss.md',
  ],
  [
    'nekroz',
    'Nekroz',
    'archetype',
    '12_YGO_Necroz.mse-set',
    'docs/12_archetype_necroz.md',
  ],
  [
    'shaddoll',
    'Shaddoll',
    'archetype',
    '11_YGO_Shaddoll.mse-set',
    'docs/11_archetype_shaddoll.md',
  ],
  [
    'spellbook',
    'Spellbook',
    'archetype',
    '13_YGO_Spellbook.mse-set',
    'docs/13_archetype_spellbook.md',
  ],
];
const accents = {
  creatures: 'relic',
  fusions: 'ember',
  synchro: 'ice',
  xyz: 'gold',
  link: 'aether',
  'non-creature': 'relic',
  'burning-abyss': 'ember',
  nekroz: 'ice',
  shaddoll: 'shadow',
  spellbook: 'aether',
};
const iconicNames = {
  'burning-abyss': 'Burning Abyss - Dante',
  shaddoll: 'El Shaddoll - Construct',
  nekroz: 'Nekroz - Trishula',
  spellbook: 'High Priestess of Prophecy',
};
const collisionWinners = new Map([
  ['Herald of the Arc Light', 'nekroz'],
  ['Downerd Magician', 'burning-abyss'],
  ['Leviair the Sea Dragon', 'burning-abyss'],
]);
const supportNames = new Set([
  'Herald of the Arc Light',
  'Manju of the Ten Thousand Hands',
  'Preparation of Rites',
  'Senju of the Thousand Hands',
]);

function fail(message) {
  throw new Error(`content: ${message}`);
}
function sha(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}
function normalizedFields(fields, excluded) {
  return `${[...fields.entries()]
    .filter(([key]) => !excluded.has(key))
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(
      ([key, value]) =>
        `${key}:${value
          .split('\n')
          .map((line) => line.trimEnd())
          .join('\n')
          .trim()}`,
    )
    .join('\n')}\n`;
}
function validLocalTimestamp(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$/.exec(value);
  if (!match) return false;
  const [year, month, day, hour, minute, second] = match.slice(1).map(Number);
  const parsed = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  return (
    parsed.getUTCFullYear() === year &&
    parsed.getUTCMonth() === month - 1 &&
    parsed.getUTCDate() === day &&
    parsed.getUTCHours() === hour &&
    parsed.getUTCMinutes() === minute &&
    parsed.getUTCSeconds() === second
  );
}
function stripMarkup(value) {
  return value
    .replace(/<[^>]*>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}
function renderName(name) {
  return `${name
    .replace(/:/g, ' -')
    .replace(/"/g, "'")
    .replace(/\//g, ' - ')
    .replace(/[<>|?*]/g, '')
    .replace(/[. ]+$/g, '')}.png`;
}
function routeForSection(section) {
  return section.kind === 'archetype'
    ? `/archetypes/${section.slug}/`
    : `/sections/non-archetype/${section.slug}/`;
}

async function safeFile(root, relative, limit) {
  if (
    !relative ||
    path.isAbsolute(relative) ||
    /^[A-Za-z]:/.test(relative) ||
    relative.startsWith('\\\\')
  )
    fail(`unsafe path ${relative}`);
  const realRoot = await realpath(root);
  const normalized = relative.replaceAll('\\', '/');
  const candidate = path.resolve(realRoot, normalized);
  if (candidate !== realRoot && !candidate.startsWith(`${realRoot}${path.sep}`))
    fail(`path escape ${relative}`);
  let cursor = realRoot;
  for (const segment of normalized.split('/').filter(Boolean)) {
    cursor = path.join(cursor, segment);
    const segmentInfo = await lstat(cursor);
    if (segmentInfo.isSymbolicLink()) fail(`linked path forbidden ${relative}`);
  }
  const resolved = await realpath(candidate);
  if (resolved !== realRoot && !resolved.startsWith(`${realRoot}${path.sep}`))
    fail(`real path escape ${relative}`);
  const info = await stat(resolved);
  if (!info.isFile()) fail(`not regular file ${relative}`);
  if (info.size > limit) fail(`${relative} exceeds ${limit} bytes`);
  return resolved;
}

function parseFields(text) {
  const fields = new Map();
  let key = null;
  let buffer = [];
  const flush = () => {
    if (key !== null) {
      if (fields.has(key)) fail(`duplicate field ${key}`);
      const value = buffer.join('\n').trimEnd();
      if (value.length > LIMITS.fieldChars)
        fail(`field ${key} exceeds ${LIMITS.fieldChars} chars`);
      fields.set(key, value);
    }
  };
  for (const line of text
    .replace(/^\uFEFF/, '')
    .replaceAll('\r\n', '\n')
    .replaceAll('\r', '\n')
    .split('\n')) {
    const match = /^\t([^:\n]+):(?:\s?(.*))?$/.exec(line);
    if (match) {
      flush();
      key = match[1].trim();
      buffer = [match[2] ?? ''];
    } else if (key !== null && line.startsWith('\t\t'))
      buffer.push(line.slice(2));
    else {
      flush();
      key = null;
      buffer = [];
    }
  }
  flush();
  return fields;
}

function validateMarkup(value, cardName) {
  const allowed = new Set([
    'atom-sep',
    'b',
    'bullet',
    'i',
    'i-auto',
    'i-flavor',
    'key',
    'kw-a',
    'li',
    'margin',
    'nospellcheck',
    'param-cost',
    'param-number',
    'soft',
    'sym-auto',
    'word-list-class-en',
    'word-list-enchantment',
    'word-list-race-en',
    'word-list-spell',
    'word-list-type-en',
  ]);
  const stack = [];
  for (const match of value.matchAll(/<(\/)?([a-z][a-z0-9-]*)(?::[^>]*)?>/gi)) {
    const tag = match[2].toLowerCase();
    if (!allowed.has(tag)) fail(`${cardName}: unknown MSE tag <${tag}>`);
    if (match[1]) {
      if (stack.pop() !== tag)
        fail(`${cardName}: unbalanced MSE tag </${tag}>`);
    } else stack.push(tag);
  }
  if (stack.length) fail(`${cardName}: unclosed MSE tag <${stack.at(-1)}>`);
}

function requireField(fields, name, source) {
  const value = fields.get(name)?.trim();
  if (!value) fail(`${source}: missing ${name}`);
  return value;
}

async function introFromDoc(relative, label) {
  const text = await readFile(path.join(ROOT, relative), 'utf8');
  const paragraphs = text
    .replace(/^---[\s\S]*?---/, '')
    .split(/\n\s*\n/)
    .map((part) =>
      part
        .replace(/^#+\s+.*$/gm, '')
        .replace(/[*_`#>]/g, '')
        .replace(/\[[^\]]+\]\([^)]*\)/g, '')
        .replace(/\s+/g, ' ')
        .trim(),
    )
    .filter((part) => part.length > 60 && !part.startsWith('|'));
  return (
    paragraphs[0]?.slice(0, 360) ??
    `${label} cards adapted for play under Magic rules.`
  );
}

async function parseProject(definition) {
  const [sectionSlug, label, kind, folder, doc] = definition;
  const projectRoot = path.join(PROJECTS, folder);
  const setPath = await safeFile(projectRoot, 'set', LIMITS.setBytes);
  const setText = await readFile(setPath, 'utf8');
  const setVisual = setText
    .replace(/^\uFEFF/, '')
    .replaceAll('\r\n', '\n')
    .replaceAll('\r', '\n')
    .replace(/\n$/, '')
    .split('\n')
    .filter(
      (line) =>
        !line.trimStart().startsWith('description:') &&
        !line.trimStart().startsWith('artist:') &&
        !line.trimStart().startsWith('copyright:'),
    )
    .map((line) => line.trimEnd())
    .join('\n');
  if (
    !/^\s*set_language:\s*EN\s*$/m.test(setText) ||
    !/^\s*card_language:\s*English\s*$/m.test(setText)
  )
    fail(`${folder}: English publication headers missing`);
  const includes = [...setText.matchAll(/^include_file:\s*(.+?)\s*$/gm)].map(
    (match) => match[1],
  );
  if (
    !includes.length ||
    includes.length > LIMITS.cards ||
    new Set(includes).size !== includes.length
  )
    fail(`${folder}: invalid manifest`);
  const cards = [];
  const diagnostics = [];
  for (const [manifestIndex, sourceFile] of includes.entries()) {
    const sourcePath = await safeFile(
      projectRoot,
      sourceFile,
      LIMITS.cardBytes,
    );
    const raw = await readFile(sourcePath, 'utf8');
    const fields = parseFields(raw);
    const name = requireField(fields, 'name', sourceFile);
    const imageRelative = fields.get('image')?.trim();
    const imagePath = imageRelative
      ? await safeFile(projectRoot, imageRelative, 64 * 1024 * 1024)
      : null;
    const artworkHash = imagePath ? sha(await readFile(imagePath)) : '';
    const cardVisual = normalizedFields(
      fields,
      new Set(['notes', 'time_created', 'time_modified']),
    );
    const visualSourceHash = sha(
      Buffer.from(
        `manifest-index:${manifestIndex}\n${setVisual}\nart:${artworkHash}\n${cardVisual}`,
      ),
    );
    const ruleText = fields.get('rule_text')?.trim() ?? '';
    const flavorText = fields.get('flavor_text')?.trim() ?? '';
    const rawSuperType = fields.get('super_type')?.trim();
    if (!rawSuperType) {
      diagnostics.push({
        sourceFile,
        reason: 'missing super_type; card withheld fail-closed',
      });
      continue;
    }
    const superType = stripMarkup(rawSuperType);
    const subType = stripMarkup(fields.get('sub_type') ?? '');
    validateMarkup(
      `${fields.get('super_type') ?? ''}${fields.get('sub_type') ?? ''}${ruleText}${flavorText}`,
      name,
    );
    const codeValues = [
      'card_code_text',
      'card_code_text_2',
      'card_code_text_3',
    ]
      .map((key) => fields.get(key)?.trim())
      .filter(Boolean);
    if (new Set(codeValues).size > 1)
      fail(`${sourceFile}: repeated card_code_text values disagree`);
    const creature = /Creature/i.test(superType);
    const power = fields.get('power')?.trim() || null;
    const toughness = fields.get('toughness')?.trim() || null;
    if (creature && Boolean(power) !== Boolean(toughness))
      fail(`${sourceFile}: creature power/toughness must be a pair`);
    const modified = requireField(fields, 'time_modified', sourceFile);
    if (!validLocalTimestamp(modified))
      fail(`${sourceFile}: invalid time_modified`);
    cards.push({
      sectionSlug,
      sourceFile,
      sourcePath,
      projectRoot,
      manifestIndex,
      name,
      matchNames: [name],
      castingCost: fields.get('casting_cost')?.trim() ?? '',
      imageRelative: imageRelative || null,
      superType,
      subType,
      rarity: fields.get('rarity')?.trim() ?? 'unknown',
      ruleText,
      ruleTextPlain: stripMarkup(ruleText),
      flavorText,
      flavorTextPlain: stripMarkup(flavorText),
      power,
      toughness,
      collectionNumber: codeValues[0] ?? '',
      created: fields.get('time_created')?.trim() ?? null,
      modified,
      support: sectionSlug === 'nekroz' && supportNames.has(name),
      sourceHash: sha(
        Buffer.from(raw.replace(/^\uFEFF/, '').replaceAll('\r\n', '\n')),
      ),
      visualSourceHash,
      artworkHash,
    });
  }
  return {
    slug: sectionSlug,
    label,
    kind,
    folder,
    doc,
    accent: accents[sectionSlug],
    intro: await introFromDoc(doc, label),
    cards,
    diagnostics,
  };
}

async function writeDerivative(input, output, format, width) {
  await mkdir(path.dirname(output), { recursive: true });
  const pipeline = sharp(input, {
    limitInputPixels: 80_000_000,
    failOn: 'warning',
  })
    .rotate()
    .resize({ width, withoutEnlargement: true });
  if (format === 'png')
    await pipeline
      .png({ compressionLevel: 9, adaptiveFiltering: true })
      .toFile(output);
  else if (format === 'webp')
    await pipeline.webp({ quality: 86, effort: 5 }).toFile(output);
  else await pipeline.avif({ quality: 60, effort: 4 }).toFile(output);
}

async function loadExplanations(cards) {
  const directory = path.join(WEBSITE, 'content', 'explanations');
  const knownIds = new Set(cards.map((card) => card.id));
  const explanations = {};
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.name === '.gitkeep') continue;
    const source = path.join(directory, entry.name);
    const info = await lstat(source);
    if (info.isSymbolicLink() || !entry.isFile() || !entry.name.endsWith('.md'))
      fail(`Unsafe explanation entry: ${entry.name}`);
    if (info.size > 256 * 1024) fail(`Explanation too large: ${entry.name}`);
    const value = await readFile(source, 'utf8');
    if (!value.startsWith('---\n'))
      fail(`Missing explanation frontmatter: ${entry.name}`);
    const end = value.indexOf('\n---\n', 4);
    if (end < 0) fail(`Unclosed explanation frontmatter: ${entry.name}`);
    const frontmatter = value.slice(4, end).trim().split('\n');
    if (frontmatter.length !== 1 || !frontmatter[0].startsWith('cardId: '))
      fail(`Explanation frontmatter only permits cardId: ${entry.name}`);
    const cardId = frontmatter[0].slice('cardId: '.length).trim();
    if (!knownIds.has(cardId) || entry.name !== `${cardId}.md`)
      fail(`Explanation identity mismatch: ${entry.name}`);
    const markdown = value.slice(end + 5).trim();
    if (/<\/?[A-Za-z][^>]*>|\{[^\n]*\}/.test(markdown))
      fail(`Raw HTML or MDX forbidden in explanation: ${entry.name}`);
    if (/!\[[^\]]*\]\([^)]*\)/.test(markdown))
      fail(`Markdown images forbidden in explanation: ${entry.name}`);
    for (const match of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
      const url = match[1].trim();
      if (!/^(?:https:\/\/|mailto:|#|\/)/i.test(url))
        fail(`Unsafe explanation URL in ${entry.name}: ${url}`);
    }
    explanations[cardId] = markdown;
  }
  return explanations;
}

async function main() {
  const identityRegistry = JSON.parse(
    await readFile(path.join(WEBSITE, 'content', 'identities.json'), 'utf8'),
  );
  if (
    identityRegistry.schemaVersion !== 1 ||
    !Array.isArray(identityRegistry.cards)
  )
    fail('Invalid identity registry schema');
  const identityByName = new Map();
  const identityById = new Map();
  const reservedIdentityIds = new Set();
  const routeAliases = new Set();
  for (const identity of identityRegistry.cards) {
    if (
      !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(identity.stableId ?? '') ||
      !identity.currentName ||
      !Array.isArray(identity.formerNames ?? []) ||
      !Array.isArray(identity.formerFilenames ?? []) ||
      !Array.isArray(identity.routeAliases ?? []) ||
      reservedIdentityIds.has(identity.stableId) ||
      identityByName.has(identity.currentName)
    )
      fail(`Invalid or duplicate identity: ${identity.stableId ?? 'unknown'}`);
    reservedIdentityIds.add(identity.stableId);
    identityByName.set(identity.currentName, identity);
    identityById.set(identity.stableId, identity);
    for (const alias of identity.routeAliases ?? []) {
      if (
        !/^\/[a-z0-9][a-z0-9/-]*\/$/.test(alias) ||
        alias.includes('//') ||
        alias.includes('..') ||
        routeAliases.has(alias)
      )
        fail(`Invalid or duplicate route alias: ${alias}`);
      routeAliases.add(alias);
    }
  }
  const sections = [];
  for (const definition of projects)
    sections.push(await parseProject(definition));
  const definedNames = new Map(
    sections
      .filter((section) => section.kind === 'archetype')
      .flatMap((section) =>
        section.cards.map((card) => [card.name, section.slug]),
      ),
  );
  const activeCards = [];
  const ids = new Set();
  const names = new Set();
  for (const section of sections) {
    section.cards = section.cards.filter((card) => {
      if (section.kind === 'non-archetype' && definedNames.has(card.name)) {
        if (collisionWinners.get(card.name) !== definedNames.get(card.name))
          fail(`unregistered ownership collision ${card.name}`);
        return false;
      }
      return true;
    });
    for (const card of section.cards) {
      const identity = identityByName.get(card.name);
      if (!identity)
        fail(
          `Published card missing stable identity registry entry: ${card.name}`,
        );
      if (identity.withdrawn) {
        section.diagnostics.push({
          sourceFile: card.sourceFile,
          reason: 'asset withdrawn by identity registry',
        });
        continue;
      }
      const id = identity.stableId;
      if (ids.has(id) || names.has(card.name))
        fail(`duplicate or reserved active public identity ${card.name}`);
      ids.add(id);
      names.add(card.name);
      card.id = id;
      card.matchNames = [
        ...new Set([card.name, ...(identity.formerNames ?? [])]),
      ];
      card.formerFilenames = identity.formerFilenames ?? [];
      card.routeAliases = identity.routeAliases ?? [];
      card.retired = Boolean(identity.retired);
      card.route = `/cards/${id}/`;
      activeCards.push(card);
    }
    section.cards = section.cards.filter((card) => card.id);
  }
  if (!activeCards.length) fail('No publishable cards remain after validation');

  if (!CHECK_ONLY) {
    await rm(GENERATED_PUBLIC, { recursive: true, force: true });
    await mkdir(GENERATED_PUBLIC, { recursive: true });
  }
  await rm(GENERATED_SOURCE, { recursive: true, force: true });
  await mkdir(GENERATED_SOURCE, { recursive: true });

  for (const section of sections) {
    const fallback = section.cards[0];
    const iconic =
      section.cards.find((card) => card.name === iconicNames[section.slug]) ??
      fallback;
    if (!iconic) fail(`${section.label}: no iconic card`);
    section.iconicId = iconic.id;
    section.route = routeForSection(section);
    section.count = section.cards.length;
    section.latestModified =
      [...section.cards].sort(
        (a, b) =>
          b.modified.localeCompare(a.modified) ||
          a.manifestIndex - b.manifestIndex ||
          a.id.localeCompare(b.id),
      )[0]?.modified ?? null;
    if (!CHECK_ONLY && iconic.imageRelative) {
      const input = await safeFile(
        iconic.projectRoot,
        iconic.imageRelative,
        64 * 1024 * 1024,
      );
      await writeDerivative(
        input,
        path.join(GENERATED_PUBLIC, 'section-art', `${section.slug}.webp`),
        'webp',
        1200,
      );
      section.image = `/generated/section-art/${section.slug}.webp`;
    } else section.image = `/generated/section-art/${section.slug}.webp`;
  }

  const provenanceByProject = new Map();
  for (const card of activeCards) {
    let provenance = provenanceByProject.get(card.projectRoot);
    if (!provenance) {
      const provenancePath = await safeFile(
        card.projectRoot,
        'render-provenance.json',
        2 * 1024 * 1024,
      );
      provenance = JSON.parse(await readFile(provenancePath, 'utf8'));
      if (
        !isSupportedRenderProvenance(provenance) ||
        provenance.project !== path.basename(card.projectRoot) ||
        !Array.isArray(provenance.cards)
      )
        fail(`${card.sectionSlug}: invalid render provenance`);
      provenanceByProject.set(card.projectRoot, provenance);
    }
    const attestation = provenance.cards.find(
      (item) => item.id === card.sourceFile,
    );
    if (!attestation) fail(`${card.name}: render provenance entry missing`);
    const canonical = await safeFile(
      path.join(card.projectRoot, 'render'),
      renderName(card.name),
      64 * 1024 * 1024,
    );
    const metadata = await sharp(canonical, {
      limitInputPixels: 80_000_000,
    }).metadata();
    if (
      !metadata.width ||
      !metadata.height ||
      metadata.width > 12_000 ||
      metadata.height > 12_000 ||
      metadata.width * metadata.height > 80_000_000
    )
      fail(`${card.name}: invalid render dimensions`);
    card.width = metadata.width;
    card.height = metadata.height;
    card.renderHash = sha(await readFile(canonical));
    if (
      attestation.sourceHash !== card.visualSourceHash ||
      attestation.artworkHash !== (card.artworkHash || null) ||
      attestation.renderHash !== card.renderHash
    )
      fail(
        `${card.name}: stale canonical provenance (source=${attestation.sourceHash === card.visualSourceHash}, artwork=${attestation.artworkHash === (card.artworkHash || null)}, render=${attestation.renderHash === card.renderHash})`,
      );
    card.render = `/generated/card-renders/${card.id}.png`;
    card.galleryWebp = `/generated/card-renders/${card.id}.webp`;
    card.galleryAvif = `/generated/card-renders/${card.id}.avif`;
    if (!CHECK_ONLY) {
      await writeDerivative(
        canonical,
        path.join(GENERATED_PUBLIC, 'card-renders', `${card.id}.png`),
        'png',
        metadata.width,
      );
      await Promise.all([
        writeDerivative(
          canonical,
          path.join(GENERATED_PUBLIC, 'card-renders', `${card.id}.webp`),
          'webp',
          560,
        ),
        writeDerivative(
          canonical,
          path.join(GENERATED_PUBLIC, 'card-renders', `${card.id}.avif`),
          'avif',
          560,
        ),
      ]);
    }
  }

  const publicCards = activeCards.map(
    ({
      sourceFile,
      sourcePath,
      projectRoot,
      imageRelative,
      visualSourceHash,
      artworkHash,
      ...card
    }) => card,
  );
  const publicSections = sections.map(({ cards, folder, doc, ...section }) => ({
    ...section,
    cardIds: cards.map((card) => card.id),
  }));
  const snapshotPath = path.join(
    WEBSITE,
    'content',
    'snapshots',
    'nekroz',
    '001-2026-07-17.json',
  );
  const snapshot = JSON.parse(await readFile(snapshotPath, 'utf8'));
  const { hash: storedSnapshotHash, ...snapshotPayload } = snapshot;
  if (
    snapshot.schemaVersion !== 1 ||
    snapshot.id !== '001-2026-07-17' ||
    snapshot.sectionSlug !== 'nekroz' ||
    snapshot.parent !== null ||
    snapshot.baseline?.length !== 19 ||
    snapshot.selected?.length !== 15 ||
    new Set(snapshot.baseline.map((item) => item.id)).size !== 19 ||
    snapshot.selected.some(
      (card) => !snapshot.baseline.some((item) => item.id === card.id),
    )
  )
    fail('Invalid immutable Nekroz snapshot structure');
  const snapshotHash = sha(Buffer.from(JSON.stringify(snapshotPayload)));
  if (storedSnapshotHash !== snapshotHash)
    fail(`Immutable Nekroz snapshot hash mismatch: ${storedSnapshotHash}`);
  const publicSnapshot = {
    ...snapshot,
    baseline: snapshot.baseline.filter(
      (item) => !identityById.get(item.id)?.withdrawn,
    ),
    selected: snapshot.selected.filter(
      (card) => !identityById.get(card.id)?.withdrawn,
    ),
  };
  const selectedUpdates = new Map(
    publicSnapshot.selected.map((card) => [card.id, card.status]),
  );
  const sortedUpdates = publicCards
    .filter(
      (card) =>
        card.sectionSlug !== publicSnapshot.sectionSlug ||
        selectedUpdates.has(card.id),
    )
    .sort(
      (a, b) =>
        b.modified.localeCompare(a.modified) ||
        a.manifestIndex - b.manifestIndex ||
        a.id.localeCompare(b.id),
    )
    .map((card) => ({
      cardId: card.id,
      sectionSlug: card.sectionSlug,
      status: selectedUpdates.get(card.id) ?? 'new',
      modified: card.modified,
    }));
  const snapshotRoot = path.join(
    WEBSITE,
    'content',
    'snapshots',
    'nekroz',
    snapshot.id,
  );
  for (const card of publicSnapshot.selected) {
    const source = await safeFile(
      snapshotRoot,
      path.join('renders', `${card.id}.png`),
      64 * 1024 * 1024,
    );
    if (sha(await readFile(source)) !== card.renderHash)
      fail(`Immutable snapshot render mismatch: ${card.id}`);
    if (!CHECK_ONLY) {
      await writeDerivative(
        source,
        path.join(
          GENERATED_PUBLIC,
          'snapshots',
          snapshot.sectionSlug,
          snapshot.id,
          `${card.id}.png`,
        ),
        'png',
        card.width,
      );
      await Promise.all([
        writeDerivative(
          source,
          path.join(
            GENERATED_PUBLIC,
            'snapshots',
            snapshot.sectionSlug,
            snapshot.id,
            `${card.id}.webp`,
          ),
          'webp',
          560,
        ),
        writeDerivative(
          source,
          path.join(
            GENERATED_PUBLIC,
            'snapshots',
            snapshot.sectionSlug,
            snapshot.id,
            `${card.id}.avif`,
          ),
          'avif',
          560,
        ),
      ]);
    }
  }
  const rightsInventory = publicSnapshot.selected.map((card) => ({
    key: `snapshot:${publicSnapshot.sectionSlug}:${publicSnapshot.id}:${card.id}:render`,
    sha256: card.renderHash,
  }));
  for (const card of activeCards) {
    rightsInventory.push({ key: `${card.id}:render`, sha256: card.renderHash });
    if (card.imageRelative) {
      const artwork = await safeFile(
        card.projectRoot,
        card.imageRelative,
        64 * 1024 * 1024,
      );
      rightsInventory.push({
        key: `${card.id}:artwork`,
        sha256: sha(await readFile(artwork)),
      });
    }
  }
  rightsInventory.sort((a, b) => a.key.localeCompare(b.key));
  await writeFile(
    path.join(GENERATED_SOURCE, 'rights-inventory.json'),
    `${JSON.stringify({ schemaVersion: 1, assets: rightsInventory }, null, 2)}\n`,
    'utf8',
  );

  const explanations = await loadExplanations(publicCards);
  const output = {
    schemaVersion: 1,
    generatedAt: new Date().toISOString(),
    sections: publicSections,
    cards: publicCards,
    explanations,
    updates: sortedUpdates,
    snapshots: publicSnapshot.selected.length ? [publicSnapshot] : [],
    publicationDiagnostics: publicSections.flatMap((section) =>
      section.diagnostics.map((diagnostic) => ({
        sectionSlug: section.slug,
        ...diagnostic,
      })),
    ),
  };
  await writeFile(
    path.join(GENERATED_SOURCE, 'catalog.json'),
    `${JSON.stringify(output, null, 2)}\n`,
    'utf8',
  );
  await writeFile(
    path.join(GENERATED_SOURCE, 'catalog.sha256'),
    `${sha(Buffer.from(JSON.stringify(output)))}\n`,
    'utf8',
  );
  process.stdout.write(
    `content: ${publicSections.length} sections, ${publicCards.length} unique cards, snapshot ${snapshot.id}\n`,
  );
}

await main();
