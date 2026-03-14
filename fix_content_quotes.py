import json
import re

with open('knowledge-base.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 逐行处理，只在 content 字段内部替换中文引号
in_content = False
content_start_line = -1
fixed_count = 0

for i, line in enumerate(lines):
    # 检测 content 字段开始
    if '"content":' in line and not in_content:
        in_content = True
        content_start_line = i
        # 检查这一行是否也包含 content 的结束
        # 如果行尾有 ", 则 content 在这一行结束
        if line.rstrip().endswith('",') or line.rstrip().endswith('"'):
            # 替换这一行中的中文引号
            original = line
            line = line.replace('"', '\\"').replace('"', '\\"')
            if line != original:
                lines[i] = line
                fixed_count += 1
                print(f'Fixed line {i+1} (single-line content)')
            in_content = False
    
    elif in_content:
        # 检查是否到达 content 的结束
        # content 通常在 </div>" 或类似的 HTML 结束标签后结束
        stripped = line.strip()
        if (stripped == '"' or stripped.endswith('",') or stripped.endswith('"')) and 'content' not in line.lower():
            # 这可能是 content 的结束
            # 替换这一行中的中文引号
            original = line
            line = line.replace('"', '\\"').replace('"', '\\"')
            if line != original:
                lines[i] = line
                fixed_count += 1
                print(f'Fixed line {i+1} (content end)')
            in_content = False
        else:
            # 在 content 内部，替换中文引号
            original = line
            line = line.replace('"', '\\"').replace('"', '\\"')
            if line != original:
                lines[i] = line
                fixed_count += 1
                print(f'Fixed line {i+1} (in content)')

print(f'\nTotal lines fixed: {fixed_count}')

# 验证修复
content = ''.join(lines)
json_start = content.find('{')
json_content = content[json_start:]

try:
    data = json.loads(json_content)
    print(f"✅ JSON 语法正确! 文章数量: {len(data.get('articles', {}))}")
    
    # 保存修复后的文件
    with open('knowledge-base.js', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("✅ 文件已保存")
    
except json.JSONDecodeError as e:
    print(f"❌ JSON 错误: 第 {e.lineno} 行 - {e.msg}")
