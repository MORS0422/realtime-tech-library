// Realtime Tech Knowledge Base - 修复版
// 添加所有缺失的交互函数

// 页面路由函数
function showPage(pageId) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示目标页面
    const targetPage = document.getElementById('page-' + pageId);
    if (targetPage) {
        // 如果页面内容为空，生成内容
        if (!targetPage.innerHTML.trim() || pageId === 'home') {
            generatePageContent(pageId, targetPage);
        }
        targetPage.classList.add('active');
    }
    
    // 关闭移动端菜单
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.classList.add('hidden');
    }
    
    // 滚动到顶部
    window.scrollTo(0, 0);
}

// 生成页面内容
function generatePageContent(pageId, container) {
    if (pageId === 'home') {
        // 首页内容已在HTML中
        return;
    }
    
    if (pageId === 'article') {
        // 文章页面由 showArticle 处理
        return;
    }
    
    // 获取该分类的文章
    const articles = Object.entries(knowledgeBase.articles)
        .filter(([id, article]) => article.category === pageId)
        .map(([id, article]) => ({ ...article, id }));
    
    if (articles.length === 0) {
        container.innerHTML = `
            <div class="max-w-7xl mx-auto px-6 py-16 text-center">
                <h2 class="text-3xl font-bold text-white mb-4">暂无内容</h2>
                <p class="text-gray-400">该分类下暂时没有文章</p>
                <button onclick="showPage('home')" class="mt-8 px-6 py-3 bg-neon-blue text-white rounded-lg hover:bg-neon-blue/80 transition">
                    返回首页
                </button>
            </div>
        `;
        return;
    }
    
    // 分类标题映射
    const categoryTitles = {
        'ue': 'Unreal Engine',
        'ta': '技术美术',
        'render': '实时渲染',
        'ta-render': 'TA渲染',
        'vfx': '特效专栏',
        'multiplat': '多端开发',
        'ai': 'AI技术'
    };
    
    const categoryColors = {
        'ue': '#00f0ff',
        'ta': '#b026ff',
        'render': '#ffbe0b',
        'ta-render': '#00ff88',
        'vfx': '#ff6600',
        'multiplat': '#00ccff',
        'ai': '#ff006e'
    };
    
    const color = categoryColors[pageId] || '#00f0ff';
    const title = categoryTitles[pageId] || pageId;
    
    let html = `
        <div class="max-w-7xl mx-auto px-6 py-12">
            <h1 class="text-4xl font-bold mb-8" style="color: ${color}">${title}</h1>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    `;
    
    articles.forEach(article => {
        const tagClass = `tag-${article.category}`;
        html += `
            <div onclick="showArticle('${article.id}')" class="glass-panel rounded-2xl p-6 card-hover cursor-pointer">
                <div class="flex flex-wrap gap-2 mb-4">
                    <span class="${tagClass} px-3 py-1 rounded-full text-sm">${article.category.toUpperCase()}</span>
                </div>
                <h3 class="text-xl font-semibold text-white mb-3">${article.title}</h3>
                <p class="text-gray-400 text-sm mb-4">${article.date} · ${article.readTime}</p>
                <div class="flex flex-wrap gap-2">
                    ${article.tags.slice(0, 3).map(tag => `<span class="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded">${tag}</span>`).join('')}
                </div>
            </div>
        `;
    });
    
    html += '</div></div>';
    container.innerHTML = html;
}

// 显示文章详情
function showArticle(articleId) {
    const article = knowledgeBase.articles[articleId];
    if (!article) return;
    
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示文章页面
    const articlePage = document.getElementById('page-article');
    if (articlePage) {
        articlePage.innerHTML = `
            <div class="max-w-5xl mx-auto px-6 py-12">
                <button onclick="showPage('${article.category}')" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
                    返回列表
                </button>
                ${article.content}
            </div>
        `;
        articlePage.classList.add('active');
    }
    
    window.scrollTo(0, 0);
}

// 移动端菜单切换
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

// 初始化首页
function initHome() {
    const recentUpdatesList = document.getElementById('recent-updates-list');
    if (recentUpdatesList) {
        // 获取最近更新的文章
        const recentArticles = Object.entries(knowledgeBase.articles)
            .map(([id, article]) => ({ ...article, id }))
            .sort((a, b) => new Date(b.date) - new Date(a.date))
            .slice(0, 5);
        
        let html = '';
        recentArticles.forEach((article, index) => {
            const colors = ['bg-neon-green', 'bg-neon-blue', 'bg-neon-purple', 'bg-neon-pink', 'bg-neon-amber'];
            const color = colors[index % colors.length];
            html += `
                <div onclick="showArticle('${article.id}')" class="cursor-pointer flex items-center gap-4 p-4 border-b border-gray-800 last:border-0 hover:bg-white/5 transition">
                    <div class="w-2 h-2 rounded-full ${color}"></div>
                    <div class="flex-1">
                        <div class="text-white font-medium">${article.title}</div>
                        <div class="text-sm text-gray-500">${article.tags.slice(0, 2).join(', ')}</div>
                    </div>
                    <div class="text-sm text-gray-500">${article.date}</div>
                </div>
            `;
        });
        
        recentUpdatesList.innerHTML = html;
    }
    
    // 更新时间
    const timeElement = document.getElementById('last-update-time');
    if (timeElement && knowledgeBase.meta) {
        timeElement.textContent = knowledgeBase.meta.lastUpdated;
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initHome();
});

// 知识库数据
const knowledgeBase = { meta: {"lastUpdated": "2026-02-28 19:30", "totalArticles": 58, "autoGenerated": true, "version": "5.0"}, articles: {"ue57-release": {"title": "Unreal Engine 5.7 正式发布：完整技术分析", "category": "ue", "tags": ["Nanite Foliage", "MegaLights", "PCG", "Substrate"], "date": "2025-11-12", "author": "Epic Games / Realtime Tech深度分析", "readTime": "20分钟", "difficulty": "困难", "content": "...升级后的内容..."}, "water-interaction": {"title": "实时水体交互渲染：FFT海浪与流体模拟", "category": "ta-render", "tags": ["快速傅里叶变换(FFT)", "Phillips频谱", "GPU粒子模拟"], "date": "2025-02-26", "author": "Realtime Tech深度分析", "readTime": "20分钟", "difficulty": "高级", "content": "<div class=\"article-content\"><h1>实时水体交互渲染</h1><p>水体渲染内容...</p></div>"}, "ue55-nanite-foliage": {"title": "UE 5.5 Nanite Foliage 技术深度解析", "category": "ue", "tags": ["Nanite", "植被渲染", "GPU Driven"], "date": "2026-02-27", "author": "Realtime Tech", "readTime": "10分钟", "difficulty": "困难", "content": "<div class=\"article-content\"><h1>Nanite Foliage</h1><p>植被渲染技术...</p></div>"}}};
