import logging
import os
import sys
from bot import setup_bot
from flask import Flask, render_template, jsonify
import threading

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Main page to show bot status"""
    return render_template('index.html')

@app.route('/status')
def status():
    """API endpoint to check bot status"""
    import os
    from config import DEFAULT_CHANNEL, MAIN_POST_INTERVAL, IMAGE_POST_INTERVAL, REDDIT_POST_INTERVAL
    
    channel = DEFAULT_CHANNEL
    if channel and not channel.startswith('@'):
        channel = '@' + channel
        
    return jsonify({
        "status": "running",
        "bot_name": "Nakano Miku Bot",
        "version": "1.0.0",
        "channel": channel,
        "intervals": {
            "main_fact_interval_minutes": MAIN_POST_INTERVAL // 60,
            "image_interval_minutes": IMAGE_POST_INTERVAL // 60,
            "reddit_interval_minutes": REDDIT_POST_INTERVAL // 60
        },
        "reddit_enabled": bool(os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET"))
    })
    
@app.route('/api/test/post/<post_type>', methods=['GET'])
def test_post(post_type):
    """API endpoint to manually trigger different types of posts"""
    from api_clients import fetch_reddit_post, get_random_miku_image, reddit_client
    from facts import get_random_miku_fact, get_random_miku_caption
    from handlers import send_post
    from bot import get_bot
    
    # Validate post type
    valid_types = ['fact', 'image', 'reddit']
    if post_type not in valid_types:
        return jsonify({
            "success": False,
            "message": f"Invalid post type. Must be one of: {', '.join(valid_types)}"
        }), 400
    
    # Get the bot instance
    bot = get_bot()
    if not bot:
        return jsonify({
            "success": False,
            "message": "Bot not initialized yet. Try again in a few seconds."
        }), 400
    
    # Create a minimal context with the bot
    class MockContext:
        def __init__(self, bot_instance):
            self.bot = bot_instance
    
    context = MockContext(bot)
    
    # Prepare content based on post type
    content = None
    
    if post_type == 'fact':
        # Post a fact with image
        image_data = get_random_miku_image()
        if not image_data:
            return jsonify({
                "success": False,
                "message": "Could not fetch a Miku image. Check logs for details."
            }), 500
            
        content = {
            "image_url": image_data["image_url"],
            "caption": get_random_miku_fact(),
            "source": image_data.get("source", "")
        }
        
    elif post_type == 'image':
        # Post just an image with short caption
        image_data = get_random_miku_image()
        if not image_data:
            return jsonify({
                "success": False,
                "message": "Could not fetch a Miku image. Check logs for details."
            }), 500
            
        content = {
            "image_url": image_data["image_url"],
            "caption": get_random_miku_caption(),
            "source": image_data.get("source", "")
        }
        
    elif post_type == 'reddit':
        # Post from Reddit
        if not reddit_client:
            return jsonify({
                "success": False,
                "message": "Reddit client not initialized. Please add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables."
            }), 400
            
        reddit_post = fetch_reddit_post()
        if not reddit_post:
            return jsonify({
                "success": False,
                "message": "Could not fetch a Reddit post. Check logs for details."
            }), 500
            
        content = reddit_post
        
    # Try to send the post
    try:
        send_post(context, content)
        return jsonify({
            "success": True,
            "message": f"{post_type.capitalize()} post sent successfully!",
            "post": {
                "type": post_type,
                "image_url": content.get("image_url", ""),
                "source": content.get("source", ""),
                "caption_preview": content.get("caption", "")[:30] + "..." if len(content.get("caption", "")) > 30 else content.get("caption", "")
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error sending post: {str(e)}"
        }), 500

# Keeping the original endpoint for backward compatibility
@app.route('/api/test/reddit-post', methods=['GET'])
def test_reddit_post():
    """Redirect to the new endpoint structure for Reddit posts"""
    return test_post('reddit')

def run_bot():
    """Run the Telegram bot in a separate thread"""
    setup_bot()

# Handle the startup differently based on workflow
def main():
    # Get the current workflow name from environment variable
    current_workflow = os.environ.get('REPL_WORKFLOW', '')
    
    # Check if this is running in the run_miku_bot workflow
    if current_workflow == 'run_miku_bot':
        print("=========================================")
        print("Detected run_miku_bot workflow")
        print("Starting BOT ONLY in standalone mode...")
        print("=========================================")
        
        from bot_runner import run_standalone_bot
        run_standalone_bot()
        return
    
    # If explicitly asked to run bot_only from command line arg
    elif len(sys.argv) > 1 and sys.argv[1] == 'bot_only':
        print("Starting Miku bot in standalone mode via command line argument...")
        
        from bot_runner import run_standalone_bot
        run_standalone_bot()
        return
    
    else:
        # Normal mode: start both the bot thread and Flask app
        print("Starting in COMBINED mode (web interface + bot)...")
        
        # Start the bot in a separate thread
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=5000)

# Only start the bot when running directly, not when imported by gunicorn
if __name__ == '__main__':
    main()
