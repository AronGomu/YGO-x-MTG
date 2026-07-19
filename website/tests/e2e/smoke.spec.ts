import { test, expect } from '@playwright/test';
const basePath = process.env.E2E_BASE_PATH?.replace(/\/$/, '') ?? '';
const urlFor = (path: string) => `${basePath}${path}`;
test('production preview serves generated routes and assets', async ({
  page,
}) => {
  const response = await page.goto(urlFor('/archetypes/nekroz/'));
  expect(response?.ok()).toBe(true);
  await expect(
    page.getByRole('heading', { name: 'Nekroz', exact: true }),
  ).toBeVisible();
  await expect(page.locator('.gallery-card')).toHaveCount(19);
  const image = page.locator('.gallery-card img').first();
  await expect(image).toHaveJSProperty('complete', true);
  await expect
    .poll(() =>
      image.evaluate((element) => (element as HTMLImageElement).naturalWidth),
    )
    .toBeGreaterThan(0);
});
