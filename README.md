# 🧹 QQ聊天记录清理工具

一个简单而强大的工具，帮助你清理QQ聊天记录文件，移除无用信息，只保留有价值的讨论内容。✨

## 🌟 主要功能

- 数据预处理部分
  - 📅 根据日期范围筛选内容
  - 🗑️ 移除日期时间行、QQ号、昵称等信息
  - 🖼️ 移除\[图片\]标记和其他表情符号
  - ⚙️ 移除系统消息和无用重复消息，支持自定义过滤关键词
    <!-- - 📊 提供详细的处理统计信息 -->
- AI 总结部分
  - 


## 📁 目录结构

```
.
├── process_chat_logs.py  # 主程序
├── filter_keywords.txt   # 过滤规则配置文件
├── inputs/               # 输入文件目录
└── outputs/              # 输出文件目录

## 🚀 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/JyiDeng/qq-chat-ai-conclusion.git
cd qq-chat-ai-conclusion
```

2. 准备聊天记录：
   - 将QQ聊天记录文件放入 `inputs` 目录
   - 确保文件使用 UTF-8 编码

3. 运行程序：
```bash
python process_chat_logs.py
```

处理后的文件将保存在 `outputs` 目录，文件名格式为：`cleaned_原文件名_日期范围.txt`

## 📖 使用说明


### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-f, --file` | 指定要处理的文件 | `-f "chat.txt"` |
| `-o, --output` | 指定输出文件路径 | `-o "output/result.txt"` |
| `-d, --directory` | 处理指定目录下的所有文件 | `-d "inputs"` |
| `-v, --verbose` | 显示详细处理信息 | `-v` |
| `-k, --keywords` | 指定过滤关键词配置文件 | `-k "filter_keywords.txt"` |
| `-t, --date` | 指定日期范围 | `-t "2025-03-18"` |


#### 基本用例

```bash
# 处理 inputs 目录下的所有文件，参数均采取默认值
python process_chat_logs.py

# 处理单个文件
python process_chat_logs.py -f "inputs/example.txt"

# 显示详细处理信息
python process_chat_logs.py -v
```

#### 日期筛选示例

```bash
# 筛选指定日期的内容
python process_chat_logs.py -t "2025-03-18"

# 筛选日期范围的内容
python process_chat_logs.py -t "2025-03-16=2025-03-18"

# 组合使用参数
python process_chat_logs.py -f "example.txt" -t "2025-03-18" -v
```

## ⚙️ 自定义过滤规则

在 `filter_keywords.txt` 中添加过滤规则，每行一个：

```text
# 普通文本
Q群管家
[图片]

# 正则表达式（以 \ 开头）
\[表情\]
\[流泪\].*
```




## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个工具！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件