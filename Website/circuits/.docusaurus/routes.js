import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', 'd02'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', 'a72'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '7ed'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '055'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', 'dcd'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '757'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '5c8'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', '1b8'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '2ed'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', 'e5d'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '3b6'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', '43d'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '479'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', 'b99'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '336'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '022'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', 'a0a'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', '177'),
    exact: true
  },
  {
    path: '/docs/tags',
    component: ComponentCreator('/docs/tags', '8f9'),
    exact: true
  },
  {
    path: '/docs/tags/tags',
    component: ComponentCreator('/docs/tags/tags', '1e1'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', 'cd8'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'e1a'),
    routes: [
      {
        path: '/docs/category/chips',
        component: ComponentCreator('/docs/category/chips', 'b2a'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/category/components',
        component: ComponentCreator('/docs/category/components', '577'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/category/documentation',
        component: ComponentCreator('/docs/category/documentation', '058'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/category/guides',
        component: ComponentCreator('/docs/category/guides', '1cd'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/documentation/chips/TEMPLATE',
        component: ComponentCreator('/docs/documentation/chips/TEMPLATE', 'a41'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/documentation/components/translate-your-site',
        component: ComponentCreator('/docs/documentation/components/translate-your-site', 'ce3'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/guides/military',
        component: ComponentCreator('/docs/guides/military', '58c'),
        exact: true,
        sidebar: "tutorialSidebar"
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '3d0'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
