import re
import json

with open('knowledge-base.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: 修复中文引号 - 将中文引号替换为英文引号并转义
# 中文左引号 U+201C -> \\"
# 中文右引号 U+201D -> \\"
content = content.replace('"', '\\"')
content = content.replace('"', '\\"')

# Step 2: 验证 JSON
json_start = content.find('{')
json_content = content[json_start:]

try:
    data = json.loads(json_content)
    print(f"✅ JSON 语法正确! 文章数量: {len(data.get('articles', {}))}")
    
    # 保存修复后的文件
    with open('knowledge-base.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 文件已保存")
    
except json.JSONDecodeError as e:
    print(f"❌ JSON 错误: 第 {e.lineno} 行")
    print(f"错误信息: {e.msg}")
    
    # 显示上下文
    lines = json_content.split('\n')
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    print("\n上下文:")
    for i in range(start, end):
        marker = ">>> " if i == e.lineno - 1 else "    "
        print(f"{marker}{i+1}: {lines[i][:100]}")
