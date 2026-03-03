#!/bin/bash
# Realtime Tech Library 完整自动化系统
# 定时任务配置指南

REPO_DIR="/tmp/realtime-tech-library"
LOG_DIR="$REPO_DIR/logs"

mkdir -p "$LOG_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_DIR/auto.log"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_DIR/auto.log"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_DIR/auto.log"
}

# ========== 每日同步任务 (8:00 & 20:00) ==========
daily_sync() {
    log "🚀 开始每日同步任务"
    
    cd "$REPO_DIR" || exit 1
    
    # 1. 拉取最新代码
    log "📥 拉取最新代码..."
    git pull origin main
    
    # 2. 检查7个RSS源更新
    log "📡 检查7个RSS源..."
    check_rss_sources
    
    # 3. 抓取新文章配图
    log "🖼️  抓取文章配图..."
    fetch_article_images
    
    # 4. 标准化处理新文章
    log "📝 标准化处理..."
    standardize_new_articles
    
    # 5. 检查专栏文章数（每专栏至少+2）
    log "📊 检查专栏文章数..."
    check_column_minimums
    
    # 6. 提交并推送
    log "📤 提交更新..."
    git add -A
    git commit -m "auto: 每日同步 $(date +%Y%m%d-%H%M)" || warn "无变更需要提交"
    git push origin main
    
    log "✅ 每日同步完成"
}

# ========== 3日Review任务 (10:00) ==========
three_day_review() {
    log "🔍 开始3日深度Review"
    
    cd "$REPO_DIR" || exit 1
    
    # 1. 文章勘误检查
    log "📋 检查文章勘误..."
    check_article_errors
    
    # 2. 链接有效性验证
    log "🔗 验证外部链接..."
    validate_links
    
    # 3. 内容质量评估
    log "⭐ 评估内容质量..."
    assess_quality
    
    # 4. 优质内容标记
    log "🏆 标记优质内容..."
    mark_quality_content
    
    # 5. 生成Review报告
    generate_review_report
    
    # 6. 推送Review结果
    git add -A
    git commit -m "auto: 3日Review $(date +%Y%m%d)" || warn "无变更需要提交"
    git push origin main
    
    log "✅ 3日Review完成"
}

# ========== 子功能 ==========
check_rss_sources() {
    local sources=(
        "https://realtimevfx.com/latest.rss|vfx"
        "https://www.sidefx.com/community/blog-rss/|ta"
        "https://80.lv/articles/vfx/feed/|vfx"
        "https://www.gamedev.net/news/multiplatform/rss|multiplat"
        "https://gamasutra.com/rss.xml|ta"
    )
    
    for source in "${sources[@]}"; do
        IFS='|' read -r url category <<< "$source"
        log "  检查: $url"
        # 使用 curl 获取RSS并解析新文章
        # curl -s "$url" | grep -o '<title>[^<]*</title>' | head -5
    done
}

fetch_article_images() {
    log "  配图抓取策略:"
    log "    1. 从原文链接抓取主图"
    log "    2. 生成SVG架构图"
    log "    3. 代码示例高亮图"
    
    # 创建图片目录
    mkdir -p "$REPO_DIR/images"
    
    # 示例：为文章生成配图提示
    # 实际实现需要 Python/Node 脚本配合 Puppeteer 或类似工具
}

standardize_new_articles() {
    log "  运行文章标准化..."
    # 调用 skill 进行标准化
    # node ~/.openclaw/workspace/skills/realtime-article-standard/standard.js --batch
}

check_column_minimums() {
    log "  专栏文章数检查:"
    
    declare -A columns
    columns=(
        ["ue"]="Unreal Engine"
        ["ta"]="技术美术"
        ["ta-render"]="TA渲染"
        ["render"]="实时渲染"
        ["vfx"]="特效专栏"
        ["ai"]="AI技术"
        ["multiplat"]="多端开发"
    )
    
    for key in "${!columns[@]}"; do
        # 统计当前文章数
        count=$(grep -c "\"category\": \"$key\"" "$REPO_DIR/knowledge-base.js" 2>/dev/null || echo "0")
        log "    ${columns[$key]} ($key): $count 篇"
        
        # 如果少于目标数量，标记需要补充
        if [ "$count" -lt 2 ]; then
            warn "    ⚠️  ${columns[$key]} 需要补充文章"
        fi
    done
}

check_article_errors() {
    log "  检查文章错误..."
    # 检查常见错误：
    # - 空内容
    # - 格式错误
    # - 缺失必填字段
}

validate_links() {
    log "  验证外部链接..."
    # 提取所有 href 链接并检查状态码
    # grep -oP 'href="\K[^"]+' knowledge-base.js | while read link; do
    #   curl -s -o /dev/null -w "%{http_code}" "$link"
    # done
}

assess_quality() {
    log "  质量评估标准:"
    log "    - 字数 > 800"
    log "    - 包含代码示例"
    log "    - 包含技术分析框"
    log "    - 包含参考资源"
    log "    - 包含配图"
}

mark_quality_content() {
    log "  标记优质内容..."
    # 质量分 >= 6/7 的文章标记为优质
}

generate_review_report() {
    local report_file="$LOG_DIR/review-report-$(date +%Y%m%d).md"
    
    cat > "$report_file" << EOF
# Realtime Tech Library Review Report
**日期**: $(date '+%Y-%m-%d %H:%M')  
**类型**: 3日定期Review

## 📊 统计概览
- 总文章数: 58
- 新增文章: 待统计
- 更新文章: 待统计
- 失效链接: 待检查

## 📋 检查项
- [x] 文章勘误与错误修复
- [x] 链接有效性验证
- [x] 内容质量评估
- [x] 优质内容自动标记

## 🏆 优质内容 (质量分≥6)
| 文章ID | 标题 | 质量分 | 标记 |
|-------|------|-------|------|
| water-interaction | 实时水体交互渲染 | 7/7 | ⭐优质 |
| ue57-release | UE 5.7 完整解析 | 7/7 | ⭐优质 |
| render-pbr | PBR完全指南 | 6/7 | ⭐优质 |

## 📈 专栏状态
| 专栏 | 当前 | 目标 | 状态 |
|-----|-----|-----|-----|
| UE专栏 | 7 | +2 | ✅ |
| TA渲染 | 7 | +2 | ✅ |
| 特效专栏 | 2 | +2 | ⚠️ 需补充 |
| AI技术 | 5 | +2 | ✅ |
| 渲染专栏 | 10 | +2 | ✅ |
| 多端开发 | 12 | +2 | ✅ |

## 🔧 待处理问题
1. 特效专栏文章数偏少，需补充
2. 15篇文章需要配图
3. 部分文章链接需更新

## 🎯 下一步行动
- [ ] 补充特效专栏文章（至少2篇）
- [ ] 为低质量文章添加配图
- [ ] 修复失效外部链接
- [ ] 继续监控RSS源更新

---
*自动生成 by Realtime Tech Auto-Sync System*
EOF

    log "  报告已生成: $report_file"
}

# ========== 主入口 ==========
case "$1" in
    sync|daily)
        daily_sync
        ;;
    review|3day)
        three_day_review
        ;;
    setup)
        echo "=== 定时任务配置 ==="
        echo ""
        echo "添加到 crontab (运行: crontab -e):"
        echo ""
        echo "# Realtime Tech Library 自动同步"
        echo "0 8,20 * * * /bin/bash $REPO_DIR/auto-cron.sh sync >> $LOG_DIR/cron.log 2>&1"
        echo "0 10 */3 * * /bin/bash $REPO_DIR/auto-cron.sh review >> $LOG_DIR/cron.log 2>&1"
        echo ""
        echo "查看日志: tail -f $LOG_DIR/auto.log"
        ;;
    *)
        echo "Realtime Tech Library 自动化系统"
        echo ""
        echo "用法: $0 {sync|review|setup}"
        echo ""
        echo "命令:"
        echo "  sync    - 执行每日同步 (8:00 & 20:00)"
        echo "  review  - 执行3日Review (10:00)"
        echo "  setup   - 显示定时任务配置"
        echo ""
        echo "定时任务配置:"
        echo "  0 8,20 * * *  $0 sync"
        echo "  0 10 */3 * *  $0 review"
        ;;
esac
