#!/usr/bin/env node
/**
 * 网站问题诊断与修复脚本
 */

const fs = require('fs');

const KB_PATH = './knowledge-base.js';
const BACKUP_DIR = './articles-v2';

// 读取知识库
let kbContent = fs.readFileSync(KB_PATH, 'utf8');
const match = kbContent.match(/const knowledgeBase = ({[\s\S]*});?\s*$/);
const kb = JSON.parse(match[1]);

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║           Realtime Tech Library - 网站问题诊断报告           ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();

// 统计
const articles = Object.entries(kb.articles);
console.log('📊 总体统计:');
console.log('   总文章数:', articles.length);
console.log();

// 内容长度分类
const categories = {
  '占位符(<2KB)': [],
  '简短(2-10KB)': [],
  '中等(10-30KB)': [],
  '完整V2(>30KB)': []
};

articles.forEach(([id, art]) => {
  const size = art.content ? art.content.length : 0;
  if (size < 2000) categories['占位符(<2KB)'].push({id, title: art.title, size});
  else if (size < 10000) categories['简短(2-10KB)'].push({id, title: art.title, size});
  else if (size < 30000) categories['中等(10-30KB)'].push({id, title: art.title, size});
  else categories['完整V2(>30KB)'].push({id, title: art.title, size});
});

console.log('📈 内容长度分布:');
Object.entries(categories).forEach(([cat, list]) => {
  console.log(`   ${cat}: ${list.length}篇`);
});
console.log();

console.log('❌ 严重问题 - 占位符文章(<2KB):');
categories['占位符(<2KB)'].forEach(a => {
  console.log(`   - ${a.id}: ${a.title.substring(0, 50)} (${Math.round(a.size/1024)}KB)`);
});
console.log();

console.log('⚠️  需要注意 - 简短文章(2-10KB):');
categories['简短(2-10KB)'].slice(0, 10).forEach(a => {
  console.log(`   - ${a.id}: ${a.title.substring(0, 50)} (${Math.round(a.size/1024)}KB)`);
});
if (categories['简短(2-10KB)'].length > 10) {
  console.log(`   ... 还有 ${categories['简短(2-10KB)'].length - 10} 篇`);
}
console.log();

console.log('✅ 完整V2文章(>30KB):');
categories['完整V2(>30KB)'].forEach(a => {
  console.log(`   - ${a.id}: ${a.title.substring(0, 50)} (${Math.round(a.size/1024)}KB)`);
});
console.log();

// 检查备份
console.log('💾 备份文件检查:');
const backups = fs.readdirSync(BACKUP_DIR);
console.log(`   articles-v2/ 目录下有 ${backups.length} 个备份文件:`);
backups.forEach(f => {
  const stats = fs.statSync(`${BACKUP_DIR}/${f}`);
  console.log(`   - ${f} (${Math.round(stats.size/1024)}KB)`);
});
console.log();

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║                        问题总结                             ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();
console.log('🔴 发现问题:');
console.log(`   1. 有 ${categories['占位符(<2KB)'].length} 篇文章只有占位符内容(<2KB)`);
console.log(`   2. 有 ${categories['简短(2-10KB)'].length} 篇文章内容简短(2-10KB)，可能未完成`);
console.log(`   3. 只有 ${categories['完整V2(>30KB)'].length} 篇文章达到V2标准(>30KB)`);
console.log(`   4. 备份目录中只有 ${backups.length} 篇文章有备份`);
console.log();
console.log('📋 建议操作:');
console.log('   1. 重新改写所有占位符文章');
console.log('   2. 扩充简短文章到V2标准');
console.log('   3. 建立定期备份机制');
console.log();
