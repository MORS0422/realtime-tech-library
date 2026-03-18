#!/usr/bin/env node
/**
 * 修复 pScatter 和 3DGS 文章的内容格式
 * 问题：pScatter 内容被错误地拼接了两次，需要清理重复部分
 */

const fs = require('fs');
const path = require('path');

const KB_PATH = path.join(__dirname, 'knowledge-base.js');

// 读取文件
let content = fs.readFileSync(KB_PATH, 'utf8');

// 提取 JSON 部分（去掉 const knowledgeBase = 和最后的 ;）
const jsonMatch = content.match(/const knowledgeBase = ({[\s\S]*});?\s*$/);
if (!jsonMatch) {
    console.error('❌ 无法解析 knowledge-base.js');
    process.exit(1);
}

let kb;
try {
    kb = JSON.parse(jsonMatch[1]);
} catch (e) {
    console.error('❌ JSON 解析失败:', e.message);
    process.exit(1);
}

console.log('📋 检查文章...');

// 修复 pScatter (440e06882426)
const pscatter = kb.articles['440e06882426'];
if (pscatter && pscatter.content) {
    console.log('🔧 检查 pScatter 文章...');
    
    // 检查是否包含重复内容标记
    const content = pscatter.content;
    
    // 查找 "（文章前半部分完成" 这个标记
    const markerIndex = content.indexOf('（文章前半部分完成');
    
    if (markerIndex !== -1) {
        console.log('   发现重复内容标记，需要清理');
        
        // 找到 marker 之前的最后一个 </section>
        const beforeMarker = content.substring(0, markerIndex);
        
        // 找到最后一个 </section> 的位置
        const lastSectionEnd = beforeMarker.lastIndexOf('</section>');
        
        if (lastSectionEnd !== -1) {
            // 提取到 </section> 为止的内容
            const fixedContent = beforeMarker.substring(0, lastSectionEnd + '</section>'.length);
            
            // 添加完整的 Section 4-6 和结尾
            const continuation = `

        <!-- Section 4: Implementation -->
        <section id="implementation" class="mb-12">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <span class="text-neon-blue mr-3">4</span>
                Nuke 节点实现详解
            </h2>
            
            <h3 class="text-lg font-semibold mb-3 text-gray-200">4.1 Position Pass 提取与预处理</h3>
            
            <p class="text-gray-300 leading-relaxed mb-4">
                在 Nuke 中使用 Position Pass 的第一步是正确提取和预处理。由于 Position Pass 通常以 32-bit float 格式存储，需要确保 Nuke 的<strong>色彩空间</strong>和<strong>位深度</strong>设置正确。
            </p>

            <div class="code-block rounded-xl p-6 mb-6">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-sm font-semibold text-gray-400">Nuke Python - Position Pass 读取与验证</span>
                    <span class="text-xs text-gray-500">Python</span>
                </div>
                <pre class="text-sm text-gray-300 overflow-x-auto"><code># Position Pass 预处理节点网络
import nuke

def setup_position_pass():
    """创建 Position Pass 预处理节点网络"""
    pos_read = nuke.nodes.Read(file="path/to/position_pass.exr")
    pos_read['colorspace'].setValue('linear')
    return pos_read</code></pre>
            </div>

            <h3 class="text-lg font-semibold mb-3 text-gray-200">4.2 边缘检测节点实现</h3>
            
            <p class="text-gray-300 leading-relaxed mb-4">
                基于 Position Pass 的梯度计算实现边缘检测。
            </p>

            <div class="code-block rounded-xl p-6 mb-6">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-sm font-semibold text-gray-400">边缘检测实现</span>
                    <span class="text-xs text-gray-500">Nuke</span>
                </div>
                <pre class="text-sm text-gray-300 overflow-x-auto"><code># 使用 Sobel 算子计算 Position Pass 梯度
sobel_x = nuke.nodes.Matrix(inputs=[pos_input], matrix='{ { -1 0 1 } { -2 0 2 } { -1 0 1 } }')
sobel_y = nuke.nodes.Matrix(inputs=[pos_input], matrix='{ { -1 -2 -1 } { 0 0 0 } { 1 2 1 } }')</code></pre>
            </div>
        </section>

        <!-- Section 5: Applications -->
        <section id="applications" class="mb-12">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <span class="text-neon-blue mr-3">5</span>
                实际应用与案例分析
            </h2>
            
            <h3 class="text-lg font-semibold mb-3 text-gray-200">5.1 典型应用场景</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div class="glass-card rounded-xl p-4 border-l-4 border-blue-500">
                    <h4 class="font-semibold text-blue-400 mb-2">🏢 建筑可视化</h4>
                    <p class="text-sm text-gray-400">为建筑渲染添加风化效果：窗户边缘积尘、墙角污渍。</p>
                </div>
                <div class="glass-card rounded-xl p-4 border-l-4 border-purple-500">
                    <h4 class="font-semibold text-purple-400 mb-2">🎬 影视后期</h4>
                    <p class="text-sm text-gray-400">为 CG 角色添加真实感：盔甲磨损、布料污渍。</p>
                </div>
            </div>
        </section>

        <!-- Section 6: References -->
        <section id="references" class="mb-12">
            <h2 class="text-2xl font-bold mb-6 flex items-center">
                <span class="text-neon-blue mr-3">6</span>
                参考与扩展阅读
            </h2>
            
            <ul class="space-y-2 text-gray-300 mb-6">
                <li><a href="https://www.cgchannel.com/2024/09/free-nuke-plugin-pscatter/" class="text-blue-400 hover:underline">CG Channel - pScatter 插件</a></li>
                <li><a href="https://learn.foundry.com/nuke/" class="text-blue-400 hover:underline">Foundry Nuke 官方文档</a></li>
            </ul>
        </section>

        <!-- Footer -->
        <footer class="text-center text-gray-500 text-sm mt-12 pt-8 border-t border-slate-800">
            <p>Realtime Tech Library • V2 概念导向版</p>
            <p class="mt-2">最后更新: 2026-03-11 • 阅读时间: 30-35分钟</p>
        </footer>
</div>`;
            
            kb.articles['440e06882426'].content = fixedContent + continuation;
            console.log('   ✅ pScatter 已修复');
        }
    } else {
        console.log('   ✓ pScatter 格式正常');
    }
}

// 3DGS 检查
const gs = kb.articles['704c94c2a1d8'];
if (gs && gs.content) {
    console.log('🔧 检查 3DGS 文章...');
    
    if (gs.content.trim().startsWith('<div class="article-content">') && 
        gs.content.trim().endsWith('</div>')) {
        console.log('   ✓ 3DGS 格式正常');
    } else {
        console.log('   ⚠️ 3DGS 可能需要检查');
    }
}

// 保存修复后的文件
const output = 'const knowledgeBase = ' + JSON.stringify(kb, null, 2) + ';\n';
fs.writeFileSync(KB_PATH, output, 'utf8');

console.log('\n✅ 修复完成！');

// 验证 JSON 语法
try {
    const verifyMatch = output.match(/const knowledgeBase = ({[\s\S]*});?\s*$/);
    if (verifyMatch) {
        JSON.parse(verifyMatch[1]);
        console.log('✅ JSON 语法验证通过');
    }
} catch (e) {
    console.error('❌ JSON 语法错误:', e.message);
}
