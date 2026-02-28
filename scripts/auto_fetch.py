#!/usr/bin/env python3
"""
全自动更新脚本 - 用于GitHub Actions
自动抓取RSS + 生成中文分析 + 更新知识库
"""

import json
import feedparser
import hashlib
import os
import re
from datetime import datetime

WORKSPACE = "."
SOURCES_FILE = f"{WORKSPACE}/data/sources.json"
ARTICLES_FILE = f"{WORKSPACE}/data/articles.json"
KB_FILE = f"{WORKSPACE}/knowledge-base.js"

CATEGORY_CONFIG = {
    "ue": {"name": "Unreal Engine", "color": "#00f0ff"},
    "ta": {"name": "技术美术", "color": "#b026ff"},
    "render": {"name": "实时渲染", "color": "#ffbe0b"},
    "ta-render": {"name": "TA渲染专栏", "color": "#00ff88"},
    "ai": {"name": "AI技术", "color": "#ff006e"}
}

def load_sources():
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_existing_articles():
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_articles(articles):
    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def generate_article_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:12]

def clean_html(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def should_include_article(article, settings):
    """过滤Unity文章"""
    title = article.get('title', '').lower()
    summary = article.get('summary', '').lower()
    
    exclude_keywords = settings.get('exclude_keywords', [])
    for keyword in exclude_keywords:
        if keyword.lower() in title or keyword.lower() in summary:
            print(f"    ⏭️  跳过(Unity): {article['title'][:50]}...")
            return False
    
    # 检测UE相关内容
    ue_keywords = ['unreal', 'ue5', 'ue4', 'niagara', 'lumen', 'nanite']
    if any(kw in title.lower() or kw in summary.lower() for kw in ue_keywords):
        article['category'] = 'ue'
        print(f"    ⭐ 发现UE内容")
    
    return True

def generate_simple_analysis(article):
    """生成简化版中文分析（无AI，本地规则）"""
    title = article['title']
    summary = clean_html(article.get('summary', ''))
    category = article['category']
    
    # 简单的标题翻译规则
    translations = {
        'Unreal Engine': '虚幻引擎',
        'UE5': '虚幻引擎5',
        'Nanite': 'Nanite虚拟几何体',
        'Lumen': 'Lumen全局光照',
        'Niagara': 'Niagara粒子系统',
        'Tutorial': '教程',
        'Guide': '指南',
        'Release': '发布',
        'Update': '更新'
    }
    
    chinese_title = title
    for en, cn in translations.items():
        chinese_title = chinese_title.replace(en, cn)
    
    # 根据分类生成技术分析
    category_analysis = {
        "ue": {
            "summary": f"本文介绍了虚幻引擎相关的最新技术进展。{summary[:200] if summary else '详细探讨了UE5引擎的新功能和优化技巧。'}",
            "technologies": ["虚幻引擎5", "渲染优化", "游戏开发"],
            "analysis": f"虚幻引擎作为行业主流游戏引擎，持续在渲染技术、工具链和工作流程上创新。本文涉及的技术方案对游戏开发者具有重要参考价值，可以帮助更好地利用UE5的特性。",
            "audience": "中级UE开发者",
            "difficulty": "中等"
        },
        "ta": {
            "summary": f"本文探讨了技术美术领域的实用技巧。{summary[:200] if summary else '分享了TA工作中的最佳实践。'}",
            "technologies": ["技术美术", "Shader开发", "材质系统"],
            "analysis": "技术美术是连接程序和美术的桥梁。本文介绍的方法可以帮助TA团队更高效地完成资产制作和引擎集成工作。",
            "audience": "技术美术师",
            "difficulty": "中等"
        },
        "ta-render": {
            "summary": f"本文分享了特效制作的实战经验。{summary[:200] if summary else '展示了渲染和特效优化的具体案例。'}",
            "technologies": ["视觉特效", "渲染优化", "实时渲染"],
            "analysis": "视觉特效是提升游戏沉浸感的关键。本文介绍的技巧可以帮助在保持高质量的同时控制好性能开销。",
            "audience": "特效师",
            "difficulty": "中等"
        }
    }
    
    config = category_analysis.get(category, category_analysis["ta"])
    
    return {
        "chinese_title": chinese_title,
        "technical_summary": config["summary"],
        "key_technologies": config["technologies"],
        "technical_analysis": config["analysis"],
        "practical_value": "提升工作效率，优化项目质量",
        "related_topics": ["相关技术", "最佳实践"],
        "target_audience": config["audience"],
        "implementation_difficulty": config["difficulty"]
    }

def generate_content_html(article, analysis):
    """生成文章HTML"""
    title = analysis['chinese_title']
    summary = analysis['technical_summary']
    tech_analysis = analysis['technical_analysis']
    technologies = analysis['key_technologies']
    link = article.get('link', '')
    published = article.get('published', datetime.now().strftime('%Y-%m-%d'))[:10]
    source = article.get('source_name', '未知来源')
    category = article.get('category', 'ta')
    
    config = CATEGORY_CONFIG.get(category, CATEGORY_CONFIG['ta'])
    tag_class = f"tag-{category}"
    
    tech_tags = ''.join([f'<span class="{tag_class} px-3 py-1 rounded-full text-sm">{tech}</span>' for tech in technologies])
    
    html = f'''<div class="article-content">
    <div class="flex flex-wrap items-center gap-3 mb-6">
        <span class="{tag_class} px-3 py-1 rounded-full text-sm">{config['name']}</span>
        <span class="text-gray-500">{published}</span>
        <span class="text-gray-500">•</span>
        <span class="text-gray-500">{analysis['target_audience']}</span>
    </div>
    <h1>{title}</h1>
    <p class="text-xl text-gray-300 mb-6">{summary}</p>
    <div class="source-box">
        <div class="flex items-center gap-2 mb-2">
            <svg class="w-4 h-4 text-neon-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
            </svg>
            <span class="text-neon-amber font-medium">原文链接</span>
        </div>
        <div class="text-sm text-gray-400">
            <div>• <a href="{link}" target="_blank" class="text-neon-blue hover:underline">{source} - 查看完整原文</a></div>
        </div>
    </div>
    <div class="tech-analysis-box" style="border-color: {config['color']}40;">
        <div class="flex items-center gap-2 mb-4">
            <span class="text-lg font-semibold" style="color: {config['color']}">🔬 技术分析</span>
        </div>
        <p class="mb-0 text-gray-300 leading-relaxed">{tech_analysis}</p>
    </div>
    <h2>🎯 核心技术点</h2>
    <div class="flex flex-wrap gap-2 mb-6">{tech_tags}</div>
    <div class="bg-dark-700/50 rounded-xl p-6 mt-8 border-l-4" style="border-color: {config['color']}">
        <p class="mb-0 text-gray-400">
            <strong style="color: {config['color']}">💡 提示:</strong> 
            本文为自动抓取生成的中文摘要。如需完整技术细节，请点击上方原文链接。
        </p>
    </div>
</div>'''
    return html

def fetch_rss_source(source):
    """抓取RSS源"""
    articles = []
    try:
        print(f"  抓取: {source['name']}...")
        feed = feedparser.parse(source['url'])
        max_articles = source.get('max_articles', 3)  # 减少数量避免过多
        
        for entry in feed.entries[:max_articles]:
            article_id = generate_article_id(entry.get('link', ''))
            published = entry.get('published', '') or entry.get('updated', datetime.now().strftime('%Y-%m-%d'))
            summary = entry.get('summary', '')
            if not summary and 'content' in entry:
                summary = entry.content[0].value
            
            article = {
                'id': article_id,
                'title': entry.get('title', '无标题'),
                'link': entry.get('link', ''),
                'summary': clean_html(summary),
                'published': published,
                'source_name': source['name'],
                'category': source['category'],
                'fetched_at': datetime.now().isoformat()
            }
            articles.append(article)
        
        print(f"  ✓ {len(articles)} 篇")
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    
    return articles

def update_knowledge_base(new_articles):
    """更新知识库"""
    # 读取现有知识库
    with open(KB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'articles:\s*({.*?}),\s*currentCategory', content, re.DOTALL)
    if not match:
        print("❌ 无法解析知识库")
        return False
    
    articles = json.loads(match.group(1))
    
    # 添加新文章
    for article_id, article_data in new_articles.items():
        if article_id not in articles:
            article = article_data['article']
            analysis = article_data['analysis']
            config = CATEGORY_CONFIG.get(article['category'], CATEGORY_CONFIG['ta'])
            
            articles[article_id] = {
                'title': analysis['chinese_title'],
                'category': article['category'],
                'tags': analysis['key_technologies'],
                'date': article.get('published', datetime.now().strftime('%Y-%m-%d'))[:10],
                'author': f"{article['source_name']} / 自动摘要",
                'readTime': '5分钟',
                'difficulty': analysis['implementation_difficulty'],
                'content': generate_content_html(article, analysis)
            }
            print(f"  + 添加: {analysis['chinese_title'][:40]}...")
    
    # 重新构建知识库
    meta = {
        "lastUpdated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "totalArticles": len(articles),
        "autoGenerated": True,
        "version": "4.0-auto"
    }
    
    js_content = f'''// Realtime Tech Knowledge Base - Auto Generated
const knowledgeBase = {{
    meta: {json.dumps(meta, indent=4)},
    articles: {json.dumps(articles, ensure_ascii=False, indent=4)},
    currentCategory: 'home',
    getArticle(id) {{ return this.articles[id] || {{ title: '文章不存在', content: '<div class="text-center py-12"><h2>找不到该文章</h2></div>' }}; }},
    getArticlesByCategory(category) {{ return Object.entries(this.articles).filter(([id, a]) => a.category === category).map(([id, a]) => ({{ id, ...a }})); }}
}};
function showPage(pageId) {{ document.querySelectorAll('.page').forEach(p => p.classList.remove('active')); const t = document.getElementById('page-' + pageId); if (t) {{ if (['ue','ta','render','ta-render','ai'].includes(pageId)) loadCategoryPage(pageId); t.classList.add('active'); }} if (pageId !== 'article') knowledgeBase.currentCategory = pageId; document.getElementById('mobile-menu').classList.add('hidden'); window.scrollTo(0, 0); }}
function loadCategoryPage(category) {{ const page = document.getElementById('page-' + category); const articles = knowledgeBase.getArticlesByCategory(category); const names = {{'ue':'Unreal Engine','ta':'技术美术','render':'实时渲染','ta-render':'TA渲染专栏','ai':'AI技术'}}; const classes = {{'ue':'tag-ue','ta':'tag-ta','render':'tag-render','ta-render':'tag-ta-render','ai':'tag-ai'}}; let html = articles.map(a => `<div onclick="showArticle('${{a.id}}')" class="glass-panel rounded-2xl p-6 card-hover cursor-pointer"><div class="flex items-center gap-2 mb-3"><span class="${{classes[category]}} px-2 py-1 rounded text-xs">${{a.tags[0]}}</span><span class="text-gray-500 text-xs">${{a.readTime}}</span><span class="text-gray-500 text-xs">•</span><span class="text-gray-500 text-xs">${{a.difficulty}}</span></div><h3 class="text-xl font-semibold text-white mb-2">${{a.title}}</h3><p class="text-gray-400 text-sm">${{a.author}} · ${{a.date}}</p></div>`).join(''); if (articles.length === 0) html = '<div class="glass-panel rounded-2xl p-12 text-center"><h3>该分类暂无文章</h3></div>'; page.innerHTML = `<div class="py-12 px-6"><div class="max-w-7xl mx-auto"><div class="flex items-center gap-4 mb-8"><button onclick="showPage('home')" class="flex items-center gap-2 px-4 py-2 rounded-lg glass-panel hover:bg-white/5"><i data-lucide="home" class="w-5 h-5"></i><span>回到主页</span></button><div><h2 class="text-3xl font-bold ${{category === 'ta-render' ? 'text-neon-green' : 'text-white'}}">${{names[category]}}</h2><p class="text-gray-500">共 ${{articles.length}} 篇技术文章</p></div></div><div class="grid grid-cols-1 md:grid-cols-2 gap-6">${{html}}</div></div></div>`; }}
function showArticle(id) {{ const a = knowledgeBase.getArticle(id); const p = document.getElementById('page-article'); p.innerHTML = `<div class="py-12 px-6"><div class="max-w-4xl mx-auto"><button onclick="backToCategory()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-6"><i data-lucide="arrow-left" class="w-5 h-5"></i><span>返回分类</span></button><div class="glass-panel rounded-3xl p-8 md:p-12">${{a.content}}</div></div></div>`; showPage('article'); if (typeof lucide !== 'undefined') lucide.createIcons(); }}
function backToCategory() {{ if (knowledgeBase.currentCategory && knowledgeBase.currentCategory !== 'home') showPage(knowledgeBase.currentCategory); else showPage('home'); }}
function toggleMobileMenu() {{ document.getElementById('mobile-menu').classList.toggle('hidden'); }}
document.addEventListener('DOMContentLoaded', function() {{ if (typeof lucide !== 'undefined') lucide.createIcons(); const t = document.getElementById('last-update-time'); if (t) t.textContent = knowledgeBase.meta.lastUpdated; }});
'''
    
    with open(KB_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    return True

def main():
    print("="*60)
    print("🤖 Realtime Tech 全自动更新")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    config = load_sources()
    sources = config.get('sources', [])
    settings = config.get('settings', {})
    
    existing_articles = load_existing_articles()
    print(f"\n现有文章: {len(existing_articles)} 篇")
    
    # 抓取新文章
    new_articles = []
    for source in sources:
        if not source.get('enabled', True):
            continue
        
        source['max_articles'] = settings.get('max_articles_per_source', 3)
        fetched = fetch_rss_source(source)
        
        for article in fetched:
            if article['id'] not in existing_articles:
                if should_include_article(article, settings):
                    new_articles.append(article)
    
    print(f"\n新发现: {len(new_articles)} 篇")
    
    if new_articles:
        # 生成分析和更新知识库
        processed = {}
        for article in new_articles:
            print(f"\n处理: {article['title'][:50]}...")
            analysis = generate_simple_analysis(article)
            processed[article['id']] = {
                'article': article,
                'analysis': analysis
            }
            existing_articles[article['id']] = article
        
        print("\n更新知识库...")
        if update_knowledge_base(processed):
            save_articles(existing_articles)
            print(f"✅ 已添加 {len(processed)} 篇新文章")
            print("知识库已更新，准备提交...")
        else:
            print("❌ 更新失败")
    else:
        print("\n✓ 没有新文章")
    
    print("="*60)

if __name__ == "__main__":
    main()
