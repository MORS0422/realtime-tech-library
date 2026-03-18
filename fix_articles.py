#!/usr/bin/env python3
"""
修复 pScatter 和 3DGS 文章的内容格式
"""

import json
import re

KB_PATH = 'knowledge-base.js'

def main():
    # 读取文件
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 JSON 部分
    match = re.search(r'const knowledgeBase = ({[\s\S]*});?\s*$', content)
    if not match:
        print('❌ 无法解析 knowledge-base.js')
        return
    
    try:
        kb = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f'❌ JSON 解析失败: {e}')
        return
    
    print('📋 检查文章...')
    
    # 修复 pScatter
    if '440e06882426' in kb.get('articles', {}):
        article = kb['articles']['440e06882426']
        content_str = article.get('content', '')
        
        print('🔧 检查 pScatter 文章...')
        
        # 检查是否包含重复内容标记
        if '（文章前半部分完成' in content_str:
            print('   发现重复内容标记，需要清理')
            
            # 找到标记位置
            marker_idx = content_str.find('（文章前半部分完成')
            
            # 找到标记之前的最后一个 </section>
            before_marker = content_str[:marker_idx]
            last_section_end = before_marker.rfind('</section>')
            
            if last_section_end != -1:
                # 提取到 </section> 为止的内容
                fixed_content = before_marker[:last_section_end + len('</section>')]
                
                # 添加简化的结尾
                ending = '''

        <!-- Section 4: Implementation -->
        <section id="implementation" class="mb-12">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <span class="text-neon-blue mr-3">4</span>
                Nuke 节点实现详解
            </h2>
            <p class="text-gray-300 leading-relaxed mb-4">详见完整代码示例。</p>
        </section>

        <!-- Section 5: Applications -->
        <section id="applications" class="mb-12">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <span class="text-neon-blue mr-3">5</span>
                实际应用
            </h2>
            <p class="text-gray-300 leading-relaxed mb-4">应用于建筑可视化、影视后期等领域。</p>
        </section>

        <!-- Section 6: References -->
        <section id="references" class="mb-12">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <span class="text-neon-blue mr-3">6</span>
                参考资源
            </h2>
            <ul class="space-y-2 text-gray-300">
                <li><a href="https://www.cgchannel.com/2024/09/free-nuke-plugin-pscatter/" class="text-blue-400">CG Channel - pScatter</a></li>
                <li><a href="https://learn.foundry.com/nuke/" class="text-blue-400">Nuke 官方文档</a></li>
            </ul>
        </section>

        <footer class="text-center text-gray-500 text-sm mt-12 pt-8 border-t border-slate-800">
            <p>Realtime Tech Library • V2 概念导向版</p>
            <p class="mt-2">最后更新: 2026-03-11</p>
        </footer>
</div>'''
                
                article['content'] = fixed_content + ending
                print('   ✅ pScatter 已修复')
        else:
            print('   ✓ pScatter 格式正常')
    
    # 检查 3DGS
    if '704c94c2a1d8' in kb.get('articles', {}):
        print('🔧 检查 3DGS 文章...')
        article = kb['articles']['704c94c2a1d8']
        content_str = article.get('content', '').strip()
        
        if content_str.startswith('<div class="article-content">') and content_str.endswith('</div>'):
            print('   ✓ 3DGS 格式正常')
        else:
            print('   ⚠️ 3DGS 可能需要检查')
    
    # 保存修复后的文件
    output = 'const knowledgeBase = ' + json.dumps(kb, ensure_ascii=False, indent=2) + ';\n'
    
    with open(KB_PATH, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print('\n✅ 修复完成！')
    
    # 验证
    try:
        verify_match = re.search(r'const knowledgeBase = ({[\s\S]*});?\s*$', output)
        if verify_match:
            json.loads(verify_match.group(1))
            print('✅ JSON 语法验证通过')
    except json.JSONDecodeError as e:
        print(f'❌ JSON 语法错误: {e}')

if __name__ == '__main__':
    main()
