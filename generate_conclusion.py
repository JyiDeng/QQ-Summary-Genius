import os
import re
import json
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 导入API配置模块
from api_config import load_api_config, setup_api_keys

# ===== 可自定义的系统提示词 =====
# 此提示词用于指导AI如何总结聊天内容
# 可根据需要修改以获得不同风格或侧重点的总结
SYSTEM_PROMPT = "你是一个专业的聊天内容分析助手。你的任务是对QQ聊天记录进行简明扼要的总结。内容上，你需要着重关注事实上发生的内容，尤其是当前时事的细节。如果有链接，你需要原样保留。*不要*添加任何主观评论。格式上，你需要按照内容前后的顺序，按话题划分小标题。"

# 加载API配置
API_CONFIG = load_api_config()

def call_siliconflow_api(content, prompt=None):
    """
    调用SiliconFlow API进行内容总结
    
    Args:
        content: 需要总结的内容
        prompt: 自定义提示词，默认为None
    
    Returns:
        总结内容
    """
    if not API_CONFIG['siliconflow']['api_key']:
        raise ValueError("未设置SiliconFlow API密钥，请使用 'python api_config.py' 设置密钥或设置环境变量SILICONFLOW_API_KEY")
    
    if prompt is None:
        prompt = "请对以下聊天记录内容进行简要总结，提取主要话题和关键信息：\n\n"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_CONFIG['siliconflow']['api_key']}"
    }
    
    # 使用SiliconFlow支持的模型
    model = API_CONFIG['siliconflow']['model']
    # 检查模型名称，确保使用有效模型
    if model == "Yi-1.5-Large-Instruct-B":
        # 可以使用这个默认模型，但确保这是SiliconFlow支持的
        pass
    elif not model or model == "":
        # 如果未设置或为空，使用推荐的免费模型
        model = "qwen/Qwen2.5-7B-Chat"
    
    user_message = f"{prompt}{content}"
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(
            API_CONFIG['siliconflow']['api_url'],
            headers=headers,
            json=data,
            timeout=60
        )
        
        # 错误处理
        if response.status_code != 200:
            error_info = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"message": response.text}
            error_message = error_info.get('message', '未知错误')
            raise ValueError(f"SiliconFlow API错误 (状态码: {response.status_code}): {error_message}")
        
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise ValueError(f"网络请求错误: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析API响应: {response.text}")
    except KeyError as e:
        raise ValueError(f"API响应格式错误: {str(e)}\n响应内容: {response.text[:500]}")

def call_openai_api(content, prompt=None):
    """
    调用OpenAI API进行内容总结
    
    Args:
        content: 需要总结的内容
        prompt: 自定义提示词，默认为None
    
    Returns:
        总结内容
    """
    if not API_CONFIG['openai']['api_key']:
        raise ValueError("未设置OpenAI API密钥，请使用 'python api_config.py' 设置密钥或设置环境变量OPENAI_API_KEY")
    
    if prompt is None:
        prompt = "请对以下聊天记录内容进行简要总结，提取主要话题和关键信息：\n\n"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_CONFIG['openai']['api_key']}"
    }
    
    data = {
        "model": API_CONFIG['openai']['model'],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{prompt}{content}"}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(
            API_CONFIG['openai']['api_url'],
            headers=headers,
            json=data,
            timeout=60
        )
        
        # 错误处理
        if response.status_code != 200:
            error_info = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"message": response.text}
            error_message = error_info.get('message', '未知错误')
            raise ValueError(f"OpenAI API错误 (状态码: {response.status_code}): {error_message}")
        
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise ValueError(f"网络请求错误: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析API响应: {response.text}")
    except KeyError as e:
        raise ValueError(f"API响应格式错误: {str(e)}\n响应内容: {response.text[:500]}")

def call_anthropic_api(content, prompt=None):
    """
    调用Anthropic Claude API进行内容总结
    
    Args:
        content: 需要总结的内容
        prompt: 自定义提示词，默认为None
    
    Returns:
        总结内容
    """
    if not API_CONFIG['anthropic']['api_key']:
        raise ValueError("未设置Anthropic API密钥，请使用 'python api_config.py' 设置密钥或设置环境变量ANTHROPIC_API_KEY")
    
    if prompt is None:
        prompt = "请对以下聊天记录内容进行简要总结，提取主要话题和关键信息：\n\n"
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_CONFIG['anthropic']['api_key'],
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": API_CONFIG['anthropic']['model'],
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"{prompt}{content}"}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(
            API_CONFIG['anthropic']['api_url'],
            headers=headers,
            json=data,
            timeout=60
        )
        
        # 错误处理
        if response.status_code != 200:
            error_info = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"message": response.text}
            error_message = error_info.get('message', '未知错误')
            raise ValueError(f"Anthropic API错误 (状态码: {response.status_code}): {error_message}")
        
        result = response.json()
        return result['content'][0]['text']
    except requests.exceptions.RequestException as e:
        raise ValueError(f"网络请求错误: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析API响应: {response.text}")
    except KeyError as e:
        raise ValueError(f"API响应格式错误: {str(e)}\n响应内容: {response.text[:500]}")

def extract_original_filename(cleaned_filename):
    """
    从清理后的文件名提取原始文件名（不含cleaned_前缀和日期部分）
    
    Args:
        cleaned_filename: 清理后的文件名，如 cleaned_example_2025-03-18.txt
    
    Returns:
        原始文件名部分
    """
    # 移除cleaned_前缀
    name_without_prefix = cleaned_filename.replace('cleaned_', '')
    
    # # 提取不含日期部分的原始文件名
    # match = re.search(r'(.+?)_\d{4}-\d{2}-\d{2}', name_without_prefix)
    # if match:
    #     return match.group(1)
    
    # # 对于范围日期格式
    # match = re.search(r'(.+?)_\d{4}-\d{2}-\d{2}=\d{4}-\d{2}-\d{2}', name_without_prefix)
    # if match:
    #     return match.group(1)
    
    # # 如果没有匹配到日期格式，返回去除扩展名的文件名
    return os.path.splitext(name_without_prefix)[0]

def summarize_chat_content(file_path, api_sources=None, custom_prompt=None):
    """
    对聊天内容文件进行总结，使用多个API源
    
    Args:
        file_path: 需要总结的文件路径
        api_sources: API源列表，默认为['siliconflow']
        custom_prompt: 自定义提示词
    
    Returns:
        包含各API源总结结果的字典
    """
    if api_sources is None:
        api_sources = ['siliconflow']
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {}
    
    # 验证所有选定的API源是否配置了密钥
    missing_keys = []
    for api in api_sources:
        if api in API_CONFIG and not API_CONFIG[api]['api_key']:
            missing_keys.append(api)
    
    if missing_keys:
        missing_keys_str = ', '.join(missing_keys)
        raise ValueError(f"以下API源未设置密钥: {missing_keys_str}，请使用 'python api_config.py' 设置密钥")
    
    
    with ThreadPoolExecutor(max_workers=len(api_sources)) as executor:
        future_to_api = {}
        
        for api in api_sources:
            if api == 'siliconflow':
                future = executor.submit(call_siliconflow_api, content, custom_prompt)
            elif api == 'openai':
                future = executor.submit(call_openai_api, content, custom_prompt)
            elif api == 'anthropic':
                future = executor.submit(call_anthropic_api, content, custom_prompt)
            else:
                print(f"不支持的API源: {api}")
                continue
            
            future_to_api[future] = api
        
        for future in as_completed(future_to_api):
            api = future_to_api[future]
            try:
                result = future.result()
                results[api] = result
            except Exception as e:
                print(f"调用 {api} API时出错：{e}")
                # 不将错误信息写入结果，而是在控制台显示
    
    return results

def generate_conclusion(input_file, output_dir='conclusion', api_sources=None, custom_prompt=None):
    """
    生成聊天内容总结并保存到指定目录
    
    Args:
        input_file: 输入文件路径
        output_dir: 输出目录路径
        api_sources: API源列表
        custom_prompt: 自定义提示词
    
    Returns:
        输出文件路径
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 提取文件名
    file_name = os.path.basename(input_file)
    original_name = extract_original_filename(file_name)
    output_file = os.path.join(output_dir, f"conclusion_{original_name}.md")
    
    # 调用API进行总结
    try:
        summary_results = summarize_chat_content(input_file, api_sources, custom_prompt)
    except ValueError as e:
        print(f"错误: {e}")
        return None
    
    # 如果没有成功获取任何总结结果，退出
    if not summary_results:
        print(f"错误: 未能从任何API源获取总结结果")
        return None
    
    # 构建输出内容
    output_content = f"# QQ聊天文字记录AI总结助手 by JyiDeng: https://github.com/JyiDeng/qq_chat_ai_conclusion\n\n"
    # output_content += f"# 聊天记录总结: {original_name}\n\n"
    output_content += f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    output_content += f"*原始文件: {file_name}*\n\n"
    
    # 添加各API的总结内容
    for api, summary in summary_results.items():
        output_content += f"## {api.capitalize()} 总结\n\n"
        output_content += f"{summary}\n\n"
    
    # 保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"已生成总结文件: {output_file}")
    return output_file

def process_all_files(input_dir='outputs', output_dir='conclusion', api_sources=None, custom_prompt=None):
    """
    处理指定目录下的所有cleaned_开头的文件
    
    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
        api_sources: API源列表
        custom_prompt: 自定义提示词
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有cleaned_开头的文件
    files = [f for f in os.listdir(input_dir) if f.startswith('cleaned_') and os.path.isfile(os.path.join(input_dir, f))]
    
    if not files:
        print(f"在 {input_dir} 目录下未找到任何cleaned_开头的文件")
        return
    
    print(f"找到 {len(files)} 个文件需要处理:")
    for file in files:
        print(f"  - {file}")
    
    # 在处理所有文件前验证API密钥
    try:
        # 验证所有选定的API源是否配置了密钥
        missing_keys = []
        for api in (api_sources or ['siliconflow']):
            if api in API_CONFIG and not API_CONFIG[api]['api_key']:
                missing_keys.append(api)
        
        if missing_keys:
            missing_keys_str = ', '.join(missing_keys)
            raise ValueError(f"以下API源未设置密钥: {missing_keys_str}，请使用 'python api_config.py' 设置密钥")
    except ValueError as e:
        print(f"错误: {e}")
        return
    
    # 处理每个文件
    success_count = 0
    for file in files:
        input_file = os.path.join(input_dir, file)
        try:
            output_file = generate_conclusion(input_file, output_dir, api_sources, custom_prompt)
            if output_file:
                print(f"成功处理文件: {file} -> {os.path.basename(output_file)}")
                success_count += 1
        except Exception as e:
            print(f"处理文件 {file} 时出错: {e}")
    
    print(f"总计: {success_count}/{len(files)} 个文件处理成功")

def main():
    """命令行入口函数"""
    global API_CONFIG
    global SYSTEM_PROMPT
    
    parser = argparse.ArgumentParser(description='QQ聊天记录AI总结工具')
    parser.add_argument('-f', '--file', help='指定要处理的文件路径')
    parser.add_argument('-d', '--input-dir', default='outputs', help='指定要处理的文件目录，默认为outputs')
    parser.add_argument('-o', '--output-dir', default='conclusion', help='指定总结文件输出目录，默认为conclusion')
    parser.add_argument('-a', '--api', nargs='+', default=['siliconflow'], 
                        choices=['siliconflow', 'openai', 'anthropic'], 
                        help='指定要使用的API源，可多选')
    parser.add_argument('-p', '--prompt', help='自定义提示词')
    parser.add_argument('-c', '--config', action='store_true', help='配置API密钥')
    parser.add_argument('-m', '--model', help='指定要使用的SiliconFlow模型名称')
    parser.add_argument('-s', '--system-prompt', help='设置系统提示词，用于指导AI如何总结内容')
    
    args = parser.parse_args()
    
    # 如果用户选择配置API密钥
    if args.config:
        setup_api_keys()
        return
    
    # 如果用户指定了系统提示词
    if args.system_prompt:
        SYSTEM_PROMPT = args.system_prompt
        print(f"已设置系统提示词: {SYSTEM_PROMPT}")
    
    # 如果用户指定了模型，更新配置
    if args.model and 'siliconflow' in API_CONFIG:
        API_CONFIG['siliconflow']['model'] = args.model
    
    # 检查API环境变量是否设置
    missing_keys = []
    for api in args.api:
        if api in API_CONFIG and not API_CONFIG[api]['api_key']:
            missing_keys.append(api)
    
    if missing_keys:
        missing_keys_str = ', '.join(missing_keys)
        print(f"警告: 以下API源未设置密钥: {missing_keys_str}")
        print("你可以使用以下命令配置API密钥: python generate_conclusion.py -c")
        
        # 询问用户是否现在配置
        response = input("是否现在配置API密钥? (y/n): ")
        if response.lower() == 'y':
            setup_api_keys()
            # 重新加载配置
            API_CONFIG = load_api_config()
            
            # 如果用户指定了模型，重新更新配置
            if args.model and 'siliconflow' in API_CONFIG:
                API_CONFIG['siliconflow']['model'] = args.model
        else:
            print("未配置API密钥，程序退出。")
            return
    
    if args.file:
        if not os.path.exists(args.file):
            print(f"错误: 文件 {args.file} 不存在")
            return
        generate_conclusion(args.file, args.output_dir, args.api, args.prompt)
    else:
        process_all_files(args.input_dir, args.output_dir, args.api, args.prompt)

if __name__ == "__main__":
    main() 