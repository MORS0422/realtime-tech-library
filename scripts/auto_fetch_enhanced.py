#!/usr/bin/env python3
"""
全自动更新脚本 - 确保每个分类至少2篇文章
自动抓取RSS + 生成中文分析 + 更新知识库 + 分类均衡
"""

import json
import feedparser
import hashlib
import os
import re
from datetime import datetime, timedelta

WORKSPACE = "."
SOURCES_FILE = f"{WORKSPACE}/data/sources.json"
ARTICLES_FILE = f"{WORKSPACE}/data/articles.json"
KB_FILE = f"{WORKSPACE}/knowledge-base.js"

CATEGORY_CONFIG = {
    "ue": {"name": "Unreal Engine", "color": "#00f0ff"},
    "ta": {"name": "技术美术", "color": "#b026ff"},
    "render": {"name": "实时渲染", "color": "#ffbe0b"},
    "ta-render": {"name": "TA渲染专栏", "color": "#00ff88"},
    "ai": {"name": "AI技术", "color": "#ff006e"},
    "vfx": {"name": "特效专栏", "color": "#ff6600"},
    "multiplat": {"name": "多端开发", "color": "#00ccff"}
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

def parse_date(date_str):
    """解析各种日期格式"""
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str[:26], fmt)
        except:
            continue
    return datetime.now()

def should_include_article(article, settings, existing_ids):
    """过滤文章"""
    if article['id'] in existing_ids:
        return False
    
    title = article.get('title', '').lower()
    summary = article.get('summary', '').lower()
    
    # 排除Unity文章
    exclude_keywords = settings.get('exclude_keywords', [])
    for keyword in exclude_keywords:
        if keyword.lower() in title or keyword.lower() in summary:
            print(f"    ⏭️  跳过(Unity): {article['title'][:50]}...")
            return False
    
    # 检测UE相关内容并自动分类
    ue_keywords = ['unreal', 'ue5', 'ue4', 'niagara', 'lumen', 'nanite', 'epic games']
    if any(kw in title.lower() or kw in summary.lower() for kw in ue_keywords):
        if article['category'] != 'ue':
            article['category'] = 'ue'
            print(f"    ⭐ 自动归类为UE: {article['title'][:40]}...")
    
    # 检测AI相关内容
    ai_keywords = ['ai ', 'artificial intelligence', 'machine learning', 'neural', 'deep learning', 'generative', 'gpt', 'llm']
    if any(kw in title.lower() or kw in summary.lower() for kw in ai_keywords):
        if article['category'] != 'ai':
            article['category'] = 'ai'
            print(f"    🤖 自动归类为AI: {article['title'][:40]}...")
    
    # 检测渲染相关内容
    render_keywords = ['rendering', 'ray tracing', 'global illumination', 'pbr', 'shader', 'graphics']
    if any(kw in title.lower() or kw in summary.lower() for kw in render_keywords):
        if article['category'] not in ['render', 'ta-render']:
            article['category'] = 'render'
            print(f"    🎨 自动归类为渲染: {article['title'][:40]}...")
    
    return True

def is_recent_article(article, days_back=3):
    """检查文章是否在指定天数内"""
    try:
        pub_date = parse_date(article.get('published', ''))
        cutoff = datetime.now() - timedelta(days=days_back)
        return pub_date >= cutoff
    except:
        return True  # 如果解析失败，默认保留

def generate_analysis(article, category):
    """生成文章分析"""
    title = article['title']
    summary = clean_html(article.get('summary', ''))
    
    # 标题翻译
    translations = {
        'Unreal Engine': '虚幻引擎',
        'UE5': 'UE5',
        'UE4': 'UE4',
        'Nanite': 'Nanite',
        'Lumen': 'Lumen',
        'Niagara': 'Niagara',
        'Tutorial': '教程',
        'Guide': '指南',
        'Release': '发布',
        'Update': '更新',
        'Deep Learning': '深度学习',
        'Machine Learning': '机器学习',
        'Neural': '神经网络',
        'Rendering': '渲染',
        'Ray Tracing': '光线追踪',
        'Global Illumination': '全局光照'
    }
    
    chinese_title = title
    for en, cn in translations.items():
        chinese_title = chinese_title.replace(en, cn)
    
    # 各分类分析模板
    category_templates = {
        "ue": {
            "summary": f"本文介绍了虚幻引擎相关的最新技术进展。{summary[:200] if summary else '详细探讨了UE5引擎的新功能和优化技巧。'}",
            "technologies": ["虚幻引擎5", "渲染优化", "游戏开发", "Niagara粒子系统"],
            "analysis": f"虚幻引擎作为行业主流游戏引擎，持续在渲染技术、工具链和工作流程上创新。{summary[:150] if summary else '本文涉及的技术方案对游戏开发者具有重要参考价值。'}",
            "audience": "中级UE开发者",
            "difficulty": "中等"
        },
        "ta": {
            "summary": f"本文探讨了技术美术领域的实用技巧。{summary[:200] if summary else '分享了TA工作中的最佳实践。'}",
            "technologies": ["技术美术", "Shader开发", "材质系统", "工具开发"],
            "analysis": f"技术美术是连接程序和美术的桥梁。{summary[:150] if summary else '本文介绍的方法可以帮助TA团队更高效地完成工作。'}",
            "audience": "技术美术师",
            "difficulty": "中等"
        },
        "ta-render": {
            "summary": f"本文分享了特效制作的实战经验。{summary[:200] if summary else '展示了渲染和特效优化的具体案例。'}",
            "technologies": ["视觉特效", "渲染优化", "实时渲染", "Niagara"],
            "analysis": f"视觉特效是提升游戏沉浸感的关键。{summary[:150] if summary else '本文介绍的技巧可以帮助在保持高质量的同时控制好性能开销。'}",
            "audience": "特效师",
            "difficulty": "中等"
        },
        "render": {
            "summary": f"本文深入探讨了实时渲染技术的最新进展。{summary[:200] if summary else '涵盖了图形学算法和渲染管线的优化方案。'}",
            "technologies": ["实时渲染", "图形学算法", "光线追踪", "PBR材质"],
            "analysis": f"实时渲染技术是游戏和影视行业的核心。{summary[:150] if summary else '本文涉及的技术方案代表了当前图形学领域的前沿方向。'}",
            "audience": "渲染工程师",
            "difficulty": "困难"
        },
        "ai": {
            "summary": f"本文介绍了AI技术在游戏开发中的最新应用。{summary[:200] if summary else '探讨了机器学习和神经网络在实时渲染中的创新应用。'}",
            "technologies": ["机器学习", "神经网络", "生成式AI", "AI辅助开发"],
            "analysis": f"AI正在深刻改变游戏开发的工作流程。{summary[:150] if summary else '本文展示的技术代表了AI与游戏结合的最新趋势。'}",
            "audience": "AI工程师/技术美术",
            "difficulty": "困难"
        }
    }
    
    config = category_templates.get(category, category_templates["ta"])
    
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

def fetch_rss_source(source, max_articles=5):
    """抓取RSS源"""
    articles = []
    try:
        print(f"  抓取: {source['name']}...")
        feed = feedparser.parse(source['url'])
        count = 0
        
        for entry in feed.entries[:max_articles * 2]:  # 多抓一些用于过滤
            if count >= max_articles:
                break
                
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
            count += 1
        
        print(f"  ✓ {len(articles)} 篇")
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    
    return articles

def parse_knowledge_base():
    """解析知识库文件，返回 articles 字典"""
    with open(KB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尝试多种方式解析
    # 方式1: 匹配 "articles": { ... } 结构（新格式）
    match = re.search(r'"articles":\s*({.*})\s*}\s*;?\s*$', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print(f"  方式1解析失败: {e}")
    
    # 方式2: 匹配 articles: { ... }, currentCategory 结构（旧格式）
    match = re.search(r'"?articles"?\s*:\s*({.*?}),\s*"?currentCategory"?', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print(f"  方式2解析失败: {e}")
    
    # 方式3: 尝试提取整个 knowledgeBase 对象
    match = re.search(r'const\s+knowledgeBase\s*=\s*({.*?});\s*$', content, re.DOTALL)
    if match:
        try:
            # 这是一个JavaScript对象，不是标准JSON，需要处理
            kb_text = match.group(1)
            # 尝试提取 articles 部分
            articles_match = re.search(r'"articles":\s*({(?:[^{}]|{(?:[^{}]|{[^{}]*})*})*})', kb_text, re.DOTALL)
            if articles_match:
                return json.loads(articles_match.group(1))
        except Exception as e:
            print(f"  方式3解析失败: {e}")
    
    print("❌ 无法解析知识库 - 所有方式都失败")
    return None

def update_knowledge_base(new_articles):
    """更新知识库"""
    # 解析现有知识库
    articles = parse_knowledge_base()
    if articles is None:
        # 如果解析失败，尝试使用已存在的文章
        articles = {}
        print("⚠️ 解析失败，将创建新的知识库")
    
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
        "version": "4.1-enhanced"
    }
    
    js_content = f'''// Realtime Tech Knowledge Base - Enhanced Auto Generated
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
    print("🤖 Realtime Tech 增强版全自动更新")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    config = load_sources()
    sources = config.get('sources', [])
    settings = config.get('settings', {})
    
    max_per_source = settings.get('max_articles_per_source', 5)
    min_per_category = settings.get('min_articles_per_category', 2)
    fetch_days = settings.get('fetch_days_back', 3)
    
    existing_articles = load_existing_articles()
    existing_ids = set(existing_articles.keys())
    print(f"\n现有文章: {len(existing_articles)} 篇")
    
    # 按分类分组抓取
    category_articles = {cat: [] for cat in CATEGORY_CONFIG.keys()}
    
    for source in sources:
        if not source.get('enabled', True):
            continue
        
        fetched = fetch_rss_source(source, max_per_source)
        
        for article in fetched:
            if should_include_article(article, settings, existing_ids):
                if is_recent_article(article, fetch_days):
                    cat = article['category']
                    if cat in category_articles:
                        category_articles[cat].append(article)
                    else:
                        category_articles['ta'].append(article)
    
    # 统计各分类文章数
    print("\n📊 各分类新文章统计:")
    for cat, articles in category_articles.items():
        print(f"  {CATEGORY_CONFIG[cat]['name']}: {len(articles)}篇")
    
    # 确保每个分类至少有min_per_category篇文章
    final_articles = []
    for cat, articles in category_articles.items():
        count = len(articles)
        if count >= min_per_category:
            # 如果超过，按时间排序取最新的
            sorted_articles = sorted(articles, key=lambda x: x.get('published', ''), reverse=True)
            final_articles.extend(sorted_articles[:min_per_category + 2])  # 多留2篇冗余
        else:
            # 如果不足，全部保留（后面会提示）
            final_articles.extend(articles)
    
    print(f"\n📝 最终选取: {len(final_articles)} 篇")
    
    # 分类统计
    final_by_category = {cat: 0 for cat in CATEGORY_CONFIG.keys()}
    for article in final_articles:
        cat = article.get('category', 'ta')
        if cat in final_by_category:
            final_by_category[cat] += 1
    
    print("\n📈 各分类最终数量:")
    for cat, count in final_by_category.items():
        status = "✅" if count >= min_per_category else "⚠️"
        print(f"  {status} {CATEGORY_CONFIG[cat]['name']}: {count}篇 (目标: {min_per_category}篇)")
    
    if final_articles:
        # 生成分析和更新知识库
        processed = {}
        for article in final_articles:
            print(f"\n处理: {article['title'][:50]}...")
            analysis = generate_analysis(article, article['category'])
            processed[article['id']] = {
                'article': article,
                'analysis': analysis
            }
            existing_articles[article['id']] = article
        
        print("\n💾 更新知识库...")
        if update_knowledge_base(processed):
            save_articles(existing_articles)
            print(f"\n✅ 成功添加 {len(processed)} 篇新文章")
            
            # 更新统计
            print("\n📊 更新后各分类统计:")
            articles = parse_knowledge_base()
            if articles:
                cat_counts = {cat: 0 for cat in CATEGORY_CONFIG.keys()}
                for aid, article in articles.items():
                    cat = article.get('category', 'ta')
                    if cat in cat_counts:
                        cat_counts[cat] += 1
                
                for cat, count in cat_counts.items():
                    print(f"  {CATEGORY_CONFIG[cat]['name']}: {count}篇")
        else:
            print("❌ 更新失败")
    else:
        print("\n✓ 没有新文章")
    
    print("="*60)

if __name__ == "__main__":
    main()
