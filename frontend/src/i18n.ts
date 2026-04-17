import { computed, ref, watch } from "vue";

export type Locale = "zh-CN" | "en";

const LOCALE_KEY = "finflow_locale";
const defaultLocale: Locale = "zh-CN";

const messages = {
  "zh-CN": {
    app: {
      localeLabel: "语言",
      switchToChinese: "切换到中文",
      switchToEnglish: "Switch to English",
    },
    nav: {
      product: "FinFlow",
      title: "投资信号驾驶舱",
      feed: "动态",
      creators: "创作者",
      settings: "设置",
      crawlLogs: "抓取日志",
      signOut: "退出登录",
    },
    feed: {
      eyebrow: "内容动态",
      title: "在同一时间线中追踪 Bilibili 与 YouTube 创作者更新。",
      status: "初始化阶段",
      cards: {
        bilibiliPlatform: "Bilibili",
        bilibiliTitle: "统一视频流",
        bilibiliDescription: "视频卡片、时间线排序和平台筛选都会在这里落地。",
        youtubePlatform: "YouTube",
        youtubeTitle: "可通知工作流",
        youtubeDescription: "飞书配置和抓取自动化已经在后端完成脚手架。",
        systemPlatform: "系统",
        systemTitle: "可组合架构",
        systemDescription: "页面已经接入 Vue Router，随时可以连接 API 驱动的 store。",
      },
    },
    creators: {
      eyebrow: "创作者",
      title: "创作者管理页面",
      description: "后续接上 API 后，你可以在这里新增、删除和标注订阅的创作者。",
    },
    settings: {
      eyebrow: "设置",
      title: "飞书 Webhook 配置",
      description: "后端设置接口已经准备好，前端表单接入后即可完成配置。",
    },
    crawlLogs: {
      eyebrow: "抓取日志",
      title: "调度执行时间线",
      description: "任务接线完成后，这里会展示爬虫执行历史。",
    },
    auth: {
      loginEyebrow: "欢迎回来",
      loginTitle: "登录 FinFlow",
      registerEyebrow: "新建工作区",
      registerTitle: "创建你的账号",
      email: "邮箱",
      password: "密码",
      displayName: "显示名称",
      emailPlaceholder: "you@example.com",
      passwordPlaceholder: "••••••••",
      displayNamePlaceholder: "你的名字",
      registerPasswordPlaceholder: "至少 8 个字符",
      signIn: "登录",
      signingIn: "登录中…",
      createAccount: "创建账号",
      creatingAccount: "创建中…",
      noAccount: "还没有账号？",
      haveAccount: "已经有账号了？",
      createOne: "立即注册",
      signInLink: "去登录",
      loginFailed: "登录失败，请稍后重试。",
      registerFailed: "注册失败，请稍后重试。",
    },
  },
  en: {
    app: {
      localeLabel: "Language",
      switchToChinese: "切换到中文",
      switchToEnglish: "Switch to English",
    },
    nav: {
      product: "FinFlow",
      title: "Investor signal cockpit",
      feed: "Feed",
      creators: "Creators",
      settings: "Settings",
      crawlLogs: "Crawl Logs",
      signOut: "Sign out",
    },
    feed: {
      eyebrow: "Live Feed",
      title: "Track creators across Bilibili and YouTube in one timeline.",
      status: "Bootstrap state",
      cards: {
        bilibiliPlatform: "Bilibili",
        bilibiliTitle: "Unified video feed",
        bilibiliDescription: "Video cards, timeline sorting and platform filtering will land here.",
        youtubePlatform: "YouTube",
        youtubeTitle: "Notification-ready workflow",
        youtubeDescription: "Feishu settings and crawl automation are scaffolded on the backend.",
        systemPlatform: "System",
        systemTitle: "Composable architecture",
        systemDescription: "This page is wired through Vue Router and ready for API-backed stores.",
      },
    },
    creators: {
      eyebrow: "Creators",
      title: "Creator management scaffold",
      description: "Add, delete and annotate creator subscriptions here after API wiring.",
    },
    settings: {
      eyebrow: "Settings",
      title: "Feishu webhook setup",
      description: "Settings APIs are initialized on the backend and waiting for frontend forms.",
    },
    crawlLogs: {
      eyebrow: "Crawl Logs",
      title: "Scheduler activity timeline",
      description: "Crawler execution history will be shown here after job wiring is added.",
    },
    auth: {
      loginEyebrow: "Welcome back",
      loginTitle: "Sign in to FinFlow",
      registerEyebrow: "New workspace",
      registerTitle: "Create your account",
      email: "Email",
      password: "Password",
      displayName: "Display name",
      emailPlaceholder: "you@example.com",
      passwordPlaceholder: "••••••••",
      displayNamePlaceholder: "Your name",
      registerPasswordPlaceholder: "At least 8 characters",
      signIn: "Sign in",
      signingIn: "Signing in…",
      createAccount: "Create account",
      creatingAccount: "Creating account…",
      noAccount: "Don't have an account?",
      haveAccount: "Already have an account?",
      createOne: "Create one",
      signInLink: "Sign in",
      loginFailed: "Login failed. Please try again.",
      registerFailed: "Registration failed. Please try again.",
    },
  },
} as const;

type MessageTree = typeof messages;
type MessageKey =
  | "app.localeLabel"
  | "app.switchToChinese"
  | "app.switchToEnglish"
  | "nav.product"
  | "nav.title"
  | "nav.feed"
  | "nav.creators"
  | "nav.settings"
  | "nav.crawlLogs"
  | "nav.signOut"
  | "feed.eyebrow"
  | "feed.title"
  | "feed.status"
  | "feed.cards.bilibiliPlatform"
  | "feed.cards.bilibiliTitle"
  | "feed.cards.bilibiliDescription"
  | "feed.cards.youtubePlatform"
  | "feed.cards.youtubeTitle"
  | "feed.cards.youtubeDescription"
  | "feed.cards.systemPlatform"
  | "feed.cards.systemTitle"
  | "feed.cards.systemDescription"
  | "creators.eyebrow"
  | "creators.title"
  | "creators.description"
  | "settings.eyebrow"
  | "settings.title"
  | "settings.description"
  | "crawlLogs.eyebrow"
  | "crawlLogs.title"
  | "crawlLogs.description"
  | "auth.loginEyebrow"
  | "auth.loginTitle"
  | "auth.registerEyebrow"
  | "auth.registerTitle"
  | "auth.email"
  | "auth.password"
  | "auth.displayName"
  | "auth.emailPlaceholder"
  | "auth.passwordPlaceholder"
  | "auth.displayNamePlaceholder"
  | "auth.registerPasswordPlaceholder"
  | "auth.signIn"
  | "auth.signingIn"
  | "auth.createAccount"
  | "auth.creatingAccount"
  | "auth.noAccount"
  | "auth.haveAccount"
  | "auth.createOne"
  | "auth.signInLink"
  | "auth.loginFailed"
  | "auth.registerFailed";

function loadInitialLocale(): Locale {
  const saved = localStorage.getItem(LOCALE_KEY);
  return saved === "zh-CN" || saved === "en" ? saved : defaultLocale;
}

const locale = ref<Locale>(loadInitialLocale());

watch(
  locale,
  (value) => {
    localStorage.setItem(LOCALE_KEY, value);
    document.documentElement.lang = value;
  },
  { immediate: true },
);

function getMessageValue(tree: MessageTree[Locale], key: MessageKey): string {
  return key.split(".").reduce((current, part) => current[part as keyof typeof current], tree as any) as string;
}

export function useI18n() {
  const currentLocale = computed(() => locale.value);

  function setLocale(value: Locale) {
    locale.value = value;
  }

  function toggleLocale() {
    locale.value = locale.value === "zh-CN" ? "en" : "zh-CN";
  }

  function t(key: MessageKey) {
    return getMessageValue(messages[locale.value], key);
  }

  return {
    locale: currentLocale,
    setLocale,
    toggleLocale,
    t,
  };
}
