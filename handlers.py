import logging
import os
import tempfile
import requests
from telegram import Update, InputFile
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
            
        try:
            # First download the image to a temporary file
            image_url = content['image_url']
            logger.info(f"Downloading image from: {image_url[:50]}...")
            
            # Create a temporary file
            temp_file = None
            try:
                # Download the image
                response = requests.get(image_url, stream=True, timeout=10)
                response.raise_for_status()  # Raise error for bad status codes
                
                # Get file extension from content type if possible
                content_type = response.headers.get('content-type', '')
                extension = '.jpg'  # Default extension
                if 'png' in content_type:
                    extension = '.png'
                elif 'gif' in content_type:
                    extension = '.gif'
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    extension = '.jpg'
                
                # Create a temporary file with the appropriate extension
                fd, temp_file = tempfile.mkstemp(suffix=extension)
                os.close(fd)  # Close the file descriptor
                
                # Write the image data to the temporary file
                with open(temp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"Image downloaded successfully to: {temp_file}")
                
                # Send the image from the temporary file
                with open(temp_file, 'rb') as photo_file:
                    bot.send_photo(
                        chat_id=channel,
                        photo=InputFile(photo_file),
                        caption=full_caption
                    )
                logger.info(f"Successfully posted content to {channel}")
                
            except requests.exceptions.RequestException as req_err:
                logger.error(f"Error downloading image: {req_err}")
                # Fall back to direct URL if download fails
                logger.info("Falling back to direct URL...")
                bot.send_photo(
                    chat_id=channel,
                    photo=image_url,
                    caption=full_caption
                )
                logger.info(f"Successfully posted content using direct URL to {channel}")
                
            finally:
                # Clean up the temporary file
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                        logger.debug(f"Temporary file {temp_file} removed")
                    except Exception as rm_err:
                        logger.warning(f"Failed to remove temporary file: {rm_err}")
                
        except Exception as e:
            if "Forbidden" in str(e) and "bot is not a member" in str(e):
                logger.error(f"Error: Bot doesn't have permission to post to {channel}. "
                            f"Make sure to add the bot as an administrator to this channel with 'Post Messages' permission.")
            else:
                logger.error(f"Error sending photo: {e}")
        
    except Exception as e:
        logger.error(f"Error sending post: {e}")
