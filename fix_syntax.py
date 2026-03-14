import re

with open('knowledge-base.js', 'r') as f:
    content = f.read()

# 找到问题位置并修复
# 匹配 multi-delta-force 文章中 content 结束后的 pattern
old_pattern = r'(<div>\r\n    </div>")(\r\n    })(\r\n      "imagePrompt": "Multi-platform optimization diagram, performance metrics, 三角洲行动)'
new_replacement = r'\1\n\2,\n\3'

# 更简单的方法：直接查找并替换特定行
lines = content.split('\n')
for i, line in enumerate(lines):
    # 查找 "multi-delta-force" 文章中 content 结束的位置
    if 'multi-delta-force' in line and '"title"' in lines[i+1]:
        # 向前查找 content 的结束
        for j in range(i+1, min(i+50, len(lines))):
            if lines[j].strip() == '</div>"':
                # 找到 content 结束，检查下一行是否是 } 
                if j+1 < len(lines) and lines[j+1].strip() == '}':
                    # 在 } 后面添加逗号
                    lines[j+1] = lines[j+1].replace('}', '},', 1)
                    print(f"Fixed at line {j+1}")
                    break
                break

with open('knowledge-base.js', 'w') as f:
    f.write('\n'.join(lines))

print('Done')
