import re

with open('knowledge-base.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修复第918行 (索引917)
if len(lines) > 917:
    line = lines[917]
    # 将 "Write Once, Run Everywhere" 替换为 \\"Write Once, Run Everywhere\\"
    line = line.replace('"Write Once, Run Everywhere"', '\\"Write Once, Run Everywhere\\"')
    lines[917] = line
    print('Fixed line 918')

with open('knowledge-base.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done')
