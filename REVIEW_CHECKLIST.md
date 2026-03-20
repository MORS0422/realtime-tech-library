# Realtime Tech Library Review 检查清单

**创建日期**: 2026-03-19
**目的**: 确保每次更新前进行本地验证，避免推送损坏的内容

---

## ✅ Pre-Push 检查清单

### 1. JSON 语法验证
```bash
cd ~/.openclaw/workspace/repos/realtime-tech-library
node --check knowledge-base.js
```
- [ ] 无语法错误
- [ ] 无未闭合的引号/括号
- [ ] 逗号分隔符正确

### 2. 文章完整性检查
```bash
python3 -c "
import json
with open('knowledge-base.js', 'r') as f:
    content = f.read()
json_start = content.find('{')
json_end = content.rfind('}') + 1
data = json.loads(content[json_start:json_end])
print(f'总文章数: {len(data[\"articles\"])}')
print(f'元数据: {data[\"meta\"]}')
"
```
- [ ] 文章数量符合预期
- [ ] 元数据已更新（lastUpdated, version）
- [ ] 新文章 ID 格式正确

### 3. 内容文件验证
```bash
ls -la articles/
```
- [ ] HTML 文件存在且非空
- [ ] 文件大小合理（> 5KB）
- [ ] 图片资源已生成或 placeholder 设置

### 4. 本地网站测试
```bash
# 启动本地服务器
python3 -m http.server 8080 &

# 测试关键功能
# - 首页加载
# - 专栏列表显示
# - 文章详情页打开
# - 搜索功能
# - 目录跳转
```
- [ ] 首页正常加载
- [ ] 所有专栏显示文章列表
- [ ] 点击文章能正常显示内容
- [ ] 无 JavaScript 错误

### 5. 内容质量检查
- [ ] 文章有符号定义表
- [ ] 包含核心理论部分
- [ ] 代码示例格式正确（语法高亮）
- [ ] 阅读时间合理（20-40分钟）
- [ ] 难度标签准确

---

## 🚫 禁止事项

1. **不要直接推送大段 HTML 到 JSON** - 使用 contentPath 指向单独文件
2. **不要删除旧文章** - 使用 v2Version 引用新版本
3. **不要跳过验证** - 即使时间紧迫也要检查
4. **不要覆盖其他正在进行的工作** - 先 pull 再 push

---

## 📝 Post-Push 检查

推送后 2-5 分钟内检查：
- [ ] GitHub Pages 部署成功（Settings > Pages）
- [ ] 网站在线版本正常
- [ ] 新文章能在网站上找到

---

## 🆘 故障恢复

如果推送后发现错误：

```bash
# 1. 立即回滚到上一个稳定版本
git log --oneline -5  # 找到上一个稳定 commit
git revert HEAD  # 或 git reset --hard <stable-commit>

# 2. 强制推送（谨慎使用）
git push -f origin main

# 3. 修复问题后重新提交
```

---

## 📊 质量指标

| 指标 | 目标 | 当前状态 |
|------|------|----------|
| JSON 验证通过率 | 100% | ✅ |
| 本地测试通过率 | 100% | ✅ |
| 用户反馈问题数 | < 2/周 | 监控中 |
| 平均修复时间 | < 30分钟 | 监控中 |

---

**Last Updated**: 2026-03-19
**Maintained by**: 布布管家
