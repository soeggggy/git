import logging
import requests
import random
import praw
from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    MIKU_SUBREDDITS, WAIFU_PICS_API, ANIME_PICS_API, SAFEBOORU_API
)
import time

logger = logging.getLogger(__name__)

# Initialize Reddit client if credentials are available
reddit_client = None
if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
    try:
        reddit_client = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        logger.info("Reddit client initialized")
    except Exception as e:
        logger.error(f"Error initializing Reddit client: {e}")
        reddit_client = None
else:
    logger.warning("Reddit API credentials not found, Reddit features disabled")

def fetch_image_from_waifu_pics():
    """
    Fetch an anime image from waifu.pics API.
    Will only sometimes return Miku, but is a good fallback.
    
    Returns:
        dict: Contains image_url and source
    """
    try:
        response = requests.get(WAIFU_PICS_API)
        if response.status_code == 200:
            data = response.json()
            return {
                "image_url": data.get("url"),
                "source": "waifu.pics"
            }
    except Exception as e:
        logger.error(f"Error fetching from waifu.pics: {e}")
    return None

def fetch_image_from_waifu_im():
    """
    Fetch an anime image from waifu.im API with Miku tag if possible.
    
    Returns:
        dict: Contains image_url and source
    """
    try:
        params = {"included_tags": "miku_nakano"}
        response = requests.get(ANIME_PICS_API, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'images' in data and len(data['images']) > 0:
                img = data['images'][0]
                return {
                    "image_url": img.get("url"),
                    "source": f"waifu.im - {img.get('source', 'Unknown')}"
                }
    except Exception as e:
        logger.error(f"Error fetching from waifu.im: {e}")
    return None

def fetch_image_from_safebooru():
    """
    Fetch a Miku image from Safebooru.
    
    Returns:
        dict: Contains image_url and source
    """
    try:
        params = {"limit": 100}
        response = requests.get(SAFEBOORU_API, params=params)
        if response.status_code == 200:
            posts = response.json()
            if posts and len(posts) > 0:
                # Select a random post
                post = random.choice(posts)
                # Safebooru image URL format
                image_url = f"https://safebooru.org/images/{post['directory']}/{post['image']}"
                return {
                    "image_url": image_url,
                    "source": f"Safebooru - Post #{post['id']}"
                }
    except Exception as e:
        logger.error(f"Error fetching from Safebooru: {e}")
    return None

def fetch_reddit_post():
    """
    Fetch a Miku-related post from Reddit.
    
    Returns:
        dict: Contains image_url, caption, and source
    """
    if not reddit_client:
        logger.warning("Reddit client not initialized")
        return None
        
    try:
        # Pick a random Miku-related subreddit
        subreddit_name = random.choice(MIKU_SUBREDDITS)
        subreddit = reddit_client.subreddit(subreddit_name)
        
        # Get hot posts from the subreddit
        posts = list(subreddit.hot(limit=50))
        
        # Filter for image posts
        image_posts = [
            post for post in posts 
            if (hasattr(post, 'url') and
                any(post.url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']))
        ]
        
        if not image_posts:
            logger.warning(f"No image posts found in r/{subreddit_name}")
            return None
            
        # Pick a random image post
        post = random.choice(image_posts)
        
        return {
            "image_url": post.url,
            "caption": post.title,
            "source": f"Reddit r/{subreddit_name} - u/{post.author.name}"
        }
        
    except Exception as e:
        logger.error(f"Error fetching from Reddit: {e}")
        return None

def get_random_miku_image():
    """
    Try different sources to get a random Miku image.
    
    Returns:
        dict: Contains image_url and source
    """
    # List of image fetcher functions to try in order
    fetchers = [
        fetch_image_from_waifu_im,  # Try specific Miku images first
        fetch_image_from_safebooru,  # Then try safebooru
        fetch_image_from_waifu_pics  # Fallback to general anime images
    ]
    
    # Shuffle to add more randomness to source selection
    random.shuffle(fetchers)
    
    for fetcher in fetchers:
        result = fetcher()
        if result and 'image_url' in result:
            return result
    
    # If all fetchers fail, return a default error response
    logger.error("All image sources failed")
    return None
