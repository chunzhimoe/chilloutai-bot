import os
import logging
import re
import uuid
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import (
    HELP_MESSAGE, MAX_PROMPT_LENGTH, TEMP_DIRECTORY, 
    CONTROLNET_MODELS, CANCEL_MESSAGE
)
from fal_client_wrapper import (
    generate_image, upload_image, 
    generate_with_controlnet, generate_with_ip_adapter
)
from user_state import UserState, state_manager

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} started the bot")
    
    # Reset user state
    state_manager.reset_user_state(user.id)
    
    welcome_message = f"Hello {user.first_name}! I'm an AI Image Generation Bot. I can create images from text or transform your images.\n\nUse /help to learn more."
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command"""
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler to cancel the current operation"""
    user = update.effective_user
    logger.info(f"User {user.id} cancelled current operation")
    
    session = state_manager.reset_user_state(user.id)
    
    # Clean up any temporary files
    if session.image_path and os.path.exists(session.image_path):
        try:
            os.remove(session.image_path)
            logger.info(f"Removed temporary file: {session.image_path}")
        except Exception as e:
            logger.error(f"Failed to remove temporary file {session.image_path}: {str(e)}")
    
    await update.message.reply_text(CANCEL_MESSAGE)

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /generate command"""
    user = update.effective_user
    
    # Reset user state
    state_manager.reset_user_state(user.id)
    
    # Check if we have a prompt
    full_text = update.message.text
    text_after_command = full_text.split('/generate', 1)[1].strip()
    
    if not text_after_command:
        await update.message.reply_text("Please provide a prompt after /generate. For example: /generate a sunset over mountains")
        return
    
    # Parse any additional parameters
    prompt, params = parse_additional_parameters(text_after_command)
    
    await process_prompt(update, prompt, params)

async def controlnet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /controlnet command - starts the ControlNet image-to-image flow"""
    user = update.effective_user
    logger.info(f"User {user.id} started ControlNet flow")
    
    # Set user state to wait for image upload
    state_manager.set_user_state(user.id, UserState.WAITING_FOR_IMAGE)
    
    await update.message.reply_text(
        "Please upload an image to use with ControlNet. "
        "This image will be used as a reference for generating a new image. "
        "After uploading, you'll select a ControlNet mode and provide a prompt.\n\n"
        "You can /cancel this operation at any time."
    )

async def ipadapter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /ipadapter command - starts the IP-Adapter image-to-image flow"""
    user = update.effective_user
    logger.info(f"User {user.id} started IP-Adapter flow")
    
    # Set user state to wait for image upload
    state_manager.set_user_state(user.id, UserState.WAITING_FOR_IMAGE, 
                                is_ip_adapter=True)
    
    await update.message.reply_text(
        "Please upload an image to use with IP-Adapter. "
        "IP-Adapter will use the style and content of your image to influence the generation. "
        "After uploading, you'll provide a prompt.\n\n"
        "You can /cancel this operation at any time."
    )

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for text messages"""
    user = update.effective_user
    text = update.message.text
    
    # Skip commands
    if text.startswith('/'):
        return
    
    # Get current user state
    session = state_manager.get_user_session(user.id)
    
    # Handle text based on user's current state
    if session.state == UserState.WAITING_FOR_CONTROLNET_PROMPT:
        await handle_controlnet_prompt(update, text)
    elif session.state == UserState.WAITING_FOR_IPADAPTER_PROMPT:
        await handle_ipadapter_prompt(update, text)
    else:
        # Treat as a normal text-to-image prompt
        prompt, params = parse_additional_parameters(text)
        await process_prompt(update, prompt, params)

async def photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for photos"""
    user = update.effective_user
    logger.info(f"User {user.id} sent a photo")
    
    # Get current user state
    session = state_manager.get_user_session(user.id)
    
    # Check if we're expecting an image
    if session.state != UserState.WAITING_FOR_IMAGE:
        await update.message.reply_text(
            "I noticed you sent an image, but I wasn't expecting one. "
            "If you want to use image-to-image generation, use /controlnet or /ipadapter first."
        )
        return
    
    # Get the photo with the highest resolution
    photo = update.message.photo[-1]
    file_id = photo.file_id
    
    # Send a temporary message to indicate processing
    message = await update.message.reply_text("📥 Downloading your image...")
    
    try:
        # Download the file
        file = await context.bot.get_file(file_id)
        file_extension = os.path.splitext(file.file_path)[1] or ".jpg"
        temp_file_path = os.path.join(TEMP_DIRECTORY, f"{uuid.uuid4()}{file_extension}")
        await file.download_to_drive(temp_file_path)
        
        # Update message
        await message.edit_text("🚀 Uploading to server...")
        
        # Upload the image to fal.ai
        image_url = await upload_image(temp_file_path)
        
        # Store the image URL and path in user session
        if hasattr(session, 'is_ip_adapter') and session.is_ip_adapter:
            # For IP-Adapter flow
            state_manager.set_user_state(user.id, UserState.WAITING_FOR_IPADAPTER_PROMPT, 
                                       image_url=image_url, 
                                       image_path=temp_file_path)
            
            await message.edit_text(
                "✅ Image uploaded successfully!\n\n"
                "Now, please provide a prompt to guide the generation using the style and content of your image."
            )
        else:
            # For ControlNet flow
            state_manager.set_user_state(user.id, UserState.WAITING_FOR_CONTROLNET_TYPE, 
                                       image_url=image_url, 
                                       image_path=temp_file_path)
            
            # Create keyboard for ControlNet types
            keyboard = [
                [
                    InlineKeyboardButton("Edge Detection", callback_data="controlnet_canny"),
                    InlineKeyboardButton("Depth Map", callback_data="controlnet_depth")
                ],
                [
                    InlineKeyboardButton("Pose Detection", callback_data="controlnet_pose"),
                    InlineKeyboardButton("Line Art", callback_data="controlnet_line")
                ],
                [InlineKeyboardButton("Cancel", callback_data="controlnet_cancel")]
            ]
            
            await message.edit_text(
                "✅ Image uploaded successfully!\n\n"
                "Now, please select a ControlNet type:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
    except Exception as e:
        logger.error(f"Error processing image from user {user.id}: {str(e)}")
        await message.edit_text(f"Sorry, there was an error processing your image: {str(e)}")
        
        # Reset user state
        state_manager.reset_user_state(user.id)

async def handle_controlnet_prompt(update: Update, prompt):
    """Process ControlNet prompt and generate image"""
    user = update.effective_user
    session = state_manager.get_user_session(user.id)
    
    if len(prompt) > MAX_PROMPT_LENGTH:
        await update.message.reply_text(f"Your prompt is too long. Please limit it to {MAX_PROMPT_LENGTH} characters.")
        return
    
    # Send a temporary message to indicate processing
    message = await update.message.reply_text("🎨 Generating your image with ControlNet, please wait...")
    
    try:
        # Extract any additional parameters
        parsed_prompt, params = parse_additional_parameters(prompt)
        
        # Generate the image with ControlNet
        result = await generate_with_controlnet(
            parsed_prompt, 
            session.image_url, 
            session.controlnet_type,
            **params
        )
        
        if not result or not result.get("images") or len(result["images"]) == 0:
            await message.edit_text("Sorry, I couldn't generate an image. Please try again with a different prompt or image.")
            return
        
        # Get the first image URL
        image_url = result["images"][0]["url"]
        
        # Send the image
        await update.message.reply_photo(
            photo=image_url,
            caption=(
                f"🖼️ Generated with ControlNet ({session.controlnet_type}) from your image and prompt:\n\n"
                f"{parsed_prompt[:100]}{'...' if len(parsed_prompt) > 100 else ''}"
            )
        )
        
        # Delete the temporary message
        await message.delete()
        
        # Reset user state
        state_manager.reset_user_state(user.id)
        
    except Exception as e:
        logger.error(f"Error in ControlNet image generation: {str(e)}")
        await message.edit_text(f"Sorry, an error occurred while generating the image: {str(e)}")
        
        # Reset user state
        state_manager.reset_user_state(user.id)

async def handle_ipadapter_prompt(update: Update, prompt):
    """Process IP-Adapter prompt and generate image"""
    user = update.effective_user
    session = state_manager.get_user_session(user.id)
    
    if len(prompt) > MAX_PROMPT_LENGTH:
        await update.message.reply_text(f"Your prompt is too long. Please limit it to {MAX_PROMPT_LENGTH} characters.")
        return
    
    # Send a temporary message to indicate processing
    message = await update.message.reply_text("🎨 Generating your image with IP-Adapter, please wait...")
    
    try:
        # Extract any additional parameters
        parsed_prompt, params = parse_additional_parameters(prompt)
        
        # Generate the image with IP-Adapter
        result = await generate_with_ip_adapter(
            parsed_prompt, 
            session.image_url,
            **params
        )
        
        if not result or not result.get("images") or len(result["images"]) == 0:
            await message.edit_text("Sorry, I couldn't generate an image. Please try again with a different prompt or image.")
            return
        
        # Get the first image URL
        image_url = result["images"][0]["url"]
        
        # Send the image
        await update.message.reply_photo(
            photo=image_url,
            caption=(
                f"🖼️ Generated with IP-Adapter from your image and prompt:\n\n"
                f"{parsed_prompt[:100]}{'...' if len(parsed_prompt) > 100 else ''}"
            )
        )
        
        # Delete the temporary message
        await message.delete()
        
        # Reset user state
        state_manager.reset_user_state(user.id)
        
    except Exception as e:
        logger.error(f"Error in IP-Adapter image generation: {str(e)}")
        await message.edit_text(f"Sorry, an error occurred while generating the image: {str(e)}")
        
        # Reset user state
        state_manager.reset_user_state(user.id)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    data = query.data
    
    # Handle ControlNet type selection
    if data.startswith("controlnet_"):
        controlnet_type = data.split("controlnet_")[1]
        
        if controlnet_type == "cancel":
            # Cancel operation
            session = state_manager.reset_user_state(user.id)
            
            # Clean up temporary file
            if session.image_path and os.path.exists(session.image_path):
                try:
                    os.remove(session.image_path)
                except Exception:
                    pass
            
            await query.edit_message_text(CANCEL_MESSAGE)
            return
        
        # Set the ControlNet type and wait for prompt
        state_manager.set_user_state(user.id, UserState.WAITING_FOR_CONTROLNET_PROMPT, 
                                   controlnet_type=controlnet_type)
        
        # Update message to ask for prompt
        controlnet_name = {
            "canny": "Edge Detection",
            "depth": "Depth Map", 
            "pose": "Pose Detection",
            "line": "Line Art"
        }.get(controlnet_type, controlnet_type)
        
        await query.edit_message_text(
            f"You've selected {controlnet_name} ControlNet.\n\n"
            "Now, please provide a prompt to guide the image generation. "
            "This prompt will be used along with your image's structural information to create a new image.\n\n"
            "You can add parameters to your prompt using this syntax:\n"
            "--steps 30 --guidance 7.5"
        )

async def process_prompt(update: Update, prompt, params=None):
    """Process the prompt and generate an image"""
    user = update.effective_user
    logger.info(f"User {user.id} requested image generation with prompt: {prompt[:100]}")
    
    if len(prompt) > MAX_PROMPT_LENGTH:
        await update.message.reply_text(f"Your prompt is too long. Please limit it to {MAX_PROMPT_LENGTH} characters.")
        return
    
    # Send a temporary message to indicate processing
    message = await update.message.reply_text("🎨 Generating your image, please wait...")
    
    try:
        # Use any provided parameters
        params = params or {}
        
        # Generate the image
        result = await generate_image(prompt, **params)
        
        if not result or not result.get("images") or len(result["images"]) == 0:
            await message.edit_text("Sorry, I couldn't generate an image. Please try again with a different prompt.")
            return
            
        # Get the first image URL
        image_url = result["images"][0]["url"]
        
        # Send the image
        await update.message.reply_photo(
            photo=image_url,
            caption=f"🖼️ Generated from your prompt:\n\n{prompt[:100]}{'...' if len(prompt) > 100 else ''}"
        )
        
        # Delete the temporary message
        await message.delete()
        
    except Exception as e:
        logger.error(f"Error in image generation: {str(e)}")
        await message.edit_text(f"Sorry, an error occurred while generating the image: {str(e)}")

def parse_additional_parameters(text):
    """Extract additional parameters from the prompt text"""
    # Regular expression to match parameters in format --param value
    param_pattern = r'--([a-zA-Z_]+)\s+([^\s-][^\s]*)'
    
    # Find all parameter matches
    params = re.findall(param_pattern, text)
    
    # If parameters found, remove them from the prompt
    if params:
        for name, value in params:
            text = re.sub(f'--{name}\\s+{re.escape(value)}\\s*', '', text)
    
    # Clean up the prompt
    prompt = text.strip()
    
    # Convert parameters to appropriate types
    param_dict = {}
    for name, value in params:
        # Try to convert to appropriate type
        if value.lower() == 'true':
            param_dict[name] = True
        elif value.lower() == 'false':
            param_dict[name] = False
        else:
            try:
                # Try to convert to int
                param_dict[name] = int(value)
            except ValueError:
                try:
                    # Try to convert to float
                    param_dict[name] = float(value)
                except ValueError:
                    # Keep as string
                    param_dict[name] = value
    
    # Handle specific parameters and map them to the API parameters
    api_param_map = {
        'steps': 'num_inference_steps',
        'guidance': 'guidance_scale',
        'images': 'num_images',
    }
    
    # Map parameters to API parameters
    final_params = {}
    for param, value in param_dict.items():
        if param in api_param_map:
            final_params[api_param_map[param]] = value
        else:
            final_params[param] = value
    
    return prompt, final_params
