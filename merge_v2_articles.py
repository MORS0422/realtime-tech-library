#!/usr/bin/env python3
"""
合并V2文章到 knowledge-base.js
"""

import json
import re
from datetime import datetime

# 读取V2文章
v2_articles = []
for filename in ['pscatter-v2.json', '3dgs-render-v2.json']:
    with open(f'articles-v2/{filename}', 'r', encoding='utf-8') as f:
        article = json.load(f)
        v2_articles.append(article)

print(f"Loaded {len(v2_articles)} V2 articles")

# 读取当前的 knowledge-base.js
with open('knowledge-base.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取JavaScript对象部分（去掉 const knowledgeBase = 和最后的 ;）
match = re.search(r'const knowledgeBase = (\{[\s\S]*\});', content)
if not match:
    print("Error: Could not parse knowledge-base.js")
    exit(1)

# 解析JSON（JavaScript对象可能需要一些转换）
js_content = match.group(1)

# 简单的转换：去掉尾部逗号，处理单引号等
# 使用json5或手动处理，这里我们使用一个简单的方法

# 找到 articles 对象的位置
articles_match = re.search(r'"articles": \{', js_content)
if not articles_match:
    print("Error: Could not find articles section")
    exit(1)

# 在 articles 对象的闭合括号前插入新文章
insert_pos = js_content.rfind('}')

# 准备新文章内容
new_articles_js = []
for article in v2_articles:
    article_id = article['id']
    # 移除id字段，因为在JS对象中键就是id
    article_data = {k: v for k, v in article.items() if k != 'id'}
    
    # 转换为JSON字符串，保持格式
    article_json = json.dumps(article_data, ensure_ascii=False, indent=2)
    # 缩进调整
    article_json = article_json.replace('\n', '\n    ')
    
    new_articles_js.append(f'"{article_id}": {article_json}')

# 合并所有新文章
new_articles_str = ',\n    '.join(new_articles_js)

# 在最后一个文章之前插入（需要找到正确的位置）
# 找到 meta 之前的那个 }
meta_pos = js_content.find('"meta":')
if meta_pos == -1:
    print("Error: Could not find meta section")
    exit(1)

# 在 meta 之前插入新文章
# 找到 meta 前的一个换行和空格
insert_before_meta = js_content.rfind('\n  }', 0, meta_pos)
if insert_before_meta == -1:
    insert_before_meta = js_content.rfind('}', 0, meta_pos)

# 构建新的内容
new_content = (
    js_content[:insert_before_meta] + 
    ',\n    ' + new_articles_str +
    js_content[insert_before_meta:]
)

# 更新 meta 部分
# 更新 lastUpdated
new_content = re.sub(
    r'"lastUpdated": "[^"]*"',
    f'"lastUpdated": "{datetime.now().strftime("%Y-%m-%d %H:%M")}"',
    new_content
)

# 更新 totalArticles
old_total = int(re.search(r'"totalArticles": (\d+)', new_content).group(1))
new_total = old_total + len(v2_articles)
new_content = re.sub(
    r'"totalArticles": \d+',
    f'"totalArticles": {new_total}',
    new_content
)

# 更新 newArticles 列表
new_article_ids = [f'"{a["id"]}"' for a in v2_articles]
new_articles_list = ',\n      '.join(new_article_ids)

# 替换 newArticles
new_content = re.sub(
    r'"newArticles": \[([^\]]*)\]',
    f'"newArticles": [\1,\n      {new_articles_list}]',
    new_content
)

# 重新组装文件
final_content = f'const knowledgeBase = {new_content};\n'

# 写入文件
with open('knowledge-base.js', 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"✅ Successfully merged {len(v2_articles)} articles")
print(f"   Total articles: {old_total} → {new_total}")
print(f"   New articles: {', '.join([a['id'] for a in v2_articles])}")
