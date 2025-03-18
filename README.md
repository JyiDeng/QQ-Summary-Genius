# 🧹 QQ Summary Genius: QQ聊天文字记录AI总结助手

QQ Summary Genius ，一个简单而强大的QQ聊天AI总结工具，帮你提炼有价值的讨论内容。

## 🌟 主要功能

- 数据预处理部分
  - 📅 根据日期范围筛选内容
  - 🗑️ 移除日期时间行、QQ号、昵称等信息
  - 🖼️ 移除\[图片\]标记和其他表情符号
  - ⚙️ 移除系统消息和无用重复消息，支持自定义过滤关键词
    <!-- - 📊 提供详细的处理统计信息 -->
- AI 总结部分
  - 🤖 支持调用多种 AI API（SiliconFlow、OpenAI、Anthropic）进行内容总结
  - 📊 生成Markdown格式的总结报告
  <!-- - ⚡ 使用多线程并行调用多个API提高效率 -->
  - 🔑 便捷的 API 密钥、模型、提示词配置系统，支持交互式设置
  - 🔒 结果留于本地，安全性高


## 📁 目录结构

```
.
├── process_chat_logs.py  # 聊天记录清理主程序
├── generate_conclusion.py # AI总结功能主程序
├── api_config.py         # API配置管理工具
├── setup.py              # 环境配置与初始化脚本
├── api_keys.ini          # API密钥配置文件(通过 setup.py 自动生成)
├── filter_keywords.txt   # 过滤规则配置文件
├── inputs/               # 输入文件目录
├── outputs/              # 清理后的输出文件目录
└── conclusion/           # AI总结生成的文件目录
```

## 实现效果

示例文件位于 `inputs/`、`outputs/`、`conclusion/`中。

## 🚀 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/JyiDeng/QQ-Summary-Genius.git
```

2. 运行初始化脚本（推荐）：
```bash
python setup.py
```
这将自动创建所需目录、安装依赖，并引导你配置 API 密钥、系统提示词。

或者，你也可以手动完成这些步骤：

3. 准备聊天记录：
   - 将QQ聊天记录文件放入 `inputs` 目录
     - 聊天记录导出：可以使用怀旧版QQ（官网下载，不带NT架构字样，可参考[(https://dldir1.qq.com/qqfile/qq/PCQQ9.7.23/QQ9.7.23.29400.exe)](https://dldir1.qq.com/qqfile/qq/PCQQ9.7.23/QQ9.7.23.29400.exe) ），右键单击群聊，点击`查看消息记录`，进入`消息管理器`，右键单击某个群聊，点击`导出消息记录`; 
     - 选择`txt`文件格式，导出文件到`./inputs`文件夹
   <!-- - 确保文件使用 UTF-8 编码 -->

4. 运行聊天记录清理程序：（具体参数配置见后文）

```bash
python process_chat_logs.py
```

5. 配置 AI API 密钥：

```bash
python api_config.py
```

或者
```bash
python generate_conclusion.py -c
```

或者，打开`J:\Project_Playground\qq_chat_ai_conclusion\api_keys.ini`，设置 API。

6. 选择模型：

打开`J:\Project_Playground\qq_chat_ai_conclusion\api_keys.ini`，设置对应 API 的模型。


7. 运行AI总结程序：（具体参数配置见后文）
```bash
python generate_conclusion.py
```

预处理后的文件将保存在 `outputs` 目录，文件名格式为：`cleaned_原文件名_日期范围.txt`
总结文件将保存在 `conclusion` 目录，文件名格式为：`conclusion_原文件名_日期范围.md`

## 📖 详细使用说明


### Step 1. 聊天记录清理 - 命令行参数

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

### Step 2. AI 总结 - 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-f, --file` | 指定要总结的文件 | `-f "outputs/cleaned_example.txt"` |
| `-d, --input-dir` | 指定要处理的文件目录，默认为outputs | `-d "outputs"` |
| `-o, --output-dir` | 指定总结文件输出目录，默认为conclusion | `-o "conclusion"` |
| `-a, --api` | 指定要使用的API源，可多选，默认为siliconflow | `-a siliconflow openai anthropic` |
| `-p, --prompt` | 自定义提示词 | `-p "请总结以下内容的主要话题："` |
| `-c, --config` | 配置API密钥 | `-c` |
| `-m, --model` | 指定要使用的SiliconFlow模型名称 | `-m "qwen/Qwen2.5-7B-Chat"` |
| `-s, --system-prompt` | 设置系统提示词 | `-s "你是一个专业的会议纪要整理专家"` |

#### 系统提示词配置

程序使用的默认系统提示词为：
```
你是一个专业的聊天内容分析助手。你的任务是对QQ聊天记录进行简明扼要的总结，提取主要话题和关键信息。格式上，按照时间顺序划分小标题，总结各个话题主要内容。
```

你可以通过以下两种方式自定义系统提示词：

1. **使用setup.py配置（推荐）**：
   运行 `python setup.py` 并按照提示修改系统提示词。

2. **直接编辑文件**：
   修改 `generate_conclusion.py` 文件中的 `SYSTEM_PROMPT` 常量。

#### 基本用例

```bash
# 使用默认API源(SiliconFlow)处理outputs目录下的所有文件
python generate_conclusion.py

# 处理单个文件
python generate_conclusion.py -f "outputs/cleaned_example.txt"

# 使用多个API源进行总结
python generate_conclusion.py -a siliconflow openai anthropic

# 自定义提示词
python generate_conclusion.py -p "请分析并总结以下聊天内容的核心观点："

# 指定使用的模型
python generate_conclusion.py -m "qwen/Qwen2.5-72B-Chat"
```

#### API 配置说明

程序提供了两种方式配置API密钥：

1. **交互式配置（推荐）**：
   ```bash
   python generate_conclusion.py -c
   ```
   或者
   ```bash
   python api_config.py
   ```
   这将启动交互式配置向导，引导你输入各个API的密钥。


2. **手动编辑配置文件**：
   配置文件保存在 `api_keys.ini`，你可以直接编辑此文件设置密钥：
   ```ini
   [siliconflow]
   api_key = your_api_key_here
   api_url = https://api.siliconflow.cn/v1/chat/completions
   model = deepseek-ai/DeepSeek-R1-Distill-Qwen-7B


   [openai]
   api_key = your_api_key_here
   api_url = https://api.openai.com/v1/chat/completions
   model = gpt-3.5-turbo

   [anthropic]
   api_key = your_api_key_here
   api_url = https://api.anthropic.com/v1/messages
   model = claude-3-sonnet-20240229
   ```

#### 模型选择 - 以 SiliconFlow 为例

以 SiliconFlow 平台为例，它提供了多种可用模型，我们在此需要选择：

- **DeepSeek**：`Pro/deepseek-ai/DeepSeek-R1`、`deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`（默认使用的模型）等
- **Qwen**：`Qwen/Qwen2.5-72B-Instruct-128K`、`Qwen/Qwen2.5-Coder-7B-Instruct`等
- **internlm**：`internlm/internlm2_5-7b-chat`、`internlm/internlm2_5-20b-chat`等
- **BAAI**：`BAAI/bge-large-zh-v1.5`等
- **THUDM**：`THUDM/glm-4-9b-chat`等
- ...(其他模型)

你可以通过以下方式指定模型：
```bash
# A. 使用命令行参数指定
python generate_conclusion.py -m "Qwen/Qwen2.5-Coder-7B-Instruct"

# B. 在api_keys.ini文件中修改model字段
```
或在`api_keys.ini`文件中修改model字段。

如果报错为模型不存在，可能是以上模型过期，请查阅SiliconFlow官方文档获取最新的模型列表。

### ⚙️ 自定义过滤规则

在 `filter_keywords.txt` 中添加过滤规则，每行一个：

```text
# 普通文本
Q群管家
[图片]

# 正则表达式（以 \ 开头）
\[表情\]
\[流泪\].*
```

等等。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个工具！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件