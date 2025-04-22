import logging
import os
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
    
@app.route('/api/test/reddit-post', methods=['GET'])
def test_reddit_post():
    """API endpoint to manually test posting from Reddit"""
    from api_clients import fetch_reddit_post, reddit_client
    from handlers import send_post
    from bot import get_bot
    
    if not reddit_client:
        return jsonify({
            "success": False,
            "message": "Reddit client not initialized. Please add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables."
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
    
    # Fetch a Reddit post
    reddit_post = fetch_reddit_post()
    if not reddit_post:
        return jsonify({
            "success": False,
            "message": "Could not fetch a Reddit post. Check logs for details."
        }), 500
        
    # Try to send the post
    try:
        send_post(context, reddit_post)
        return jsonify({
            "success": True,
            "message": "Reddit post fetched and sent successfully!",
            "post": {
                "image_url": reddit_post.get("image_url", ""),
                "source": reddit_post.get("source", ""),
                "caption_length": len(reddit_post.get("caption", ""))
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error sending post: {str(e)}"
        }), 500

def run_bot():
    """Run the Telegram bot in a separate thread"""
    setup_bot()

# Only start the bot when running directly, not when imported by gunicorn
if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
