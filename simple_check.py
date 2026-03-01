# -*- coding: utf-8 -*-
import json
import re

with open('knowledge-base.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'articles:\s*({.*?}),\s*currentCategory', content, re.DOTALL)
if match:
    articles = json.loads(match.group(1))
    print('当前文章数:', len(articles))
    print('前5篇:', list(articles.keys())[:5])
