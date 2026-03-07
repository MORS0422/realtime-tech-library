#!/usr/bin/env node
/**
 * 删除 knowledge-base.js 中的英文 multiplat 文章
 */

const fs = require('fs');
const path = require('path');

const KB_PATH = path.join(__dirname, 'knowledge-base.js');
const BACKUP_PATH = path.join(__dirname, 'knowledge-base.js.backup.' + Date.now());

// 需要删除的文章ID（英文标题的multiplat文章）
const ARTICLES_TO_DELETE = [
  '5b15b8653a61',  // Virtual Dice Roller
  '615c1ab9cb30',  // How to stay safe from doxxing?
  '12b42e50f19c',  // How to Build a Paper Prototype
  'a79faa3358c6',  // Are you interested in learning game design?
  '5d412250d44b',  // SIGGRAPH 2025 Links
  '59bbb4cdd52f',  // Valve in hot water...
  '11abe04c8ace',  // Could pre-launch open testing...
  '970eeabddcaf',  // How publishers can do better...
  'db42158dca70',  // Splash Damage acquires...
];

console.log('=== 清理英文 multiplat 文章 ===\n');

// 备份原文件
const originalContent = fs.readFileSync(KB_PATH, 'utf8');
fs.writeFileSync(BACKUP_PATH, originalContent);
console.log('✅ 已备份到:', BACKUP_PATH);

// 查找并删除文章
let modifiedContent = originalContent;
let deletedCount = 0;

for (const articleId of ARTICLES_TO_DELETE) {
  // 构建匹配模式：文章ID及其完整内容块
  const pattern = new RegExp(
    `\\s*"${articleId}":\\s*\\{[\\s\\S]*?"category":\\s*"multiplat"[\\s\\S]*?\\}(,|\\s*})`,
    'g'
  );
  
  const matches = modifiedContent.match(pattern);
  if (matches) {
    // 删除匹配的文章块
    modifiedContent = modifiedContent.replace(pattern, function(match, trailing) {
      // 如果后面跟着逗号，删除逗号
      if (trailing === ',') {
        return '';
      }
      return '';
    });
    console.log(`✅ 已删除: ${articleId}`);
    deletedCount++;
  } else {
    console.log(`⚠️ 未找到: ${articleId}`);
  }
}

// 清理可能出现的多余逗号（连续逗号或逗号后跟右花括号）
modifiedContent = modifiedContent.replace(/,\s*,/g, ',');
modifiedContent = modifiedContent.replace(/,\s*\}/g, '\n  }');

// 更新 meta.totalArticles
const currentCount = (modifiedContent.match(/"[a-z0-9-]+":\s*\{/g) || []).length - 1; // -1 for meta
modifiedContent = modifiedContent.replace(
  /"totalArticles":\s*\d+/,
  `"totalArticles": ${currentCount}`
);

// 更新时间戳
const now = new Date();
const dateStr = now.toISOString().slice(0, 16).replace('T', ' ');
modifiedContent = modifiedContent.replace(
  /"lastUpdated":\s*"[^"]+"/,
  `"lastUpdated": "${dateStr}"`
);

// 写入修改后的文件
fs.writeFileSync(KB_PATH, modifiedContent);
console.log(`\n=== 完成 ===`);
console.log(`✅ 删除了 ${deletedCount} 篇文章`);
console.log(`✅ 更新 totalArticles: ${currentCount}`);
console.log(`✅ 更新时间戳: ${dateStr}`);
console.log(`\n原文件已备份: ${BACKUP_PATH}`);
