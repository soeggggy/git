import logging
from telegram import Update
from config import DEFAULT_CHANNEL

logger = logging.getLogger(__name__)

def start_command(update, context):
    """
    Handle the /start command.
    Sends a welcome message and instructions to the user.
    """
    update.message.reply_text(
        "Hello! I'm the Nakano Miku Bot! 💙\n\n"
        "I'll be posting Miku content regularly in this chat.\n"
        "Facts and images every 30 minutes, and extra images every 15 minutes!\n\n"
        "Just sit back and enjoy the Miku content! 🎧"
    )

def send_post(context, content: dict):
    """
    Send a post to the target channel or chat.
    
    Args:
        context: The context from the scheduler
        content: Dict containing 'image_url', 'caption', and 'source'
    """
    try:
        chat_id = DEFAULT_CHANNEL or context.job.chat_id
        if not chat_id:
            logger.error("No chat ID provided for posting!")
            return
            
        # Add hashtags and source attribution to the caption
        full_caption = f"{content['caption']}\n\n"
        
        if 'source' in content and content['source']:
            full_caption += f"Source: {content['source']}\n"
            
        full_caption += "#NakanoMiku #Miku #GotoubunNoHanayome #QuintessentialQuintuplets"
        
        # Send the image with caption
        context.bot.send_photo(
            chat_id=chat_id,
            photo=content['image_url'],
            caption=full_caption
        )
        logger.info(f"Posted content: {content['image_url'][:30]}...")
        
    except Exception as e:
        logger.error(f"Error sending post: {e}")
