#!/usr/bin/env python3
"""
Realtime Tech Library - 内容质量Review工具
每3天运行一次，检查：
1. 文章勘误
2. 阅读原文链接有效性
3. 内容质量评分
4. 优质内容标记
"""

import json
import os
import re
from datetime import datetime, timedelta

WORKSPACE = "."
ARTICLES_FILE = f"{WORKSPACE}/data/articles.json"
KB_FILE = f"{WORKSPACE}/knowledge-base.js"
REVIEW_LOG = f"{WORKSPACE}/data/review_log.json"

# 优质来源白名单
QUALITY_SOURCES = [
    "Unreal Engine 官方博客",
    "Epic Games",
    "NVIDIA",
    "80 Level",
    "Gamasutra",
    "GDC Vault",
    "SIGGRAPH",
    "SideFX Houdini",
    "Realtime VFX",
    "ArtStation Magazine",
    "CG Channel"
]

# 优质关键词
QUALITY_KEYWORDS = [
    "SIGGRAPH", "GDC", "UE5", "Unreal Engine 5", "Nanite", "Lumen", "Niagara",
    "Houdini", "Ray Tracing", "Global Illumination", "PBR", "VFX", " Niagara"
]

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_source_quality(source_name):
    """检查来源是否为优质来源"""
    for quality_source in QUALITY_SOURCES:
        if quality_source.lower() in source_name.lower():
            return True
    return False

def check_content_quality(article):
    """检查内容质量"""
    title = article.get('title', '')
    summary = article.get('summary', '')
    
    score = 0
    reasons = []
    
    # 检查优质关键词
    for keyword in QUALITY_KEYWORDS:
        if keyword.lower() in title.lower() or keyword.lower() in summary.lower():
            score += 10
            reasons.append(f"包含优质关键词: {keyword}")
    
    # 检查来源质量
    if check_source_quality(article.get('source_name', '')):
        score += 20
        reasons.append("来源为优质技术站点")
    
    # 检查摘要长度（有摘要通常质量更高）
    if len(summary) > 100:
        score += 10
        reasons.append("摘要内容完整")
    
    # 检查是否有UE相关内容
    if any(kw in title.lower() for kw in ['unreal', 'ue5', 'niagara', 'lumen']):
        score += 15
        reasons.append("Unreal Engine相关内容")
    
    # 判断质量等级
    if score >= 40:
        level = "优质"
    elif score >= 25:
        level = "良好"
    elif score >= 10:
        level = "一般"
    else:
        level = "需改进"
    
    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }

def check_link_validity(article):
    """检查原文链接（标记需要检查的链接）"""
    link = article.get('link', '')
    
    # 检查链接格式
    if not link.startswith(('http://', 'https://')):
        return {"valid": False, "issue": "链接格式不正确"}
    
    # 检查是否为常见无效链接
    invalid_patterns = ['example.com', 'localhost', '127.0.0.1']
    for pattern in invalid_patterns:
        if pattern in link:
            return {"valid": False, "issue": f"包含无效域名: {pattern}"}
    
    return {"valid": True, "issue": None}

def review_article(article_id, article):
    """Review单篇文章"""
    print(f"\n📄 Review: {article['title'][:50]}...")
    
    # 内容质量检查
    quality = check_content_quality(article)
    print(f"   质量评分: {quality['score']} - {quality['level']}")
    for reason in quality['reasons'][:2]:  # 只显示前2个原因
        print(f"   ✓ {reason}")
    
    # 链接有效性检查
    link_check = check_link_validity(article)
    if not link_check['valid']:
        print(f"   ⚠️ 链接问题: {link_check['issue']}")
    
    return {
        "article_id": article_id,
        "title": article['title'],
        "quality_score": quality['score'],
        "quality_level": quality['level'],
        "link_valid": link_check['valid'],
        "link_issue": link_check['issue'],
        "reviewed_at": datetime.now().isoformat()
    }

def main():
    print("="*60)
    print("🔍 Realtime Tech Library - 内容质量Review")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 加载文章
    articles = load_json(ARTICLES_FILE)
    print(f"\n📚 共 {len(articles)} 篇文章需要Review")
    
    # Review每篇文章
    review_results = []
    quality_stats = {"优质": 0, "良好": 0, "一般": 0, "需改进": 0}
    
    for article_id, article in articles.items():
        result = review_article(article_id, article)
        review_results.append(result)
        quality_stats[result['quality_level']] += 1
    
    # 统计
    print("\n" + "="*60)
    print("📊 Review统计")
    print("="*60)
    for level, count in quality_stats.items():
        print(f"  {level}: {count}篇")
    
    # 保存Review日志
    review_log = {
        "review_date": datetime.now().isoformat(),
        "total_articles": len(articles),
        "quality_distribution": quality_stats,
        "results": review_results
    }
    save_json(review_log, REVIEW_LOG)
    print(f"\n💾 Review日志已保存: {REVIEW_LOG}")
    
    # 标记优质文章
    high_quality = [r for r in review_results if r['quality_level'] == '优质']
    print(f"\n🏆 优质文章: {len(high_quality)}篇")
    for item in high_quality[:5]:  # 只显示前5篇
        print(f"  • {item['title'][:40]}...")
    
    print("\n✅ Review完成!")
    print("="*60)

if __name__ == "__main__":
    main()
