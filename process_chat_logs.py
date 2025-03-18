from datetime import datetime, timedelta
import re
import os
import argparse

def get_last_message_date(content):
    """
    获取聊天记录中最后一条消息的日期
    
    Args:
        content: 聊天记录内容
    
    Returns:
        最后一条消息的日期（datetime对象）或当前日期
    """
    # 查找所有日期行
    date_matches = re.findall(r'(\d{4})-(\d{2})-(\d{2})', content)
    
    if date_matches:
        # 获取最后一个日期
        last_match = date_matches[-1]
        year, month, day = map(int, last_match)
        return datetime(year, month, day)
    
    # 如果没有找到日期，返回当前日期
    return datetime.now()

def parse_date_range(date_str, content=None):
    """
    解析日期范围字符串
    
    Args:
        date_str: 日期范围字符串，格式为 "YYYY-MM-DD" 或 "YYYY-MM-DD=YYYY-MM-DD"
        content: 聊天记录内容，用于获取最后一条消息的日期
    
    Returns:
        (start_date, end_date): 开始日期和结束日期的元组
    """
    if not date_str:
        # 如果没有指定日期且提供了内容，使用最后一条消息的日期
        if content:
            last_date = get_last_message_date(content)
            return last_date, last_date
        # 否则使用当前日期
        today = datetime.now()
        return today, today
    
    if '=' in date_str:
        start_str, end_str = date_str.split('=')
        start_date = datetime.strptime(start_str.strip(), '%Y-%m-%d')
        end_date = datetime.strptime(end_str.strip(), '%Y-%m-%d')
    else:
        date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        start_date = date
        end_date = date
    
    return start_date, end_date

def extract_date_from_line(line):
    """
    从行中提取日期
    
    Args:
        line: 包含日期的行
    
    Returns:
        datetime对象或None
    """
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})', line)
    if match:
        year, month, day = map(int, match.groups())
        return datetime(year, month, day)
    return None

def filter_by_date(content, start_date, end_date):
    """
    根据日期范围筛选内容
    
    Args:
        content: 原始内容
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        筛选后的内容
    """
    lines = content.split('\n')
    filtered_lines = []
    current_date = None
    
    for line in lines:
        date = extract_date_from_line(line)
        if date:
            current_date = date
            if start_date <= current_date <= end_date:
                filtered_lines.append(line)
        elif current_date and start_date <= current_date <= end_date:
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)

def load_filter_keywords(filter_file='filter_keywords.txt'):
    """
    从配置文件中加载需要过滤的关键词
    
    Args:
        filter_file: 过滤关键词配置文件路径
    
    Returns:
        包含所有过滤关键词的列表
    """
    if not os.path.exists(filter_file):
        print(f"警告: 过滤配置文件 '{filter_file}' 不存在，将使用默认过滤规则")
        return []
    
    keywords = []
    with open(filter_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                keywords.append(line)
    
    return keywords

def clean_chat_log(input_file, output_file=None, verbose=False, filter_file='filter_keywords.txt', date_range=None):
    """
    清理QQ聊天记录:
    1. 根据日期范围筛选内容
    2. 移除所有日期时间行
    3. 移除[图片]标记
    4. 合并超过一行的连续空行为单个空行
    5. 移除QQ号、系统消息、无用重复消息
    6. 移除表情符号
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径，如果为None则自动生成"cleaned_"前缀的文件名
        verbose: 是否显示详细信息
        filter_file: 过滤关键词配置文件路径
        date_range: 日期范围字符串，格式为 "YYYY-MM-DD" 或 "YYYY-MM-DD=YYYY-MM-DD"
    
    Returns:
        处理后的文本内容
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"找不到输入文件: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录原始行数
    original_lines = content.count('\n') + 1
    
    # 解析日期范围
    start_date, end_date = parse_date_range(date_range, content)
    
    # 根据日期范围筛选内容
    content = filter_by_date(content, start_date, end_date)
    
    if output_file is None:
        dir_name = os.path.dirname(input_file)
        base_name = os.path.basename(input_file)
        
        # 创建输出目录（如果不存在）
        output_dir = os.path.join(dir_name, "../outputs")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 修改输出文件名格式：根据日期范围命名
        filename, ext = os.path.splitext(base_name)
        
        # 根据日期范围生成文件名部分
        if start_date == end_date:
            date_suffix = start_date.strftime('%Y-%m-%d')
        else:
            date_suffix = f"{start_date.strftime('%Y-%m-%d')}={end_date.strftime('%Y-%m-%d')}"
        
        output_file = os.path.join(output_dir, f"cleaned_{filename}_{date_suffix}{ext}")
    
    # 移除文件头部的元信息
    content = re.sub(r'消息记录（此消息记录为文本格式，不支持重新导入）\n+', '', content)
    content = re.sub(r'={64,}\n消息分组:.*\n={64,}\n消息对象:.*\n={64,}\n+', '', content)
    
    # 移除日期时间行 (匹配格式如 2025-03-18 10:08:26)
    content = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [^\n]+\n', '', content)
    
    # 应用自定义过滤规则
    filter_keywords = load_filter_keywords(filter_file)
    for keyword in filter_keywords:
        try:
            # 尝试按正则表达式处理
            if keyword.startswith('\\'):
                content = re.sub(r'' + keyword, '', content)
            else:
                # 普通文本替换
                content = content.replace(keyword, '')
        except re.error:
            # 如果正则表达式无效，按普通文本处理
            content = content.replace(keyword, '')
    
    # 基本过滤规则（保持原有功能）
    content = content.replace('[图片]', '')
    
    # 替换多个连续空行为单个空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 移除每行开头的QQ号格式 (12345678)
    content = re.sub(r'\([0-9]+\)', '', content)
    
    # 移除@用户名 格式
    content = re.sub(r'@[^ ]+ @[^ ]+ ', '', content)
    content = re.sub(r'@[^ ]+ ', '', content)
    
    # 移除QQ表情代码
    content = re.sub(r'\[表情\]', '', content)
    content = re.sub(r'\[流泪\][^\n]*', '', content)
    content = re.sub(r'\[[^\]]+\]', '', content)  # 移除所有方括号包围的表情
    
    # 清理剩余的空行
    content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)
    
    # 移除开头和结尾的空行
    content = content.strip()
    
    # 计算处理后的行数
    processed_lines = content.count('\n') + 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if verbose:
        print(f"已清理聊天记录 '{input_file}' -> '{output_file}'")
        print(f"  - 原始行数: {original_lines}")
        print(f"  - 处理后行数: {processed_lines}")
        print(f"  - 减少了 {original_lines - processed_lines} 行 ({100 * (original_lines - processed_lines) / original_lines:.1f}%)")
        if filter_keywords:
            print(f"  - 应用了 {len(filter_keywords)} 个自定义过滤规则")
        print(f"  - 日期范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")
    else:
        print(f"已清理聊天记录并保存至: {output_file}")
    
    return content

def process_all_chat_logs(directory='inputs/', verbose=False, filter_file='filter_keywords.txt', date_range=None):
    """
    处理指定目录下的所有聊天记录文件
    
    Args:
        directory: 目录路径，默认为inputs/目录
        verbose: 是否显示详细信息
        filter_file: 过滤关键词配置文件路径
        date_range: 日期范围字符串
    
    Returns:
        处理的文件数量
    """
    if not os.path.exists(directory):
        print(f"警告: 目录不存在: {directory}")
        return 0
    
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.txt') and not filename.startswith('cleaned_'):
            input_path = os.path.join(directory, filename)
            clean_chat_log(input_path, verbose=verbose, filter_file=filter_file, date_range=date_range)
            count += 1
    
    return count

def main():
    parser = argparse.ArgumentParser(description='清理QQ聊天记录文件')
    parser.add_argument('-f', '--file', help='指定要处理的聊天记录文件')
    parser.add_argument('-o', '--output', help='指定输出文件路径')
    parser.add_argument('-d', '--directory', help='处理指定目录下的所有聊天记录文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细处理信息')
    parser.add_argument('-k', '--keywords', default='filter_keywords.txt', help='指定过滤关键词配置文件路径')
    parser.add_argument('-t', '--date', help='指定日期范围，格式为 "YYYY-MM-DD" 或 "YYYY-MM-DD=YYYY-MM-DD"')
    
    args = parser.parse_args()
    
    if args.file:
        clean_chat_log(args.file, args.output, verbose=args.verbose, filter_file=args.keywords, date_range=args.date)
        print("处理完成!")
    elif args.directory:
        count = process_all_chat_logs(args.directory, verbose=args.verbose, filter_file=args.keywords, date_range=args.date)
        print(f"处理完成! 共处理了 {count} 个聊天记录文件")
    else:
        count = process_all_chat_logs(verbose=args.verbose, filter_file=args.keywords, date_range=args.date)
        print(f"处理完成! 共处理了 {count} 个聊天记录文件")

if __name__ == "__main__":
    main()