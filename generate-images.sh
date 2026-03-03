#!/bin/bash
# BananaPro API 图片批量生成脚本
# API Key: AIzaSyBHMdw82XzE2h9PoiJkOakykRrRe3xQWa8

API_KEY="AIzaSyBHMdw82XzE2h9PoiJkOakykRrRe3xQWa8"
IMAGE_DIR="/tmp/realtime-tech-library/images"
LOG_FILE="/tmp/realtime-tech-library/logs/image-gen.log"

mkdir -p "$IMAGE_DIR"
mkdir -p "$(dirname $LOG_FILE)"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 生成单张图片
generate_image() {
    local prompt="$1"
    local output_file="$2"
    local article_id="$3"
    
    log "生成图片: $article_id"
    log "提示词: ${prompt:0:80}..."
    
    # 使用 Google Gemini API 生成图片
    # 注意：需要使用支持图片生成的模型
    curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key=$API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"contents\": [{
                \"parts\": [{\"text\": \"$prompt\"}]
            }],
            \"generationConfig\": {
                \"responseModalities\": [\"TEXT\", \"IMAGE\"]
            }
        }" > "$output_file.tmp"
    
    # 检查是否成功
    if grep -q '"image"' "$output_file.tmp"; then
        # 提取base64图片数据
        python3 << EOF
import json
import base64

with open('$output_file.tmp', 'r') as f:
    data = json.load(f)

# 查找图片数据
for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
    if 'inlineData' in part:
        image_data = base64.b64decode(part['inlineData']['data'])
        with open('$output_file', 'wb') as img:
            img.write(image_data)
        print(f"图片保存成功: $output_file")
        break
EOF
        rm "$output_file.tmp"
        return 0
    else
        log "生成失败，保存响应到日志"
        mv "$output_file.tmp" "$output_file.error.json"
        return 1
    fi
}

# 批量生成
generate_all() {
    log "=== 开始批量生成图片 ==="
    
    # 读取知识库获取所有图片提示
    node << 'NODE_SCRIPT'
const fs = require('fs');
const content = fs.readFileSync('/tmp/realtime-tech-library/knowledge-base.js', 'utf8');
const match = content.match(/const knowledgeBase = ({[\s\S]+});\s*$/);
const kb = eval('(' + match[1] + ')');

const articles = Object.entries(kb.articles);
console.log(`共有 ${articles.length} 篇文章需要生成图片`);

articles.forEach(([id, article], index) => {
    const filename = `${article.category}-${id}.png`;
    console.log(`${index + 1}|${id}|${filename}|${article.imagePrompt || 'default'}`);
});
NODE_SCRIPT
}

# 检查API状态
check_api() {
    log "检查API状态..."
    
    local response=$(curl -s -X POST \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"contents": [{"parts": [{"text": "Hello"}]}]}')
    
    if echo "$response" | grep -q '"text"'; then
        log "✅ API 正常"
        return 0
    elif echo "$response" | grep -q 'RESOURCE_EXHAUSTED'; then
        log "⚠️  API配额已用完，请稍后重试"
        return 1
    else
        log "❌ API错误: $response"
        return 1
    fi
}

# 主入口
case "$1" in
    check)
        check_api
        ;;
    generate)
        if check_api; then
            generate_all
        fi
        ;;
    single)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: $0 single \"image prompt\" output.png"
            exit 1
        fi
        generate_image "$2" "$3" "manual"
        ;;
    *)
        echo "BananaPro (Google Gemini) 图片生成脚本"
        echo ""
        echo "用法:"
        echo "  $0 check        - 检查API状态"
        echo "  $0 generate     - 批量生成所有文章图片"
        echo "  $0 single \"prompt\" output.png  - 生成单张图片"
        echo ""
        echo "配置:"
        echo "  API Key: ${API_KEY:0:20}..."
        echo "  输出目录: $IMAGE_DIR"
        ;;
esac
