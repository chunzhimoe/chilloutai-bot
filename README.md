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
   git clone https://github.com/your-username/telegram-ai-image-bot.git
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
