import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const base = process.env.BASE_SHA;
if (!base || /^0+$/.test(base)) {
  process.stdout.write(
    'snapshots: no merge-base supplied; current schema checked by content builder\n',
  );
  process.exit(0);
}
const root = path.resolve('..');
const prefix = 'website/content/snapshots/';
const git = (...args) =>
  execFileSync('git', args, { cwd: root, encoding: 'utf8' }).trim();
let priorFiles = [];
try {
  priorFiles = git('ls-tree', '-r', '--name-only', base, '--', prefix)
    .split('\n')
    .filter(Boolean);
} catch {
  throw new Error(`Unable to inspect snapshot merge-base ${base}`);
}
const changed = [];
for (const file of priorFiles) {
  const prior = execFileSync('git', ['show', `${base}:${file}`], {
    cwd: root,
  });
  let current;
  try {
    current = await readFile(path.join(root, file));
  } catch {
    changed.push(`${file}: deleted`);
    continue;
  }
  if (!current.equals(prior)) changed.push(`${file}: modified`);
}
if (changed.length)
  throw new Error(`Published snapshots are immutable:\n${changed.join('\n')}`);

const identityPath = 'website/content/identities.json';
let identityExisted = true;
try {
  execFileSync('git', ['cat-file', '-e', `${base}:${identityPath}`], {
    cwd: root,
    stdio: 'ignore',
  });
} catch {
  identityExisted = false;
}
const priorIdentity = identityExisted
  ? JSON.parse(
      execFileSync('git', ['show', `${base}:${identityPath}`], {
        cwd: root,
        encoding: 'utf8',
      }),
    )
  : { cards: [] };
const currentIdentity = JSON.parse(
  await readFile(path.join(root, identityPath), 'utf8'),
);
const currentById = new Map(
  currentIdentity.cards.map((identity) => [identity.stableId, identity]),
);
const identityErrors = [];
for (const prior of priorIdentity.cards ?? []) {
  const current = currentById.get(prior.stableId);
  if (!current)
    identityErrors.push(`${prior.stableId}: deleted identity/tombstone`);
  else if (
    prior.currentName !== current.currentName &&
    !(current.formerNames ?? []).includes(prior.currentName)
  )
    identityErrors.push(
      `${prior.stableId}: renamed without formerNames history`,
    );
  else if (prior.withdrawn && !current.withdrawn)
    identityErrors.push(`${prior.stableId}: withdrawn identity reactivated`);
}
if (identityErrors.length)
  throw new Error(
    `Published identities require migration-safe history:\n${identityErrors.join('\n')}`,
  );
process.stdout.write(
  `snapshots: ${priorFiles.length} published files unchanged from ${base}\n`,
);
