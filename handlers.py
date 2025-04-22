import logging
from telegram import Update
from config import DEFAULT_CHANNEL
import sys

logger = logging.getLogger(__name__)

def send_post(context, content: dict):
    """
    Send a post to the target channel or chat.
    
    Args:
        context: The context from the scheduler
        content: Dict containing 'image_url', 'caption', and 'source'
    """
    try:
        # Use DEFAULT_CHANNEL from config as channel username
        channel = DEFAULT_CHANNEL
        if not channel:
            logger.error("No channel username provided for posting! Set TELEGRAM_CHANNEL_USERNAME in environment variables.")
            return
            
        # Make sure the channel name starts with @ if it doesn't already
        if not channel.startswith('@'):
            channel = '@' + channel
            
        # Add hashtags and source attribution to the caption
        full_caption = f"{content['caption']}\n\n"
        
        if 'source' in content and content['source']:
            full_caption += f"Source: {content['source']}\n"
            
        full_caption += "#NakanoMiku #Miku #GotoubunNoHanayome #QuintessentialQuintuplets"
        
        # Get bot instance and send the photo
        bot = None
        if hasattr(context, 'bot'):
            bot = context.bot
            
        if not bot:
            logger.error("Could not get bot instance!")
            return
            
        # Send the image with caption
        bot.send_photo(
            chat_id=channel,
            photo=content['image_url'],
            caption=full_caption
        )
        logger.info(f"Posted content: {content['image_url'][:30]}...")
        
    except Exception as e:
        logger.error(f"Error sending post: {e}")
