import json
import os
import logging
import hashlib
import re
import urllib.parse
from config import HISTORY_FILE

logger = logging.getLogger(__name__)

def load_post_history():
    """
    Load the post history from a JSON file.
    
    Returns:
        dict: The post history or an empty dict if the file doesn't exist
    """
    if not os.path.exists(HISTORY_FILE):
        return {
            "urls": [], 
            "facts": [], 
            "content_hashes": [], 
            "image_fingerprints": [],
            "post_ids": []
        }
    
    try:
        with open(HISTORY_FILE, 'r') as file:
            history = json.load(file)
            
            # Make sure all needed categories exist
            if "content_hashes" not in history:
                history["content_hashes"] = []
            if "image_fingerprints" not in history:
                history["image_fingerprints"] = []
            if "post_ids" not in history:
                history["post_ids"] = []
                
            return history
    except Exception as e:
        logger.error(f"Error loading post history: {e}")
        return {
            "urls": [], 
            "facts": [], 
            "content_hashes": [], 
            "image_fingerprints": [],
            "post_ids": []
        }

def save_post_history(history):
    """
    Save the post history to a JSON file.
    
    Args:
        history (dict): The post history to save
    """
    try:
        with open(HISTORY_FILE, 'w') as file:
            json.dump(history, file)
    except Exception as e:
        logger.error(f"Error saving post history: {e}")

def normalize_url(url):
    """
    Normalize a URL by removing query parameters and standardizing the format.
    This helps catch duplicate URLs that appear different but point to the same content.
    
    Args:
        url (str): The URL to normalize
        
    Returns:
        str: The normalized URL
    """
    if not url:
        return url
        
    try:
        # Parse the URL
        parsed = urllib.parse.urlparse(url)
        
        # Remove any query parameters, keeping only the path
        normalized = urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            None,
            None,
            None
        ))
        
        # Remove trailing slashes
        if normalized and normalized[-1:] == "/":
            normalized = normalized[:-1]
        
        # Convert to lowercase
        normalized = normalized.lower()
        
        return normalized
    except Exception as e:
        logger.warning(f"Error normalizing URL {url}: {e}")
        return url

def create_content_hash(content_dict):
    """
    Create a hash of content to identify duplicates even if URLs are different.
    
    Args:
        content_dict (dict): Dict containing post content like image_url, caption, etc.
        
    Returns:
        str: A hash string uniquely identifying the content
    """
    if not content_dict:
        return None
        
    try:
        # Create a standardized string representation of the content
        hash_components = []
        
        # Add the normalized URL
        if 'image_url' in content_dict:
            hash_components.append(f"url:{normalize_url(content_dict['image_url'])}")
            
        # Add the caption without spaces and punctuation (for fuzzy matching)
        if 'caption' in content_dict and content_dict['caption']:
            # Remove punctuation and whitespace, convert to lowercase
            cleaned_caption = re.sub(r'[^\w]', '', content_dict['caption'].lower())
            hash_components.append(f"caption:{cleaned_caption}")
            
        # Add source if available
        if 'source' in content_dict and content_dict['source']:
            hash_components.append(f"source:{content_dict['source']}")
            
        # Generate the hash
        if hash_components:
            content_str = "|".join(hash_components)
            return hashlib.md5(content_str.encode()).hexdigest()
            
    except Exception as e:
        logger.error(f"Error creating content hash: {e}")
        
    return None

def add_to_history(item_type, item_content, content_dict=None):
    """
    Add an item to the post history.
    
    Args:
        item_type (str): The type of item ('urls', 'facts', etc.)
        item_content (str): The content to add
        content_dict (dict, optional): Full content dictionary for hash generation
    """
    history = load_post_history()
    
    # Ensure the type exists in history
    if item_type not in history:
        history[item_type] = []
    
    # Add the item if it's not already there
    if item_content not in history[item_type]:
        history[item_type].append(item_content)
        
        # Limit the history size to prevent unlimited growth
        max_history = 1000  # Increased from 500 to store more history
        if len(history[item_type]) > max_history:
            history[item_type] = history[item_type][-max_history:]
        
        # If this is a URL, normalize it and add that too
        if item_type == "urls":
            normalized_url = normalize_url(item_content)
            if normalized_url and normalized_url != item_content:
                if "normalized_urls" not in history:
                    history["normalized_urls"] = []
                if normalized_url not in history["normalized_urls"]:
                    history["normalized_urls"].append(normalized_url)
        
        # If we have the full content dict, create and store a content hash
        if content_dict:
            content_hash = create_content_hash(content_dict)
            if content_hash and "content_hashes" in history and content_hash not in history["content_hashes"]:
                history["content_hashes"].append(content_hash)
                
            # If it's a Reddit post, store the post ID too
            if "id" in content_dict:
                post_id = content_dict["id"]
                if post_id and "post_ids" in history and post_id not in history["post_ids"]:
                    history["post_ids"].append(post_id)
        
        save_post_history(history)

def is_in_history(item_type, item_content, content_dict=None):
    """
    Check if an item is in the post history using multiple methods.
    
    Args:
        item_type (str): The type of item ('urls' or 'facts')
        item_content (str): The content to check
        content_dict (dict, optional): Full content dictionary for hash checking
        
    Returns:
        bool: True if the item is in the history, False otherwise
    """
    history = load_post_history()
    
    # Direct check of the item in the specific history type
    if item_type in history and item_content in history[item_type]:
        logger.info(f"Found direct match for {item_type} in history")
        return True
        
    # For URLs, also check the normalized version
    if item_type == "urls":
        normalized_url = normalize_url(item_content)
        if "normalized_urls" in history and normalized_url in history["normalized_urls"]:
            logger.info(f"Found normalized URL match in history")
            return True
    
    # For content dictionaries, check content hash
    if content_dict:
        content_hash = create_content_hash(content_dict)
        if content_hash and "content_hashes" in history and content_hash in history["content_hashes"]:
            logger.info(f"Found content hash match in history")
            return True
            
        # Check post ID for Reddit content
        if "id" in content_dict:
            post_id = content_dict["id"]
            if post_id and "post_ids" in history and post_id in history["post_ids"]:
                logger.info(f"Found post ID match in history")
                return True
    
    return False
