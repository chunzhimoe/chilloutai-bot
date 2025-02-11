import telegram
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, CallbackContext, ConversationHandler
import requests
import base64
import time
import os
 
# Telegram bot API token
token = "YOUR_TELEGRAM_BOT_API_TOKEN"
 
# Runpod API credentials
runpod_key = "YOUR_RUNPOD_API_KEY"
api_name = "YOUR_RUNPOD_API_NAME"
 
# Define conversation state constants
PROMPT, NEGATIVE_PROMPT = range(2)
 
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello, I am a bot that can generate images ! To generate an image, '
                              'send me a message in the following format: \n\n /generate')
 
def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('To generate an image, send me a message in the following format: \n\n /generate')
 
def generate(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask the user for the prompt."""
    update.message.reply_text("Please enter the prompt:")
    return PROMPT
 
def prompt_callback(update: Update, context: CallbackContext) -> int:
    """Process the user's prompt and ask for the negative prompt."""
    prompt_text = update.message.text
    context.user_data['prompt'] = prompt_text
    update.message.reply_text(
        'Please enter the negative prompt (or type /skip):'
    )
    return NEGATIVE_PROMPT
 
def negative_prompt_callback(update: Update, context: CallbackContext) -> None:
    """Process the user's negative prompt and generate the image."""
    text = update.message.text
    if text != "/skip":
        context.user_data['negative_prompt'] = text
 
    # Make a request to the Runpod API
    res = requests.post(f'https://api.runpod.ai/v2/{api_name}/run', headers={
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {runpod_key}"
    }, json={
        "input": {"prompt": context.user_data['prompt'], "steps": 28, "negative_prompt": context.user_data.get('negative_prompt', ''), "width": 512, "height": 768, "sampler_index": "DPM++ SDE Karras",
                  "batch_size": 1, "seed": -1},
    })
 
    task_id = res.json()['id']
 
    while True:
        res = requests.get(f'https://api.runpod.ai/v2/{api_name}/status/{task_id}', headers={
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {runpod_key}"
        })
 
        status = res.json()['status']
        if status == 'COMPLETED':
            for imgstring in res.json()['output']['images']:
                # Create a unique filename for the image by including the current timestamp
                filename = f"test_{time.time()}.png"
                with open(filename, "wb") as fh:
                    imgdata = base64.b64decode(imgstring)
                    fh.write(imgdata)
 
                # Send the image back to the user on Telegram
                chat_id = update.message.chat_id
                context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))
 
                # Delete the local image file
                os.remove(filename)
            break
 
        if status == 'FAILED':
            update.message.reply_text("Sorry, there was an error generating the image.")
            break
 
        time.sleep(10)
 
    # Clear the conversation state
    context.user_data.clear()
    return ConversationHandler.END
 
def cancel(update: Update, context: CallbackContext) -> None:
    """Cancel the conversation and clear the conversation state."""
    update.message.reply_text("Conversation cancelled.")
    context.user_data.clear()
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it the bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Define conversation handler to handle prompts
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('generate', generate)],
        states={
            PROMPT: [MessageHandler(Filters.text & ~Filters.command, prompt_callback)],
            NEGATIVE_PROMPT: [MessageHandler(Filters.text & ~Filters.command, negative_prompt_callback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Define command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
