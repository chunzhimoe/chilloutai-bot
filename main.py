import logging
import os
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, CallbackQueryHandler
)
from config import TELEGRAM_BOT_TOKEN
from bot_handlers import (
    start_command, help_command, generate_command, text_message,
    controlnet_command, ipadapter_command, cancel_command,
    photo_message, button_callback
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Application instance
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CommandHandler("controlnet", controlnet_command))
    application.add_handler(CommandHandler("ipadapter", ipadapter_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    application.add_handler(MessageHandler(filters.PHOTO, photo_message))
    
    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
