

I will create a comprehensive README in both English and Chinese for the advanced Telegram AI Image Generation Bot.

# Advanced Telegram AI Image Generation Bot

## English Documentation

### Overview
This Telegram bot leverages fal.ai's Stable Diffusion API to create high-quality AI-generated images. It supports both text-to-image generation and advanced image-to-image transformations using ControlNet and IP-Adapter technologies.

### Features
- **Text-to-Image Generation**: Create images from detailed text prompts
- **ControlNet Image Transformation**: Transform your images using different ControlNet modes:
  - Edge Detection (Canny): Preserves edges from the original image
  - Depth Map: Maintains the 3D structure of the original image
  - Pose Detection: Preserves human poses from the original image
  - Line Art: Creates images based on line drawings
- **IP-Adapter**: Generate new images that retain the style and content of a reference image
- **Customizable Parameters**: Fine-tune the generation with additional parameters
- **Intuitive Conversation Flow**: Easy-to-follow step-by-step process for image generation

### Setup Instructions

1. **Clone the Repository**
   ```
   git clone https://github.com/chunzhimoe/chilloutai-bot
   cd telegram-ai-image-bot
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   
   Create a `.env` file in the project directory with the following:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   FAL_KEY=your_fal_ai_api_key
   ```

   - To get a Telegram bot token, talk to [@BotFather](https://t.me/BotFather) on Telegram
   - For a fal.ai API key, sign up at [fal.ai](https://fal.ai)

4. **Run the Bot**
   ```
   python main.py
   ```

### Usage Guide

#### Basic Commands
- `/start` - Start the bot and receive a welcome message
- `/help` - Display the help menu with available commands
- `/generate [prompt]` - Generate an image from text
- `/controlnet` - Start the ControlNet image-to-image flow
- `/ipadapter` - Start the IP-Adapter image-to-image flow
- `/cancel` - Cancel the current operation

#### Text-to-Image Generation
1. Simply send any text message or use `/generate [prompt]`
2. The bot will process your prompt and generate an image

#### Using Additional Parameters
You can add parameters to your prompts for fine-tuned control:
```
/generate a beautiful sunset over mountains --steps 30 --guidance 7.5
```

Common parameters:
- `--steps` (or `num_inference_steps`): Number of denoising steps (higher = more detail but slower)
- `--guidance` (or `guidance_scale`): How closely to follow the prompt (higher = more adherence)
- `--images` (or `num_images`): Number of images to generate

#### ControlNet Image Transformation
1. Type `/controlnet`
2. Upload an image
3. Select a ControlNet mode from the options
4. Enter a text prompt
5. The bot will transform your image according to the prompt and selected mode

#### IP-Adapter Image Transformation
1. Type `/ipadapter`
2. Upload a reference image
3. Enter a text prompt
4. The bot will generate a new image influenced by both the prompt and the style/content of your reference image

### Project Structure
- `main.py`: Entry point for the bot
- `config.py`: Configuration settings and environment variables
- `bot_handlers.py`: Telegram bot command handlers
- `fal_client_wrapper.py`: Wrapper for fal.ai API calls
- `user_state.py`: Handle user conversation states

### Deployment
For production deployment, consider using:
- [Heroku](https://heroku.com)
- [PythonAnywhere](https://pythonanywhere.com)
- [AWS EC2](https://aws.amazon.com/ec2/)
- [Google Cloud Run](https://cloud.google.com/run)

Be sure to set environment variables on your hosting platform.

---

## 中文文档

### 概述
这个 Telegram 机器人利用 fal.ai 的 Stable Diffusion API 创建高质量的 AI 生成图像。它支持文本到图像的生成和使用 ControlNet 与 IP-Adapter 技术进行高级图像到图像的转换。

### 功能特色
- **文本到图像生成**：通过详细的文本提示创建图像
- **ControlNet 图像转换**：使用不同的 ControlNet 模式转换您的图像：
  - 边缘检测（Canny）：保留原始图像的边缘
  - 深度图（Depth Map）：维持原始图像的3D结构
  - 姿态检测（Pose）：保留原始图像中的人体姿势
  - 线条艺术（Line Art）：基于线条绘图创建图像
- **IP-Adapter**：生成保留参考图像风格和内容的新图像
- **可自定义参数**：通过额外参数微调生成过程
- **直观的对话流程**：易于遵循的图像生成分步流程

### 设置说明

1. **克隆仓库**
   ```
   git clone https://github.com/chunzhimoe/chilloutai-bot
   cd telegram-ai-image-bot
   ```

2. **安装依赖**
   ```
   pip install -r requirements.txt
   ```

3. **设置环境变量**
   
   在项目目录中创建一个 `.env` 文件，内容如下：
   ```
   TELEGRAM_BOT_TOKEN=你的_telegram_机器人_token
   FAL_KEY=你的_fal_ai_api_密钥
   ```

   - 要获取 Telegram 机器人 token，在 Telegram 上联系 [@BotFather](https://t.me/BotFather)
   - 要获取 fal.ai API 密钥，请在 [fal.ai](https://fal.ai) 注册

4. **运行机器人**
   ```
   python main.py
   ```

### 使用指南

#### 基本命令
- `/start` - 启动机器人并接收欢迎消息
- `/help` - 显示包含可用命令的帮助菜单
- `/generate [提示词]` - 从文本生成图像
- `/controlnet` - 开始 ControlNet 图像到图像流程
- `/ipadapter` - 开始 IP-Adapter 图像到图像流程
- `/cancel` - 取消当前操作

#### 文本到图像生成
1. 只需发送任何文本消息或使用 `/generate [提示词]`
2. 机器人将处理您的提示词并生成图像

#### 使用附加参数
您可以向提示词添加参数以进行精细控制：
```
/generate 山脉上美丽的日落 --steps 30 --guidance 7.5
```

常用参数：
- `--steps`（或 `num_inference_steps`）：去噪步骤数（更高 = 更多细节但更慢）
- `--guidance`（或 `guidance_scale`）：对提示词的遵循程度（更高 = 更严格遵循）
- `--images`（或 `num_images`）：要生成的图像数量

#### ControlNet 图像转换
1. 输入 `/controlnet`
2. 上传一张图像
3. 从选项中选择 ControlNet 模式
4. 输入文本提示词
5. 机器人将根据提示词和所选模式转换您的图像

#### IP-Adapter 图像转换
1. 输入 `/ipadapter`
2. 上传一张参考图像
3. 输入文本提示词
4. 机器人将生成一张受提示词和参考图像风格/内容影响的新图像

### 项目结构
- `main.py`：机器人的入口点
- `config.py`：配置设置和环境变量
- `bot_handlers.py`：Telegram 机器人命令处理程序
- `fal_client_wrapper.py`：fal.ai API 调用的封装器
- `user_state.py`：处理用户对话状态

### 部署
对于生产环境部署，请考虑使用：
- [Heroku](https://heroku.com)
- [PythonAnywhere](https://pythonanywhere.com)
- [AWS EC2](https://aws.amazon.com/ec2/)
- [Google Cloud Run](https://cloud.google.com/run)

请确保在您的托管平台上设置环境变量。

### 注意事项
- 为了最佳性能，建议使用1h2g服务器来托管此机器人
- 确保您的 fal.ai API 密钥有足够的使用配额
- 监控您的使用情况，以避免意外费用
- 根据您的用户群体规模考虑实施速率限制

### 贡献
欢迎贡献！请随时提交问题或拉取请求。

### 许可证
此项目采用 MIT 许可证。
