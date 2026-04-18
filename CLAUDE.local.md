# CLAUDE.local.md — 开发进度记录

## 当前状态（2026-04-19）

### 已完成
- Feed 页 CSS 5 列网格（`.video-grid-sm`）Vite 缓存问题已修复（`docker compose restart frontend`）
- 前端导航与文案调整：
  - 标题：「投资信号驾驶舱」→「金融资讯」
  - 导航「动态」→「最新内容动态」
  - 导航「创作者」→「信源管理」
  - 「抓取日志」+「设置」合并为「控制中心」（`/control-center`，`ControlCenterView.vue`）
  - 新增「内容分析」导航入口（`/content-analysis`，`ContentAnalysisView.vue`，占位页面）
  - Feed 每页从 20 改为 15（5×3 网格，便于翻页验证）

### 已修改文件
| 文件 | 改动 |
|---|---|
| `frontend/src/i18n.ts` | nav.title/feed/creators 文案；新增 nav.controlCenter/contentAnalysis key；新增 contentAnalysis.* 消息块；更新 MessageKey 类型 |
| `frontend/src/views/FeedView.vue` | PAGE_SIZE 20→15 |
| `frontend/src/components/layout/AppShell.vue` | 导航链接调整为 /content-analysis 和 /control-center |
| `frontend/src/router/index.ts` | 路由替换：settings+crawl-logs → control-center+content-analysis |
| `frontend/src/views/ControlCenterView.vue` | 新建，合并 settings+crawlLogs 内容 |
| `frontend/src/views/ContentAnalysisView.vue` | 新建，占位页面 |

### 待验证
- 刷新浏览器确认 5 列网格正常（上次 Vite 已重启）
- 确认新导航路由均可访问（/content-analysis, /control-center）
- 确认翻页功能（15 条/页）

### 下一步主线
1. 打通飞书 Webhook 通知（控制中心配置表单）
2. 内容分析页接入大模型（视频摘要/投研洞察）
3. 控制中心展示真实抓取日志
