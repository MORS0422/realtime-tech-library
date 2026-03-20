#!/usr/bin/env python3
"""正确添加所有 Niagara V2 文章到 knowledge-base.js"""

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

def add_all_niagara_v2(data):
    """添加所有 Niagara V2 文章"""
    
    new_articles = []
    
    # 1. Niagara Decal V2
    if 'niagara-decal-v2' not in data['articles']:
        data['articles']['niagara-decal-v2'] = {
            "title": "Niagara Decal 渲染器完全指南：投影映射、Deferred Decal 与动态淡入淡出",
            "category": "ta-render",
            "tags": ["Projective Mapping", "Box Projection", "Normal Blending", "Deferred Decal", "DBuffer", "Niagara粒子系统"],
            "date": "2026-03-19",
            "author": "Realtime Tech Library / V2概念版",
            "readTime": "25-30分钟",
            "difficulty": "中等",
            "isV2": True,
            "originalId": "3afcd990447d",
            "content": "",
            "contentPath": "articles/niagara-decal-v2.html",
            "imagePrompt": "Technical diagram showing Box Projection matrix, Decal rendering pipeline with Projective Mapping, UE5 Niagara interface, dark theme with mathematical formulas and geometric projections",
            "hasImage": True
        }
        new_articles.append('niagara-decal-v2')
        print("✅ 已添加: niagara-decal-v2")
    
    # 2. Niagara PostProcess V2
    if 'niagara-postprocess-v2' not in data['articles']:
        data['articles']['niagara-postprocess-v2'] = {
            "title": "Niagara 后处理控制完全指南：ACES、HDR、Bloom 与 Niagara 数据驱动",
            "category": "ta-render",
            "tags": ["ACES", "HDR", "Bloom", "Tone Mapping", "Color Grading", "Niagara", "后处理体积"],
            "date": "2026-03-19",
            "author": "Realtime Tech Library / V2概念版",
            "readTime": "30-35分钟",
            "difficulty": "困难",
            "isV2": True,
            "originalId": "514c7a61d0d8",
            "content": "",
            "contentPath": "articles/niagara-postprocess-v2.html",
            "imagePrompt": "Technical diagram showing ACES color pipeline, HDR tone mapping curves, UE5 Post Process Volume interface, Niagara to PPV data flow, dark theme with color science formulas",
            "hasImage": True
        }
        new_articles.append('niagara-postprocess-v2')
        print("✅ 已添加: niagara-postprocess-v2")
    
    # 3. Niagara Slime V2
    if 'niagara-slime-v2' not in data['articles']:
        data['articles']['niagara-slime-v2'] = {
            "title": "Niagara 粘液特效完全指南：非牛顿流体、SPH 模拟与粘弹性物理",
            "category": "ta-render",
            "tags": ["非牛顿流体", "SPH", "Herschel-Bulkley", "粘弹性", "次表面散射", "Niagara GPU粒子"],
            "date": "2026-03-19",
            "author": "Realtime Tech Library / V2概念版",
            "readTime": "30-35分钟",
            "difficulty": "困难",
            "isV2": True,
            "originalId": "338c49bf45db",
            "content": "",
            "contentPath": "articles/niagara-slime-v2.html",
            "imagePrompt": "Technical diagram showing non-Newtonian fluid simulation, SPH particle interactions, Herschel-Bulkley viscosity curves, UE5 Niagara slime effect, dark theme with physics formulas",
            "hasImage": True
        }
        new_articles.append('niagara-slime-v2')
        print("✅ 已添加: niagara-slime-v2")
    
    # 更新原始文章引用
    for v2_id, original_id in [
        ('niagara-decal-v2', '3afcd990447d'),
        ('niagara-postprocess-v2', '514c7a61d0d8'),
        ('niagara-slime-v2', '338c49bf45db')
    ]:
        if original_id in data['articles']:
            data['articles'][original_id]['v2Version'] = v2_id
            print(f"✅ 已更新 {original_id} 的 v2Version 引用")
    
    # 更新元数据
    if new_articles:
        data['meta']['lastUpdated'] = '2026-03-19 18:25'
        data['meta']['totalArticles'] = len(data['articles'])
        data['meta']['version'] = '6.4'
        data['meta']['newArticles'] = new_articles
    
    return data, new_articles

if __name__ == "__main__":
    print("=== 添加所有 Niagara V2 文章 ===\n")
    data = load_kb()
    data, new_articles = add_all_niagara_v2(data)
    save_kb(data)
    print(f"\n✅ 完成！新增 {len(new_articles)} 篇文章")
    for aid in new_articles:
        print(f"   - {aid}")
