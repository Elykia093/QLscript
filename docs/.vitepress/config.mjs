import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'QLscript',
  description: '青龙面板脚本库文档',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' }],
    ['link', { rel: 'alternate icon', href: '/favicon.ico' }]
  ],
  cleanUrls: true,
  themeConfig: {
    logo: {
      src: '/logo.svg',
      width: 24,
      height: 24,
      alt: 'QLscript'
    },
    nav: [
      { text: '使用指南', link: '/', activeMatch: '^/$|^/guide/getting-started' },
      { text: '脚本索引', link: '/guide/scripts', activeMatch: '^/guide/scripts' },
      { text: '配置排错', link: '/guide/environment', activeMatch: '^/guide/environment' },
      { text: '开发规范', link: '/guide/development', activeMatch: '^/guide/development' }
    ],
    sidebar: [
      {
        text: '文档',
        items: [
          { text: '项目概览', link: '/' },
          { text: '快速开始', link: '/guide/getting-started' },
          { text: '脚本索引', link: '/guide/scripts' },
          { text: '环境变量与排错', link: '/guide/environment' },
          { text: '开发规范', link: '/guide/development' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Elykia093/QLscript' }
    ],
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    skipToContentLabel: '跳转到正文',
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索',
            buttonAriaLabel: '搜索文档'
          },
          modal: {
            displayDetails: '显示详细列表',
            resetButtonTitle: '清空搜索',
            backButtonTitle: '关闭搜索',
            noResultsText: '没有找到结果：',
            footer: {
              selectText: '选择',
              selectKeyAriaLabel: '回车',
              navigateText: '切换',
              navigateUpKeyAriaLabel: '上箭头',
              navigateDownKeyAriaLabel: '下箭头',
              closeText: '关闭',
              closeKeyAriaLabel: 'Esc'
            }
          }
        }
      }
    },
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最后更新',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    },
    footer: {
      message: 'QLscript 面向青龙面板的个人自动化脚本库。',
      copyright: 'Copyright © 2026-present Elykia'
    }
  },
  lastUpdated: true
})
