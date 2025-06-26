// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'tmux-ultimate',
  tagline: 'A tmux config generator written by claude code.',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://jeremyeder.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/tmux-ultimate/',

  // GitHub pages deployment config.
  organizationName: 'jeremyeder', // Usually your GitHub org/user name.
  projectName: 'tmux-ultimate', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
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
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          editUrl:
            'https://github.com/jeremyeder/tmux-ultimate/tree/main/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/jeremyeder/tmux-ultimate/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'tmux-ultimate',
        logo: {
          alt: 'tmux-ultimate Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Tutorial',
          },
          {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/jeremyeder/tmux-ultimate',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow - TMUX',
                href: 'https://stackoverflow.com/questions/tagged/tmux',
              },
              {
                label: 'TMUX Wiki',
                href: 'https://github.com/tmux/tmux/wiki',
              },
              {
                label: 'TMUX Manual',
                href: 'https://man.openbsd.org/tmux',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/jeremyeder/tmux-ultimate',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} tmux-ultimate. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
