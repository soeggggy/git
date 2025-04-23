import logging
import random
import time
from telegram.ext import Updater
from api_clients import get_random_miku_image, fetch_reddit_post
from facts import get_random_miku_fact, get_random_miku_caption
from handlers import send_post
from storage import add_to_history, is_in_history
from config import (
    MAIN_POST_INTERVAL, IMAGE_POST_INTERVAL, REDDIT_POST_INTERVAL
)
from reddit_tracker import check_for_new_posts, get_batch_posts, initialize_last_post_ids

logger = logging.getLogger(__name__)

def post_miku_fact(context):
    """
    Scheduled job to post a Miku fact with an image.
    """
    try:
        # Get a random fact that hasn't been used recently
        fact = get_random_miku_fact()
        fact_attempts = 0
        max_attempts = 15  # Increased attempts to find unique content
        
        while is_in_history("facts", fact) and fact_attempts < max_attempts:
            fact = get_random_miku_fact()
            fact_attempts += 1
            
        # If we couldn't find a unique fact after many attempts, log and skip this post
        if fact_attempts >= max_attempts and is_in_history("facts", fact):
            logger.warning("Could not find a unique fact after multiple attempts. Skipping post.")
            return
        
        # Get a random image
        image_data = get_random_miku_image()
        if not image_data:
            logger.error("Failed to get a Miku image for fact post")
            return
            
        image_url = image_data["image_url"]
        
        # Create the content package for checking
        content = {
            "image_url": image_url,
            "caption": fact,
            "source": image_data.get("source", "")
        }
        
        # Check if this content is already in history (using enhanced deduplication)
        content_attempts = 0
        while is_in_history("urls", image_url, content) and content_attempts < max_attempts:
            # Try to get a new image
            image_data = get_random_miku_image()
            if not image_data:
                logger.error("Failed to get a unique Miku image after multiple attempts")
                break
                
            image_url = image_data["image_url"]
            content = {
                "image_url": image_url,
                "caption": fact,
                "source": image_data.get("source", "")
            }
            content_attempts += 1
            
        # If we still have a duplicate after many attempts, log and skip
        if content_attempts >= max_attempts and is_in_history("urls", image_url, content):
            logger.warning("Could not create unique content after multiple attempts. Skipping post.")
            return
        
        # Log that we're sending non-duplicate content
        logger.info(f"Sending fact post with unique content (attempts: facts={fact_attempts}, images={content_attempts})")
        
        # Send the post
        send_post(context, content)
        
        # Record used content in history with enhanced tracking
        add_to_history("facts", fact)
        add_to_history("urls", image_url, content)
        
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
        
        # Create the content package
        content = {
            "image_url": image_url,
            "caption": caption,
            "source": image_data.get("source", "")
        }
        
        # Check if this content is already in history using enhanced checks
        max_attempts = 15
        content_attempts = 0
        
        while is_in_history("urls", image_url, content) and content_attempts < max_attempts:
            # Try to get a new image
            image_data = get_random_miku_image()
            if not image_data:
                logger.error("Failed to get a unique Miku image after multiple attempts")
                break
                
            image_url = image_data["image_url"]
            # Update the content with the new image
            content = {
                "image_url": image_url,
                "caption": caption,
                "source": image_data.get("source", "")
            }
            content_attempts += 1
            
        # If we still have a duplicate after many attempts, log and skip
        if content_attempts >= max_attempts and is_in_history("urls", image_url, content):
            logger.warning("Could not create unique image content after multiple attempts. Skipping post.")
            return
            
        # Log that we're sending non-duplicate content
        logger.info(f"Sending image post with unique content (attempts: {content_attempts})")
        
        # Send the post
        send_post(context, content)
        
        # Record used content in history with enhanced tracking
        add_to_history("urls", image_url, content)
        
    except Exception as e:
        logger.error(f"Error in post_miku_image: {e}")

def post_reddit_miku(context):
    """
    Scheduled job to post Miku content from Reddit.
    Gets a batch of posts every 10 minutes.
    """
    try:
        # Get a batch of Reddit posts (up to 3 at a time)
        batch_posts = get_batch_posts(max_posts=3)
        
        if not batch_posts:
            logger.info("No new Reddit posts to share at this time")
            return
        
        posted_count = 0    
        for post in batch_posts:
            # Double-check post isn't already in history before sending
            # (This is a safety check in case the batch getter missed a duplicate)
            if is_in_history("urls", post["image_url"], post):
                logger.info(f"Skipping already posted Reddit content: {post.get('id', 'unknown')} (URL: {post['image_url'][:30]}...)")
                continue
                
            # Send the post
            send_post(context, post)
            
            # Record used content in history with enhanced tracking
            add_to_history("urls", post["image_url"], post)
            
            # If the post has an ID, add it specifically
            if "id" in post:
                add_to_history("post_ids", post["id"])
            
            posted_count += 1
            
            # Small delay between posts to avoid flooding
            time.sleep(1)
        
        if posted_count > 0:
            logger.info(f"Posted {posted_count} Reddit posts in batch")
        else:
            logger.info("No new unique Reddit posts to share (all were duplicates)")
        
    except Exception as e:
        logger.error(f"Error in post_reddit_miku: {e}")

def check_new_reddit_posts(context):
    """
    Frequently checks for new Reddit posts and posts them immediately.
    This allows us to post new content as soon as it appears.
    """
    try:
        # Check for new posts
        new_posts = check_for_new_posts()
        
        if not new_posts:
            return
        
        logger.info(f"Found {len(new_posts)} potential new Reddit posts")
        
        posted_count = 0
        for post in new_posts:
            # Double-check post isn't already in history
            if is_in_history("urls", post["image_url"], post):
                logger.info(f"Skipping already posted Reddit content: {post.get('id', 'unknown')}")
                continue
                
            # Send the post
            send_post(context, post)
            
            # Record used content in history with enhanced tracking
            add_to_history("urls", post["image_url"], post)
            
            # If the post has an ID, add it specifically
            if "id" in post:
                add_to_history("post_ids", post["id"])
                
            posted_count += 1
            
            # Small delay between posts to avoid flooding
            time.sleep(1)
            
        if posted_count > 0:
            logger.info(f"Posted {posted_count} new Reddit posts")
        
    except Exception as e:
        logger.error(f"Error in check_new_reddit_posts: {e}")

def setup_scheduler(updater: Updater):
    """
    Set up the scheduler for regular posts.
    
    Args:
        updater: The Telegram bot updater
    """
    job_queue = updater.job_queue
    
    # Initialize Reddit tracking
    initialize_last_post_ids()
    
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
    
    # Schedule Reddit batch posts every 10 minutes
    job_queue.run_repeating(
        post_reddit_miku,
        interval=600,  # 10 minutes in seconds
        first=60  # Start after 1 minute
    )
    
    # Schedule frequent checks for new Reddit posts (every 2 minutes)
    job_queue.run_repeating(
        check_new_reddit_posts,
        interval=120,  # 2 minutes in seconds
        first=30  # Start after 30 seconds
    )
    
    logger.info("Scheduler set up successfully")
