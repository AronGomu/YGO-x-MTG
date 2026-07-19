import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
const trustedScripts = JSON.parse(
  await readFile(new URL('../trusted-install-scripts.json', import.meta.url)),
);
const lock = JSON.parse(
  await readFile(new URL('../package-lock.json', import.meta.url)),
);
if (
  trustedScripts.schemaVersion !== 1 ||
  !trustedScripts.reviewedBy ||
  !trustedScripts.packages
)
  throw new Error('Invalid trusted install-script review record');
const scripted = new Set(
  Object.entries(lock.packages)
    .filter(([, metadata]) => metadata.hasInstallScript)
    .map(([location]) => location.split('node_modules/').at(-1)),
);
const unreviewedScripts = [...scripted].filter(
  (name) => !trustedScripts.packages[name],
);
if (unreviewedScripts.length)
  throw new Error(
    `Unreviewed dependency install scripts: ${unreviewedScripts.join(', ')}`,
  );

const allowed = new Set([
  'MIT',
  'ISC',
  'BSD-2-Clause',
  'BSD-3-Clause',
  'Apache-2.0',
  'Apache-2.0 AND LGPL-3.0-or-later',
  'LGPL-3.0-or-later',
  'BlueOak-1.0.0',
  'MPL-2.0',
  '0BSD',
  'CC0-1.0',
]);
const npmCli = process.env.npm_execpath;
const command = npmCli ? process.execPath : 'npm';
const args = npmCli
  ? [npmCli, 'query', ':not(.dev)', '--json']
  : ['query', ':not(.dev)', '--json'];
const packages = JSON.parse(
  execFileSync(command, args, {
    encoding: 'utf8',
  }),
);
const failures = [];
for (const item of packages) {
  if (item.name === 'ygo-mtg-showcase') continue;
  const values = Array.isArray(item.license) ? item.license : [item.license];
  if (
    !values.some((license) =>
      allowed.has(typeof license === 'string' ? license : license?.type),
    )
  )
    failures.push(
      `${item.name}@${item.version}: ${JSON.stringify(item.license ?? 'UNKNOWN')}`,
    );
}
if (failures.length)
  throw new Error(
    `Forbidden or unknown production licenses:\n${failures.join('\n')}`,
  );
process.stdout.write(
  `licenses: ${packages.length - 1} production packages allowed; ${scripted.size} install-script package names reviewed\n`,
);
