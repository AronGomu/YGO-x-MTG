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
  const trigger = page.getByRole('button', { name: /Present filtered cards/ });
  await expect(trigger).toBeVisible();
  await trigger.focus();
  expect(
    await trigger.evaluate((element) => getComputedStyle(element).outlineStyle),
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

test('Nekroz filters persist and presentation restores focus', async ({
  page,
}) => {
  await page.goto(urlFor('/archetypes/nekroz/?q=Trishula'));
  await expect(page.getByLabel('Name', { exact: true })).toHaveValue(
    'Trishula',
  );
  await expect(page).toHaveURL(/q=Trishula/);
  await page.getByLabel('Name', { exact: true }).fill('Brionac');
  await expect(page).toHaveURL(/q=Brionac/);
  await page.reload();
  await expect(page.getByLabel('Name', { exact: true })).toHaveValue('Brionac');
  await expect(page.getByText('1 card shown')).toBeVisible();
  const trigger = page.getByRole('button', { name: /Present filtered cards/ });
  await trigger.click();
  await expect(
    page.getByRole('dialog', { name: /Nekroz - Brionac/ }),
  ).toBeVisible();
  await page.getByRole('button', { name: 'Close' }).click();
  await expect(trigger).toBeFocused();
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
