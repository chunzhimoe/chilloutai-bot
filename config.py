import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Please set the TELEGRAM_BOT_TOKEN environment variable")

# fal.ai API Key
FAL_KEY = os.getenv("FAL_KEY")
if not FAL_KEY:
    raise ValueError("Please set the FAL_KEY environment variable")

# Set fal.ai key as environment variable for the fal-client
os.environ["FAL_KEY"] = FAL_KEY

# Default model
DEFAULT_MODEL = "fal-ai/stable-diffusion-v35-large"

# Default parameters for image generation
DEFAULT_PARAMS = {
    "negative_prompt": "",
    "num_inference_steps": 28,
    "guidance_scale": 3.5,
    "num_images": 1,
    "enable_safety_checker": True,
    "output_format": "jpeg",
    "image_size": "landscape_4_3"
}

# ControlNet paths
CONTROLNET_MODELS = {
    "canny": "lllyasviel/control_v11p_sd15_canny",
    "depth": "lllyasviel/control_v11f1p_sd15_depth",
    "pose": "lllyasviel/control_v11p_sd15_openpose",
    "line": "lllyasviel/control_v11p_sd15_lineart",
}

# IP-Adapter paths
IP_ADAPTER_CONFIG = {
    "path": "ip-adapter/sdxl-ip-adapter",
    "image_encoder_path": "openai/clip-vit-large-patch14",
    "scale": 0.5
}

# Maximum prompt length
MAX_PROMPT_LENGTH = 1000

# Help message
HELP_MESSAGE = """
*AI Image Generation Bot*

This bot uses fal.ai's Stable Diffusion to generate images from text and image inputs.

*Text to Image Commands:*
/start - Start the bot
/help - Show this help message
/generate [prompt] - Generate image from text prompt

*Image to Image Commands:*
/controlnet - Start ControlNet image-to-image flow
/ipadapter - Start IP-Adapter image-to-image flow
/cancel - Cancel the current operation

*ControlNet Modes:*
After sending /controlnet and uploading an image, you can choose from these modes:
- canny - Edge detection
- depth - 3D depth map
- pose - Human pose detection
- line - Line art

*Basic Usage:*
1. Simply send any text to generate an image from text
2. Use /controlnet or /ipadapter, then upload an image and follow instructions

*Advanced Usage:*
You can set parameters like this:
/generate a beach at sunset --steps 30 --guidance 7.5
"""

# Cancel message
CANCEL_MESSAGE = "Operation cancelled. What would you like to do next?"

# Temporary file storage
TEMP_DIRECTORY = "temp_images"
os.makedirs(TEMP_DIRECTORY, exist_ok=True)
