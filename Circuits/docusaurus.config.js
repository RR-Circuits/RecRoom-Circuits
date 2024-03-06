// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {themes} = require('prism-react-renderer');

const lightCodeTheme = themes.github
const darkCodeTheme = themes.dracula

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Circuits Docs',
  tagline: 'For the community, by the community.',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://circuits.pages.dev',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'RR-Circuits', // Usually your GitHub org/user name.
  projectName: 'RecRoom-Circuits', // Usually your repo name.
  trailingSlash: false,
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  deploymentBranch: "main",

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'guides',
        path: 'guides',
        routeBasePath: 'guides',
        sidebarPath: require.resolve("./sidebars.js"),
      },
    ]
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      algolia: {
        // The application ID provided by Algolia
        appId: 'SAKJY3CCPM',

        // Public API key: it is safe to commit it
        apiKey: '9f4a711957da351271094828e8e0eea2',

        indexName: 'circuits',
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: true,
        respectPrefersColorScheme: false,
      },
      // Replace with your project's social card
      image: 'img/social-card.png',
      navbar: {
        title: 'Circuit Docs',
        logo: {
          alt: 'My Site Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            href: '/docs',
            label: 'Docs',
            position: 'left',
          },
          {
            href: '/guides',
            label: 'Guides',
            position: 'left',
          },
          {
            href: 'https://github.com/RR-Circuits/RecRoom-Circuits',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Main',
            items: [
              {
                label: 'Docs',
                to: '/docs',
              },
              {
                label: 'Guides',
                to: '/guides',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Rec Room Discord',
                href: 'https://discordapp.com/invite/recroom',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/RR-Circuits/RecRoom-Circuits',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Circuits Community | Built with Docusaurus`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
