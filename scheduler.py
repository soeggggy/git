import logging
import random
from telegram.ext import Updater
from api_clients import get_random_miku_image, fetch_reddit_post
from facts import get_random_miku_fact, get_random_miku_caption
from handlers import send_post
from storage import add_to_history, is_in_history
from config import (
    MAIN_POST_INTERVAL, IMAGE_POST_INTERVAL, REDDIT_POST_INTERVAL
)

logger = logging.getLogger(__name__)

def post_miku_fact(context):
    """
    Scheduled job to post a Miku fact with an image.
    """
    try:
        # Get a random fact that hasn't been used recently
        fact = get_random_miku_fact()
        fact_attempts = 0
        max_attempts = 10
        
        while is_in_history("facts", fact) and fact_attempts < max_attempts:
            fact = get_random_miku_fact()
            fact_attempts += 1
        
        # Get a random image
        image_data = get_random_miku_image()
        if not image_data:
            logger.error("Failed to get a Miku image for fact post")
            return
            
        image_url = image_data["image_url"]
        
        # Check if this image URL has been used before
        image_attempts = 0
        while is_in_history("urls", image_url) and image_attempts < max_attempts:
            image_data = get_random_miku_image()
            if not image_data:
                logger.error("Failed to get a unique Miku image after multiple attempts")
                break
            image_url = image_data["image_url"]
            image_attempts += 1
            
        # Create the content package
        content = {
            "image_url": image_url,
            "caption": fact,
            "source": image_data.get("source", "")
        }
        
        # Send the post
        send_post(context, content)
        
        # Record used content in history
        add_to_history("facts", fact)
        add_to_history("urls", image_url)
        
    except Exception as e:
        logger.error(f"Error in post_miku_fact: {e}")

def post_miku_image(context):
    """
    Scheduled job to post just a Miku image with a short caption.
    """
    try:
        # Get a random caption
        caption = get_random_miku_caption()
        
        # Get a random image
        image_data = get_random_miku_image()
        if not image_data:
            logger.error("Failed to get a Miku image for image post")
            return
            
        image_url = image_data["image_url"]
        
        # Check if this image URL has been used before
        max_attempts = 10
        image_attempts = 0
        while is_in_history("urls", image_url) and image_attempts < max_attempts:
            image_data = get_random_miku_image()
            if not image_data:
                logger.error("Failed to get a unique Miku image after multiple attempts")
                break
            image_url = image_data["image_url"]
            image_attempts += 1
            
        # Create the content package
        content = {
            "image_url": image_url,
            "caption": caption,
            "source": image_data.get("source", "")
        }
        
        # Send the post
        send_post(context, content)
        
        # Record used content in history
        add_to_history("urls", image_url)
        
    except Exception as e:
        logger.error(f"Error in post_miku_image: {e}")

def post_reddit_miku(context):
    """
    Scheduled job to post Miku content from Reddit.
    """
    try:
        # Fetch a Miku post from Reddit
        reddit_post = fetch_reddit_post()
        if not reddit_post:
            logger.error("Failed to get a Reddit Miku post")
            return
            
        image_url = reddit_post["image_url"]
        
        # Check if this image URL has been used before
        max_attempts = 5
        image_attempts = 0
        while is_in_history("urls", image_url) and image_attempts < max_attempts:
            reddit_post = fetch_reddit_post()
            if not reddit_post:
                logger.error("Failed to get a unique Reddit Miku post after multiple attempts")
                break
            image_url = reddit_post["image_url"]
            image_attempts += 1
            
        # Send the post
        send_post(context, reddit_post)
        
        # Record used content in history
        add_to_history("urls", image_url)
        
    except Exception as e:
        logger.error(f"Error in post_reddit_miku: {e}")

def setup_scheduler(updater: Updater):
    """
    Set up the scheduler for regular posts.
    
    Args:
        updater: The Telegram bot updater
    """
    job_queue = updater.job_queue
    
    # Schedule the main posts every 30 minutes
    job_queue.run_repeating(
        post_miku_fact,
        interval=MAIN_POST_INTERVAL,
        first=5  # Start after 5 seconds
    )
    
    # Schedule image posts every 15 minutes (offset by 7.5 minutes from main posts)
    job_queue.run_repeating(
        post_miku_image,
        interval=IMAGE_POST_INTERVAL,
        first=IMAGE_POST_INTERVAL // 2  # Start halfway between main posts
    )
    
    # Schedule Reddit posts every hour
    job_queue.run_repeating(
        post_reddit_miku,
        interval=REDDIT_POST_INTERVAL,
        first=REDDIT_POST_INTERVAL // 4  # Start after 15 minutes
    )
    
    logger.info("Scheduler set up successfully")
