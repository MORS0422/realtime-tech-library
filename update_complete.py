#!/usr/bin/env python3
import json
import re
from datetime import datetime

exec(open('data/supplement_articles.py').read())

with open('knowledge-base.js', 'r') as f:
    content = f.read()

match = re.search(r'articles:\s*({.*?}),\s*currentCategory', content, re.DOTALL)
articles = json.loads(match.group(1))

print(f"当前文章数: {len(articles)}")

# 1. 更新FFT水体
today = datetime.now().strftime('%Y-%m-%d')
fft_data = fft_water_full
articles['water-interaction'] = {
    'title': fft_data['chinese_title'],
    'category': 'ta-render',
    'tags': fft_data['key_technologies'][:3],
    'date': fft_data['date'],
    'author': 'Realtime Tech深度分析',
    'readTime': '20分钟',
    'difficulty': fft_data['difficulty'],
    'content': '<div class="article-content"><div class="flex flex-wrap items-center gap-3 mb-6"><span class="tag-ta-render px-3 py-1 rounded-full text-sm">TA渲染专栏</span><span class="text-gray-500">' + fft_data['date'] + '</span><span class="text-gray-500">•</span><span class="text-gray-500">20分钟阅读</span></div><h1>' + fft_data['chinese_title'] + '</h1><p class="text-xl text-gray-300">' + fft_data['technical_summary'] + '</p><div class="source-box"><div class="flex items-center gap-2 mb-2"><svg class="w-4 h-4 text-neon-amber" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg><span class="text-neon-amber font-medium">参考资源</span></div><div class="text-sm text-gray-400"><div>• Tessendorf, J. (2001). "Simulating Ocean Water". SIGGRAPH Course Notes</div><div>• NVIDIA GPU Gems: Chapter 1. Effective Water Simulation</div></div></div><div class="tech-analysis-box" style="border-color: #00ff8840;"><div class="flex items-center gap-2 mb-4"><span class="text-lg font-semibold" style="color: #00ff88">🔬 深度技术分析</span></div><p class="mb-0 text-gray-300 leading-relaxed">' + fft_data['technical_analysis'] + '</p></div><h2>🎯 核心技术点</h2><ul class="space-y-2 text-gray-300"><li><strong>快速傅里叶变换(FFT)</strong></li><li><strong>Phillips频谱</strong></li><li><strong>GPU粒子模拟</strong></li><li><strong>次表面散射(SSS)</strong></li><li><strong>Flipbook流体</strong></li></ul><h2>💡 实用价值</h2><p>' + fft_data['practical_value'] + '</p><div class="bg-dark-700/50 rounded-xl p-6 mt-8 border-l-4" style="border-color: #00ff88"><p class="mb-0 text-gray-400"><strong style="color: #00ff88">💡 提示:</strong> 本文为Realtime Tech深度技术分析。如需完整Shader代码实现，请参考GPU Gems原文。</p></div></div>'
}

# 2. 添加实时渲染文章
for aid, data in render_articles.items():
    tech_tags = ''.join(['<span class="tag-render px-3 py-1 rounded-full text-sm">' + t + '</span>' for t in data['technologies']])
    articles[aid] = {
        'title': data['chinese_title'],
        'category': 'render',
        'tags': data['technologies'][:3],
        'date': today,
        'author': 'Realtime Tech / 实时渲染',
        'readTime': '10分钟',
        'difficulty': data['difficulty'],
        'content': '<div class="article-content"><div class="flex flex-wrap items-center gap-3 mb-6"><span class="tag-render px-3 py-1 rounded-full text-sm">实时渲染</span><span class="text-gray-500">' + today + '</span></div><h1>' + data['chinese_title'] + '</h1><p class="text-xl text-gray-300">' + data['summary'] + '</p><div class="tech-analysis-box" style="border-color: #ffbe0b40;"><div class="flex items-center gap-2 mb-4"><span class="text-lg font-semibold" style="color: #ffbe0b">🔬 技术分析</span></div><p class="mb-0 text-gray-300 leading-relaxed">' + data['analysis'] + '</p></div><h2>🎯 核心技术</h2><div class="flex flex-wrap gap-2 mb-6">' + tech_tags + '</div></div>'
    }

# 3. 添加AI技术文章
for aid, data in ai_articles.items():
    tech_tags = ''.join(['<span class="tag-ai px-3 py-1 rounded-full text-sm">' + t + '</span>' for t in data['technologies']])
    articles[aid] = {
        'title': data['chinese_title'],
        'category': 'ai',
        'tags': data['technologies'][:3],
        'date': today,
        'author': 'Realtime Tech / AI技术',
        'readTime': '10分钟',
        'difficulty': data['difficulty'],
        'content': '<div class="article-content"><div class="flex flex-wrap items-center gap-3 mb-6"><span class="tag-ai px-3 py-1 rounded-full text-sm">AI技术</span><span class="text-gray-500">' + today + '</span></div><h1>' + data['chinese_title'] + '</h1><p class="text-xl text-gray-300">' + data['summary'] + '</p><div class="tech-analysis-box" style="border-color: #ff006e40;"><div class="flex items-center gap-2 mb-4"><span class="text-lg font-semibold" style="color: #ff006e">🔬 技术分析</span></div><p class="mb-0 text-gray-300 leading-relaxed">' + data['analysis'] + '</p></div><h2>🎯 核心技术</h2><div class="flex flex-wrap gap-2 mb-6">' + tech_tags + '</div></div>'
    }

print(f"更新后总数: {len(articles)}")

# 统计
categories = {}
for article in articles.values():
    cat = article.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

print("\n分类统计:")
for cat, count in sorted(categories.items()):
    name = {'ue': 'UE', 'ta': 'TA', 'ta-render': 'TA渲染', 'render': '实时渲染', 'ai': 'AI技术'}.get(cat, cat)
    print(f"  {name}: {count}篇")

# 重建知识库
meta = {
    "lastUpdated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "totalArticles": len(articles),
    "autoGenerated": True,
    "version": "4.1-complete"
}

js_content = '''// Realtime Tech Knowledge Base - Complete Version
const knowledgeBase = {
    meta: ''' + json.dumps(meta, indent=4) + ''',
    articles: ''' + json.dumps(articles, ensure_ascii=False, indent=4) + ''',
    currentCategory: 'home',
    getArticle(id) { return this.articles[id] || { title: '文章不存在', content: '<div class="text-center py-12"><h2>找不到该文章</h2></div>' }; },
    getArticlesByCategory(category) { return Object.entries(this.articles).filter(([id, a]) => a.category === category).map(([id, a]) => ({ id, ...a })); }
};
function showPage(pageId) { document.querySelectorAll('.page').forEach(p => p.classList.remove('active')); const t = document.getElementById('page-' + pageId); if (t) { if (['ue','ta','render','ta-render','ai'].includes(pageId)) loadCategoryPage(pageId); t.classList.add('active'); } if (pageId !== 'article') knowledgeBase.currentCategory = pageId; document.getElementById('mobile-menu').classList.add('hidden'); window.scrollTo(0, 0); }
function loadCategoryPage(category) { const page = document.getElementById('page-' + category); const articles = knowledgeBase.getArticlesByCategory(category); const names = {'ue':'Unreal Engine','ta':'技术美术','render':'实时渲染','ta-render':'TA渲染专栏','ai':'AI技术'}; const classes = {'ue':'tag-ue','ta':'tag-ta','render':'tag-render','ta-render':'tag-ta-render','ai':'tag-ai'}; let html = articles.map(a => `<div onclick="showArticle('${a.id}')" class="glass-panel rounded-2xl p-6 card-hover cursor-pointer"><div class="flex items-center gap-2 mb-3"><span class="${classes[category]} px-2 py-1 rounded text-xs">${a.tags[0]}</span><span class="text-gray-500 text-xs">${a.readTime}</span><span class="text-gray-500 text-xs">•</span><span class="text-gray-500 text-xs">${a.difficulty}</span></div><h3 class="text-xl font-semibold text-white mb-2">${a.title}</h3><p class="text-gray-400 text-sm">${a.author} · ${a.date}</p></div>`).join(''); if (articles.length === 0) html = '<div class="glass-panel rounded-2xl p-12 text-center"><h3>该分类暂无文章</h3></div>'; page.innerHTML = `<div class="py-12 px-6"><div class="max-w-7xl mx-auto"><div class="flex items-center gap-4 mb-8"><button onclick="showPage('home')" class="flex items-center gap-2 px-4 py-2 rounded-lg glass-panel hover:bg-white/5"><i data-lucide="home" class="w-5 h-5"></i><span>回到主页</span></button><div><h2 class="text-3xl font-bold ${category === 'ta-render' ? 'text-neon-green' : 'text-white'}">${names[category]}</h2><p class="text-gray-500">共 ${articles.length} 篇技术文章</p></div></div><div class="grid grid-cols-1 md:grid-cols-2 gap-6">${html}</div></div></div>`; }
function showArticle(id) { const a = knowledgeBase.getArticle(id); const p = document.getElementById('page-article'); p.innerHTML = `<div class="py-12 px-6"><div class="max-w-4xl mx-auto"><button onclick="backToCategory()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-6"><i data-lucide="arrow-left" class="w-5 h-5"></i><span>返回分类</span></button><div class="glass-panel rounded-3xl p-8 md:p-12">${a.content}</div></div></div>`; showPage('article'); if (typeof lucide !== 'undefined') lucide.createIcons(); }
function backToCategory() { if (knowledgeBase.currentCategory && knowledgeBase.currentCategory !== 'home') showPage(knowledgeBase.currentCategory); else showPage('home'); }
function toggleMobileMenu() { document.getElementById('mobile-menu').classList.toggle('hidden'); }
document.addEventListener('DOMContentLoaded', function() { if (typeof lucide !== 'undefined') lucide.createIcons(); const t = document.getElementById('last-update-time'); if (t) t.textContent = knowledgeBase.meta.lastUpdated; });
'''

with open('knowledge-base.js', 'w') as f:
    f.write(js_content)

print("\n✅ 知识库已更新！")
