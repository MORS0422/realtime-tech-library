#!/usr/bin/env python3
"""正确添加 Niagara V2 文章到 knowledge-base.js"""

import json
import os

REPO_DIR = "/Users/morszhu/.openclaw/workspace/repos/realtime-tech-library"

def load_kb():
    with open(f"{REPO_DIR}/knowledge-base.js", 'r') as f:
        content = f.read()
    json_start = content.find('{')
    json_end = content.rfind('}') + 1
    return json.loads(content[json_start:json_end])

def save_kb(data):
    js_content = f"const knowledgeBase = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    with open(f"{REPO_DIR}/knowledge-base.js", 'w') as f:
        f.write(js_content)
    print("✅ 已更新 knowledge-base.js")

def add_niagara_v2_articles(data):
    """添加 Niagara V2 文章（使用 contentPath 而不是直接嵌入 content）"""
    
    # Niagara Decal V2 文章
    data['articles']['niagara-decal-v2'] = {
        "title": "Niagara Decal 渲染器完全指南：投影映射、Deferred Decal 与动态淡入淡出",
        "category": "ta-render",
        "tags": [
            "Projective Mapping",
            "Box Projection",
            "Normal Blending",
            "Deferred Decal",
            "DBuffer",
            "Niagara粒子系统"
        ],
        "date": "2026-03-19",
        "author": "Realtime Tech Library / V2概念版",
        "readTime": "25-30分钟",
        "difficulty": "中等",
        "isV2": True,
        "originalId": "3afcd990447d",
        "content": "",  # 内容在单独文件中
        "contentPath": "articles/niagara-decal-v2.html",
        "imagePrompt": "Technical diagram showing Box Projection matrix, Decal rendering pipeline with Projective Mapping, UE5 Niagara interface, dark theme with mathematical formulas and geometric projections, professional technical illustration, dark background with pink/magenta accents",
        "hasImage": True
    }
    
    # 更新原始 Decal 文章，添加 v2Version 引用
    if '3afcd990447d' in data['articles']:
        data['articles']['3afcd990447d']['v2Version'] = 'niagara-decal-v2'
    
    # 更新元数据
    data['meta']['lastUpdated'] = '2026-03-19 18:20'
    data['meta']['totalArticles'] = 60
    data['meta']['version'] = '6.3'
    data['meta']['newArticles'] = ['niagara-decal-v2']
    
    print("✅ 已添加 Niagara Decal V2 文章")
    return data

if __name__ == "__main__":
    print("=== 添加 Niagara V2 文章 ===\n")
    data = load_kb()
    data = add_niagara_v2_articles(data)
    save_kb(data)
    print("\n✅ 完成！")
