import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const basePath = process.env.E2E_BASE_PATH?.replace(/\/$/, '') ?? '';
const urlFor = (path: string) => `${basePath}${path}`;

test('home renders English archive and passes automated a11y scan', async ({
  page,
}) => {
  await page.goto(urlFor('/'));
  await expect(page).toHaveTitle(/YGO × MTG/);
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(
    page.getByRole('heading', { name: /Yu-Gi-Oh! feel/i }),
  ).toBeVisible();
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test('mobile drawer traps entry and restores focus', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(urlFor('/'));
  const trigger = page.getByRole('button', { name: 'Catalog' });
  await trigger.click();
  const dialog = page.getByRole('dialog', { name: 'Catalog' });
  await expect(dialog).toBeVisible();
  await expect(
    page.getByRole('button', { name: 'Close catalog' }),
  ).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect
    .poll(() =>
      page.evaluate(() => document.activeElement?.closest('dialog')?.open),
    )
    .toBe(true);
  await page.getByRole('button', { name: 'Close catalog' }).click();
  await expect(trigger).toBeFocused();
});

test('primary routes pass automated a11y scans', async ({
  page,
  browserName,
}) => {
  test.skip(browserName !== 'chromium', 'full route coverage runs once');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  for (const route of [
    '/archetypes/nekroz/',
    '/cards/nekroz-trishula/',
    '/updates/',
    '/rules/',
    '/philosophy/',
    '/archetypes/nekroz/snapshots/001-2026-07-17/',
  ]) {
    await page.goto(urlFor(route));
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations, route).toEqual([]);
  }
});

test('forced colors preserve readable controls', async ({
  page,
  browserName,
}) => {
  test.skip(browserName !== 'chromium', 'forced-colors coverage runs once');
  await page.emulateMedia({ forcedColors: 'active', reducedMotion: 'reduce' });
  await page.goto(urlFor('/archetypes/nekroz/'));
  const firstCard = page.locator('.gallery-card').first();
  await expect(firstCard).toBeVisible();
  await firstCard.focus();
  expect(
    await firstCard.evaluate(
      (element) => getComputedStyle(element).outlineStyle,
    ),
  ).not.toBe('none');
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(
    await page.evaluate(() => document.documentElement.clientWidth),
  );
});

test('global search keyboard shortcut opens card-name combobox', async ({
  page,
}) => {
  await page.goto(urlFor('/'));
  await page.getByRole('button', { name: /Find a card/ }).click();
  await page.getByRole('button', { name: 'Close search' }).click();
  await page.keyboard.press(
    process.platform === 'darwin' ? 'Meta+K' : 'Control+K',
  );
  const search = page.getByRole('combobox', {
    name: /Search current or former card name/i,
  });
  await expect(search).toBeFocused();
  await search.fill('Trishula');
  await expect(page.getByRole('option').first()).toContainText('Trishula');
});

test('Nekroz gallery removes filters and preserves card proportions', async ({
  page,
}) => {
  await page.goto(urlFor('/archetypes/nekroz/'));
  await expect(page.getByText('Refine this section')).toHaveCount(0);
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'nekroz');
  const heroFrame = page.locator('.catalog-hero-art');
  const heroImage = heroFrame.locator('img');
  const frameBeforeHover = await heroFrame.boundingBox();
  const transformBeforeHover = await heroImage.evaluate(
    (element) => getComputedStyle(element).transform,
  );
  await heroFrame.hover();
  await expect
    .poll(() =>
      heroImage.evaluate((element) => getComputedStyle(element).transform),
    )
    .not.toBe(transformBeforeHover);
  expect(await heroFrame.boundingBox()).toEqual(frameBeforeHover);
  const card = page.locator('.gallery-card').first();
  const image = card.locator('img');
  const size = await image.evaluate((element: HTMLImageElement) => ({
    displayedWidth: element.getBoundingClientRect().width,
    displayedHeight: element.getBoundingClientRect().height,
    naturalWidth: element.naturalWidth,
    naturalHeight: element.naturalHeight,
  }));
  expect(size.displayedWidth).toBeLessThanOrEqual(400);
  expect(size.displayedWidth / size.displayedHeight).toBeCloseTo(
    size.naturalWidth / size.naturalHeight,
    2,
  );
  await card.hover();
  await expect(page.locator('.card-hover-preview')).toHaveClass(/is-visible/);
});

test('home exposes rules, philosophy, and single-row new-card carousel', async ({
  page,
}) => {
  await page.goto(urlFor('/'));
  await expect(page.getByRole('link', { name: 'Rules' })).toHaveAttribute(
    'href',
    /rules\/$/,
  );
  await expect(page.getByRole('link', { name: 'Philosophy' })).toHaveAttribute(
    'href',
    /philosophy\/$/,
  );
  const carousel = page.getByRole('list', { name: 'New cards' });
  await expect(carousel).toHaveCSS('display', 'flex');
  await expect(carousel).toHaveCSS('overflow-x', 'auto');
});

test('rules and philosophy expose sticky chapter summary', async ({ page }) => {
  await page.goto(urlFor('/rules/'));
  const rulesToc = page.getByRole('navigation', { name: 'Chapter summary' });
  await expect(rulesToc).toBeVisible();
  await expect(rulesToc.getByRole('link', { name: 'Traps' })).toHaveAttribute(
    'href',
    '#traps',
  );
  await rulesToc.getByRole('link', { name: 'Traps' }).click();
  await expect(page.locator('#traps')).toBeInViewport();

  await page.goto(urlFor('/philosophy/'));
  const philosophyToc = page.getByRole('navigation', {
    name: 'Chapter summary',
  });
  await expect(philosophyToc).toBeVisible();
  await expect(
    philosophyToc.getByRole('link', { name: 'What the cube avoids' }),
  ).toHaveAttribute('href', '#avoids');
  await philosophyToc
    .getByRole('link', { name: 'What the cube avoids' })
    .click();
  await expect(page.locator('#avoids')).toBeInViewport();
});

test('card detail opens full-size dialog and restores focus', async ({
  page,
}) => {
  await page.goto(urlFor('/cards/nekroz-trishula/'));
  const trigger = page.getByRole('button', { name: 'View full-size card' });
  await trigger.click();
  await expect(
    page.getByRole('dialog', { name: /Full-size Nekroz - Trishula/ }),
  ).toBeVisible();
  await page.getByRole('button', { name: 'Close full-size card' }).click();
  await expect(trigger).toBeFocused();
});
