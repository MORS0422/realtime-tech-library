# Realtime Tech 自动知识库 - 使用指南

## ✅ 系统状态

| 组件 | 状态 |
|------|------|
| RSS 抓取器 | ✅ 运行正常 |
| 内容处理器 | ✅ 运行正常 |
| 知识库生成器 | ✅ 运行正常 |
| 定时任务 | ⏳ 待配置 |

## 📁 文件结构

```
realtime-tech/
├── index.html              # 主页面
├── knowledge-base.js       # ⭐ 自动生成的知识库 (每2小时更新)
├── ARCHITECTURE.md         # 系统架构文档
├── data/
│   ├── sources.json        # RSS 源配置
│   └── articles.json       # 抓取的文章数据
├── scripts/
│   ├── update_kb.py        # ⭐ 主更新脚本
│   └── cron_job.sh         # 定时任务脚本
└── logs/
    └── update.log          # 更新日志
```

## 🚀 手动运行更新

```bash
cd /Users/morszhu/workspace/realtime-tech
python3 scripts/update_kb.py
```

## ⏰ 设置定时任务 (每2小时自动运行)

### 方法一：使用 macOS launchd (推荐)

创建 plist 文件：

```bash
cat > ~/Library/LaunchAgents/com.realtime-tech.update.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.realtime-tech.update</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/morszhu/workspace/realtime-tech/scripts/cron_job.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>7200</integer>
    <key>StandardOutPath</key>
    <string>/Users/morszhu/workspace/realtime-tech/logs/cron.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/morszhu/workspace/realtime-tech/logs/cron-error.log</string>
</dict>
</plist>
EOF
```

加载定时任务：

```bash
launchctl load ~/Library/LaunchAgents/com.realtime-tech.update.plist
launchctl start com.realtime-tech.update
```

### 方法二：使用 cron

```bash
crontab -e
```

添加以下行：

```
0 */2 * * * /bin/bash /Users/morszhu/workspace/realtime-tech/scripts/cron_job.sh
```

## 📊 当前数据源

| 源名称 | 类型 | 状态 | 抓取数量 |
|--------|------|------|----------|
| Unreal Engine Blog | RSS | ⚠️ 暂无新内容 | 0 |
| 80 Level | RSS | ⚠️ 暂无新内容 | 0 |
| GameDev.net | RSS | ⚠️ 暂无新内容 | 0 |
| CG Channel | RSS | ✅ 正常 | 5 |
| Realtime VFX | RSS | ✅ 正常 | 5 |

**总计: 10 篇新文章 + 2 篇原有文章 = 12 篇**

## 📝 自定义 RSS 源

编辑 `data/sources.json` 添加/修改数据源：

```json
{
  "id": "自定义ID",
  "name": "显示名称",
  "type": "rss",
  "url": "https://example.com/feed.xml",
  "category": "ue|ta|render|ta-render|ai",
  "enabled": true
}
```

## 🔍 查看日志

```bash
# 更新日志
tail -f /Users/morszhu/workspace/realtime-tech/logs/update.log

# 定时任务日志
tail -f /Users/morszhu/workspace/realtime-tech/logs/cron.log
```

## 🎯 下一步计划

- [ ] 添加更多 RSS 源 (SIGGRAPH, GDC Vault 等)
- [ ] 集成 AI 生成深度分析
- [ ] 添加文章评分/推荐系统
- [ ] 支持中文翻译

## 💡 提示

1. 首次运行后，`knowledge-base.js` 会自动更新
2. 刷新浏览器即可看到新文章
3. 原有手动编写的深度文章保持不变
4. 重复文章会自动去重
