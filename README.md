# CACM Daily News · 云端每日推送

每天早上（北京时间 09:00）自动抓取 **Communications of the ACM 的 所有栏目**最新文章，
生成中文摘要、核心要点、中文思维导图和**中英对照全文**，发到你的邮箱。

跑在 **GitHub Actions** 上——**电脑关机也照常执行**，不需要你开着电脑。

```
GitHub Actions（每天 01:00 UTC / 09:00 CST）
   └─ fetch  → 翻译（DeepSeek）→ 摘要 + 思维导图 → SMTP 发信
```

邮件长这样：HTML 正文（摘要 + 要点 + 内嵌思维导图）+ `article.md` 附件（中英对照全文）。

---

## 一、部署（5 步，约 10 分钟）

### 1. 建一个 GitHub 仓库

- 打开 <https://github.com/new>，名字随意（如 `cacm-daily`），**Private 或 Public 都行**。
- 不要勾选 "Add a README file"（避免冲突）。

### 2. 上传本目录的所有文件

方式 A（不用装 Git）：仓库页面 → **Add file → Upload files**，把 `cacm-daily-cloud`
**里面的内容**（不是文件夹本身）拖进去，注意 `.github` 目录也要一起上传
（网页上传支持拖文件夹）。

方式 B（有 Git）：

```bash
cd cacm-daily-cloud
git init && git add -A
git commit -m "init"
git branch -M main
git remote add origin https://github.com/<你的用户名>/cacm-daily.git
git push -u origin main
```

### 3. 添加 Secrets

仓库 → **Settings → Secrets and variables → Actions → New repository secret**，
逐个添加：

| Secret | 必填 | 说明 |
| --- | --- | --- |
| `DEEPSEEK_API_KEY` | ✅ | DeepSeek 开放平台的 key（`sk-` 开头） |
| `SMTP_HOST` | ✅ | 如 `smtp.qq.com` |
| `SMTP_PORT` | ✅ | `465`（SSL）或 `587`（STARTTLS） |
| `SMTP_USER` | ✅ | 发件邮箱，如 `you@qq.com` |
| `SMTP_PASS` | ✅ | **授权码**，不是邮箱登录密码（见下表） |
| `MAIL_TO` | ✅ | 收件邮箱，多个用英文逗号分隔 |
| `MAIL_FROM` | ⬜ | 发件人地址，默认等于 `SMTP_USER` |

**各邮箱的 SMTP 参数：**

| 邮箱 | SMTP_HOST | 端口 | SMTP_PASS 怎么拿 |
| --- | --- | --- | --- |
| QQ 邮箱 | `smtp.qq.com` | 465 | 设置 → 账户 → 开启 POP3/SMTP → 生成**授权码** |
| 163 邮箱 | `smtp.163.com` | 465 | 设置 → POP3/SMTP/IMAP → 开启服务 → 设置**客户端授权密码** |
| Gmail | `smtp.gmail.com` | 465 | 开启两步验证 → 生成**应用专用密码** |
| Outlook | `smtp.office365.com` | 587 | 账户安全 → 应用密码 |

### 4. 手动跑一次（测试）

仓库 → **Actions** → 左侧 **CACM Daily News** → **Run workflow**：

- 想测试完整流程：在 `force_id` 填 `813528`（一篇已有的 News 文章，可重复测试，不会污染去重状态）
- 想测试定时逻辑：留空直接跑（如果最新文章已推送过，会显示 `NO_NEW` 并正常退出）

跑完看日志里有没有 `MAIL: {"status": "sent" ...}`，然后查收邮箱。

> 第一次运行若提示权限错误：**Settings → Actions → General → Workflow permissions**
> 选 **Read and write permissions**，保存后重跑。

### 5. 完成

之后每天北京时间 09:00 自动执行。想改时间就改 `.github/workflows/daily.yml` 里的
`cron: "0 1 * * *"`（UTC 时间，北京时间 = UTC + 8）。

---

## 二、它是怎么判断「新文章」的

- 站点：`https://cacm.acm.org/wp-json/wp/v2/posts?section=72`（News 栏目，
  普通网页有反爬，但 WordPress API 可以直连，返回全文 HTML）。
- `state.json` 记录已推送的文章 id，随仓库一起提交，所以**不会重复推送**。
- 只处理 **7 天内** 的文章；更旧的视为过期，避免把陈年旧闻当新闻。
- 自动跳过 "Call for Papers" 这类通知稿。

> News 栏目实际是**每周 2~4 篇**，不是每天都有。没有新稿的那天，Actions 会正常退出、不发信。

---

## 三、常见问题

**Q：会延迟吗？**
GitHub 的 schedule 在高峰期可能延迟 5~20 分钟，属于正常现象。

**Q：60 天后定时任务被自动停用？**
GitHub 会停用长期无活动的仓库的定时任务。本流程每次运行都会更新并提交
`state.json`（`last_check` 时间戳），所以只要在跑就不会被停用。如果收到
"workflow disabled" 邮件，去 Actions 页面点一次 **Enable workflow** 即可。

**Q：费用？**
- GitHub Actions：私有仓库每月 2000 分钟免费，本任务每天约 1~2 分钟，够用。
- DeepSeek：每篇文章约 2 次调用，合计几分钱。

**Q：能改成推送博客（BLOG@CACM）或不限栏目吗？**
改 `.github/workflows/daily.yml` 里的 `CACM_SECTION`：`72` = News，`164` = 博客，`0` = 全部。

**Q：能只发到手机、不发邮件？**
邮件本身就是手机上最完整的载体（能带图片和附件）。如果一定要 IM 推送，
可以在 `scripts/mailer.py` 里换成 Bark / Server酱 / 企业微信机器人——它们只能发文字，
图片需要公网 URL。

**Q：想多收几个人？**
`MAIL_TO` 用逗号分隔多个地址即可。

---

## 四、本地调试

```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY=sk-xxx
python scripts/main.py --force 813528            # 完整跑一篇
python scripts/main.py --force 813528 --dry-run out.eml   # 只生成 .eml 不发信
```

Windows PowerShell 用 `$env:DEEPSEEK_API_KEY="sk-xxx"`。

`--dry-run` 生成的 `.eml` 可直接用邮件客户端打开预览。

---

## 五、目录结构

```
cacm-daily-cloud/
├─ .github/workflows/daily.yml   # 定时任务定义
├─ scripts/
│  ├─ main.py                    # 主流程
│  ├─ fetch.py                   # 抓取 + 去重 + 正文抽取
│  ├─ ai.py                      # DeepSeek：翻译 + 摘要/要点/导图结构
│  ├─ render.py                  # 思维导图 PNG + 中英对照 Markdown
│  └─ mailer.py                  # HTML 邮件组装与 SMTP 发送
├─ state.json                    # 已推送文章记录（自动更新）
├─ articles/<日期>-<slug>/       # 每期产物（自动累积）
│  ├─ article.md                 # 中英对照全文
│  ├─ mindmap.png                # 思维导图
│  ├─ blocks.json / translations.json / meta.json
└─ requirements.txt
```

---

英文原文版权归 Communications of the ACM 及作者所有；中文译文由 AI 辅助生成，仅供个人学习参考。
