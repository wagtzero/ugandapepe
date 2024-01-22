import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageDraw
from io import BytesIO

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6450978428:AAGZp-qIBStgmfgf-eS493zH2BqWk72YYgk'

# Replace 'path/to/overlay.png' with the path to your overlay image
OVERLAY_IMAGE_PATH = 'johncena5.png'

# Define the command handler
def jup(update: Update, context: CallbackContext) -> None:
    # Check if the message is a reply to an image
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        # Get the photo file ID
        photo_file_id = update.message.reply_to_message.photo[-1].file_id

        # Get the photo file from Telegram
        photo_file = context.bot.get_file(photo_file_id)
        photo_bytes = photo_file.download_as_bytearray()

        # Open the overlay image
        overlay_image = Image.open(OVERLAY_IMAGE_PATH)

        # Open the original image
        original_image = Image.open(BytesIO(photo_bytes))

        # Resize overlay image to fit the original image
        overlay_image = overlay_image.resize(original_image.size, Image.ANTIALIAS)

        # Apply overlay
        edited_image = Image.alpha_composite(original_image.convert("RGBA"), overlay_image)

        # Convert back to RGB
        edited_image = edited_image.convert("RGB")

        # Save the edited image to a byte array
        edited_image_byte_array = BytesIO()
        edited_image.save(edited_image_byte_array, format='PNG')
        edited_image_byte_array.seek(0)

        # Send the edited image back to the user
        context.bot.send_photo(chat_id=update.message.chat_id, photo=edited_image_byte_array)
    else:
        update.message.reply_text("There's nothing to meme, knucklehead!")

# Set up the updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add command handler for /jup
dispatcher.add_handler(CommandHandler("jup", jup))

# Start the bot
updater.start_polling()

# Run the bot until you send a signal to stop it
updater.idle()