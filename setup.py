import os
import sys
import re
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本是否符合要求"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        return False
    return True

def create_required_directories():
    """创建必要的目录结构"""
    directories = ['inputs', 'outputs', 'conclusion']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 已创建目录: {directory}/")

def install_dependencies():
    """安装所需的依赖包"""
    print("\n正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✓ 依赖包安装完成")
    except subprocess.CalledProcessError:
        print("× 安装依赖包失败，请手动安装: pip install requests")
        return False
    return True

def setup_api_keys():
    """设置API密钥"""
    print("\n配置API密钥")
    try:
        subprocess.check_call([sys.executable, "api_config.py"])
        print("✓ API密钥配置完成")
    except subprocess.CalledProcessError:
        print("× API密钥配置失败，请手动配置: python api_config.py")
        return False
    return True

def setup_system_prompt():
    """设置AI总结的系统提示词"""
    file_path = "generate_conclusion.py"
    
    # 确保文件存在
    if not os.path.exists(file_path):
        print("× 找不到generate_conclusion.py文件，无法修改系统提示词")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取当前的系统提示词
    prompt_pattern = r'SYSTEM_PROMPT\s*=\s*"([^"]+)"'
    prompt_match = re.search(prompt_pattern, content)
    
    if not prompt_match:
        print("× 无法在generate_conclusion.py中找到SYSTEM_PROMPT，将使用默认提示词")
        return False
    
    current_prompt = prompt_match.group(1)
    
    # 询问用户是否要修改提示词
    print("\n当前系统提示词:")
    print(f'"{current_prompt}"')
    
    response = input("是否要修改系统提示词? (y/n, 默认n): ")
    if response.lower() != 'y':
        print("保持默认系统提示词不变")
        return True
    
    # 获取用户输入的新提示词
    print("\n请输入新的系统提示词 (提示词将用于指导AI如何总结聊天内容):")
    new_prompt = input("新提示词: ")
    
    if not new_prompt:
        print("未输入新提示词，保持默认提示词不变")
        return True
    
    # 替换文件中的提示词
    updated_content = content.replace(f'SYSTEM_PROMPT = "{current_prompt}"', f'SYSTEM_PROMPT = "{new_prompt}"')
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✓ 系统提示词已更新")
    return True

def display_instructions():
    """显示使用说明"""
    print("\n🎉 环境配置完成！")
    print("\n🚀 快速开始:")
    print("  1. 将QQ聊天记录文件放入 'inputs/' 目录")
    print("  2. 运行清理程序: python process_chat_logs.py")
    print("  3. 运行AI总结程序: python generate_conclusion.py")
    print("\n📚 详细使用说明请参考 README.md")

def main():
    """主函数"""
    print("=" * 60)
    print("🧹 QQ聊天记录清理与AI总结工具 - 初始化向导")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 创建必要的目录
    create_required_directories()
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 询问是否配置API密钥
    api_response = input("\n是否现在配置AI API密钥? (y/n, 默认y): ")
    if api_response.lower() != 'n':
        setup_api_keys()
    else:
        print("跳过API密钥配置，您可以稍后通过运行 'python api_config.py' 进行配置")
    
    # 询问是否设置系统提示词
    prompt_response = input("\n是否设置AI总结的系统提示词? (y/n, 默认n): ")
    if prompt_response.lower() == 'y':
        setup_system_prompt()
    else:
        print("使用默认系统提示词，您可以稍后在generate_conclusion.py文件中修改")
    
    # 显示使用说明
    display_instructions()

if __name__ == "__main__":
    main() 