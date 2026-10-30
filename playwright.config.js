import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4173';
const chromiumLaunchOptions = {
  args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'],
};

const webkitProjects = process.env.PLAYWRIGHT_WEBKIT === '1'
  ? [
      {
        name: 'webkit-desktop',
        use: {
          ...devices['Desktop Safari'],
          viewport: { width: 1600, height: 900 },
        },
      },
      {
        name: 'webkit-mobile',
        use: {
          ...devices['iPhone 13'],
        },
      },
    ]
  : [];

export default defineConfig({
  testDir: './tests/qa',
  outputDir: 'test-results',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  timeout: 120_000,
  expect: { timeout: 20_000 },
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'off',
    actionTimeout: 20_000,
    navigationTimeout: 90_000,
  },
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: 'npm run build && npm run serve',
        url: baseURL,
        reuseExistingServer: !process.env.CI,
        timeout: 180_000,
      },
  projects: [
    {
      name: 'chromium-desktop-1600',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1600, height: 900 },
        launchOptions: chromiumLaunchOptions,
      },
    },
    {
      name: 'chromium-desktop-1080p',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
        launchOptions: chromiumLaunchOptions,
      },
    },
    {
      name: 'firefox-desktop',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1600, height: 900 },
        firefoxUserPrefs: {
          'webgl.force-enabled': true,
          'webgl.disabled': false,
        },
      },
    },
    {
      name: 'chromium-mobile',
      use: {
        ...devices['Pixel 7'],
        launchOptions: chromiumLaunchOptions,
      },
    },
    ...webkitProjects,
  ],
});
