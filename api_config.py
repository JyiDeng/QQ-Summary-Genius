import os
import json
import configparser
from pathlib import Path

# 默认配置文件路径
CONFIG_FILE = "api_keys.ini"

# API 配置，注意不是在这里配置，这只是模版；应该在 `api_keys.ini` 文件中配置。
DEFAULT_API_CONFIG = {
    'siliconflow': {
        'api_url': 'https://api.siliconflow.cn/v1/chat/completions',
        'api_key': '',  # 用户需要配置
        'model': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B'  # 使用SiliconFlow支持的模型
    },
    'openai': {
        'api_url': 'https://api.openai.com/v1/chat/completions',
        'api_key': '',  # 用户需要配置
        'model': 'gpt-3.5-turbo'
    },
    'anthropic': {
        'api_url': 'https://api.anthropic.com/v1/messages',
        'api_key': '',  # 用户需要配置
        'model': 'claude-3-sonnet-20240229'
    }
}

def create_default_config():
    """创建默认配置文件"""
    config = configparser.ConfigParser()
    
    for api_name, api_info in DEFAULT_API_CONFIG.items():
        config[api_name] = {
            'api_key': api_info['api_key'] or os.environ.get(f"{api_name.upper()}_API_KEY", ''),
            'api_url': api_info['api_url'],
            'model': api_info['model']
        }
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        config.write(f)
    
    print(f"已创建默认配置文件: {CONFIG_FILE}")
    print("请编辑此文件，填入你的API密钥。")

def load_api_config():
    """加载API配置"""
    config_path = Path(CONFIG_FILE)
    
    # 如果配置文件不存在，创建默认配置
    if not config_path.exists():
        create_default_config()
        return DEFAULT_API_CONFIG
    
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    
    api_config = {}
    for api_name, api_info in DEFAULT_API_CONFIG.items():
        if api_name in config:
            api_config[api_name] = {
                'api_url': config[api_name].get('api_url', api_info['api_url']),
                'api_key': config[api_name].get('api_key') or os.environ.get(f"{api_name.upper()}_API_KEY", ''),
                'model': config[api_name].get('model', api_info['model'])
            }
        else:
            api_config[api_name] = api_info.copy()
            api_config[api_name]['api_key'] = os.environ.get(f"{api_name.upper()}_API_KEY", '')
    
    return api_config

def setup_api_keys():
    """设置API密钥交互式向导"""
    config_path = Path(CONFIG_FILE)
    config = configparser.ConfigParser()
    
    # 如果配置文件存在，读取它
    if config_path.exists():
        config.read(CONFIG_FILE, encoding='utf-8')
    
    # 遍历所有API提供商
    for api_name, api_info in DEFAULT_API_CONFIG.items():
        # 确保该部分存在
        if api_name not in config:
            config[api_name] = {}
        
        # 获取当前API密钥
        current_key = config[api_name].get('api_key', '')
        if not current_key:
            current_key = os.environ.get(f"{api_name.upper()}_API_KEY", '')
        
        # 打印当前API名称
        print(f"\n配置 {api_name.capitalize()} API:")
        
        # 询问用户输入API密钥
        masked_key = '****' + current_key[-4:] if len(current_key) > 4 else ''
        prompt = f"请输入API密钥 {f'(当前: {masked_key})' if masked_key else ''} (回车跳过该项): "
        new_key = input(prompt)
        
        # 如果用户输入了新密钥，更新配置
        if new_key:
            config[api_name]['api_key'] = new_key
        elif current_key and not config[api_name].get('api_key'):
            config[api_name]['api_key'] = current_key
        
        # 确保其他配置项存在
        if 'api_url' not in config[api_name]:
            config[api_name]['api_url'] = api_info['api_url']
        if 'model' not in config[api_name]:
            config[api_name]['model'] = api_info['model']
    
    # 保存配置文件
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        config.write(f)
    
    print(f"\n配置已保存到: {CONFIG_FILE}")
    print("你可以随时编辑此文件来更新API密钥。")

if __name__ == "__main__":
    setup_api_keys() 