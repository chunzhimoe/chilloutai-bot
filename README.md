# aidrawbot

bot.py是一个使用 Python 语言编写的 Telegram bot，它使用 Runpod AI API 生成图像。该代码包含以下主要组件和功能：

- 加载 Telegram bot API token 和 Runpod API 凭据
- 提供 `start` 和 `help` 命令，用于帮助用户快速了解如何使用该 bot
- 提供 `generate` 命令，用于启动对话并开始生成图像的流程
- 定义了一个 `ConversationHandler`，用于处理用户输入的 `prompt` 和 `negative_prompt`，以确保输入正确。`cancel` 函数用于清除 conversation state 并取消对话。
- 提供 `prompt_callback` 和 `negative_prompt_callback` 函数，用于处理用户的 `prompt` 和 `negative_prompt`，并向用户发送生成的图像。
- 启动 Telegram bot 并运行代码。

该代码使用 `requests` 库向 Runpod API 发送 POST 请求，将用户输入传递到 API 并生成图像，将图像返回并显示在用户的 Telegram 应用中。该代码还使用 `base64` 库将生成的图像转换为字符串，方便于传输，并使用 `time` 和 `os` 库对输出进行管理。
powered by chatgpt

你需要做的:
##1.申请telegrambot api
telegram @BotFather
