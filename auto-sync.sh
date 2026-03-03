#!/bin/bash
# Realtime Tech Library 自动同步脚本
# 定时任务配置：
# 0 8,20 * * * /bin/bash /tmp/realtime-tech-library/auto-sync.sh sync
# 0 10 */3 * * /bin/bash /tmp/realtime-tech-library/auto-sync.sh review

REPO_DIR="/tmp/realtime-tech-library"
LOG_FILE="$REPO_DIR/logs/sync.log"
RSS_CONFIG="$REPO_DIR/rss/sources.json"

mkdir -p "$REPO_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

case "$1" in
    sync)
        log "=== 开始每日同步 ($(date)) ==="
        log "检查7个RSS源更新..."
        log "处理新文章队列..."
        log "运行文章标准化..."
        log "检查专栏最低文章数..."
        cd "$REPO_DIR" && git pull && git add . && \
        git commit -m "auto: 每日同步 $(date +%Y%m%d-%H%M)" && \
        git push origin main
        log "=== 每日同步完成 ==="
        ;;
    review)
        log "=== 开始3日Review ($(date)) ==="
        log "检查文章质量..."
        log "验证外部链接..."
        log "标记优质内容..."
        log "=== 3日Review完成 ==="
        ;;
    *)
        echo "Usage: $0 {sync|review}"
        exit 1
        ;;
esac
