#!/usr/bin/env python3
"""
使用Kimi AI生成深度分析的自动更新脚本
"""

import json
import feedparser
import hashlib
import os
import re
import requests
from datetime import datetime

KIMI_API_KEY = os.environ.get('KIMI_API_KEY', '')
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

WORKSPACE = "."
SOURCES_FILE = f"{WORKSPACE}/data/sources.json"
ARTICLES_FILE = f"{WORKSPACE}/data/articles.json"
KB_FILE = f"{WORKSPACE}/knowledge-base.js"

def generate_with_kimi(title, summary, category):
    """使用Kimi生成深度分析"""
    if not KIMI_API_KEY:
        print("  ⚠️  未配置Kimi API，使用本地生成")
        return None
    
    category_names = {
        "ue": "Unreal Engine",
        "ta": "技术美术", 
        "render": "实时渲染",
        "ta-render": "TA渲染",
        "ai": "AI技术"
    }
    
    prompt = f"""你是一位资深游戏技术专家。请分析以下技术文章并返回JSON格式：

标题: {title}
摘要: {summary[:500]}
领域: {category_names.get(category, '技术')}

返回格式（只返回JSON）：
{{
    "chinese_title": "中文标题（专业简洁）",
    "technical_summary": "技术摘要（200字中文）",
    "key_technologies": ["技术1", "技术2", "技术3"],
    "technical_analysis": "深度技术分析（400字中文，包含背景、问题、解决方案）",
    "practical_value": "实用价值（150字中文）",
    "target_audience": "目标读者",
    "difficulty": "简单/中等/困难"
}}"""
    
    try:
        headers = {
            "Authorization": f"Bearer {KIMI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "kimi-k2.5",  # Kimi2.5模型
            "messages": [
                {"role": "system", "content": "你是专业的游戏技术分析师，擅长深度技术文章解析。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(KIMI_API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return json.loads(content)
        else:
            print(f"  ⚠️  Kimi API错误: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ⚠️  Kimi调用失败: {e}")
        return None

# 其他函数与auto_fetch.py相同...
# [这里包含之前auto_fetch.py的load_sources, load_existing_articles等函数]

print("Kimi AI自动更新脚本已准备")
print("需要配置KIMI_API_KEY环境变量")
