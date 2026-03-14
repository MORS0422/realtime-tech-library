import json
import re

def fix_knowledge_base():
    with open('knowledge-base.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 方法：找到每个 article 对象，然后修复其中的 content 字段
    # 使用正则表达式找到 content 字段及其值
    
    # 匹配模式："content": "..." (多行)
    # 使用非贪婪匹配找到 content 值
    pattern = r'"content": "(.*?)"\n(?=\s*})'
    
    def replace_quotes_in_content(match):
        content_value = match.group(1)
        # 只替换中文引号为转义的英文引号
        content_value = content_value.replace('"', '\\"')
        content_value = content_value.replace('"', '\\"')
        return f'"content": "{content_value}"'
    
    # 这个模式可能不准确，让我用另一种方法
    
    # 方法二：逐字符解析
    result = []
    i = 0
    in_content = False
    content_depth = 0
    
    while i < len(content):
        char = content[i]
        
        # 检测 content 字段开始
        if not in_content and content[i:i+12] == '"content": "':
            in_content = True
            content_depth = 1
            result.append(char)
        elif in_content:
            if char == '"' or char == '"':
                # 中文引号，替换为转义的英文引号
                result.append('\\"')
            elif char == '"' and content[i-1:i] != '\\':
                # 可能是 content 的结束引号
                # 检查后面是否是换行和 }
                j = i + 1
                while j < len(content) and content[j] in ' \t':
                    j += 1
                if j < len(content) and content[j] == '\n':
                    # 可能是结束
                    k = j + 1
                    while k < len(content) and content[k] in ' \t':
                        k += 1
                    if k < len(content) and content[k] == '}':
                        # 找到 content 结束
                        in_content = False
                        result.append(char)
                    else:
                        # 不是结束，替换
                        result.append('\\"')
                else:
                    result.append(char)
            else:
                result.append(char)
        else:
            result.append(char)
        
        i += 1
    
    fixed_content = ''.join(result)
    
    # 验证修复
    try:
        json_start = fixed_content.find('{')
        data = json.loads(fixed_content[json_start:])
        print(f"✅ JSON 语法正确! 文章数量: {len(data.get('articles', {}))}")
        
        with open('knowledge-base.js', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("✅ 文件已保存")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON 错误: 第 {e.lineno} 行 - {e.msg}")
        return False

if __name__ == '__main__':
    fix_knowledge_base()
