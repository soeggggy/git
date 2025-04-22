"""
Simple web dashboard that doesn't interfere with the main bot.
This can be run as a separate workflow.
"""
import os
import time
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)
start_time = time.time()

# Home page
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Miku Bot Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #e91e63;
            }
            .status {
                margin: 20px 0;
                padding: 15px;
                background-color: #e8f5e9;
                border-left: 5px solid #4caf50;
                border-radius: 4px;
            }
            .info {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin: 20px 0;
            }
            .card {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .label {
                font-weight: bold;
                color: #555;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Nakano Miku Bot Dashboard</h1>
            
            <div class="status">
                <span id="bot-status">Bot status: Checking...</span>
            </div>
            
            <div class="info">
                <div class="card">
                    <div class="label">Uptime:</div>
                    <div id="uptime">Calculating...</div>
                </div>
                <div class="card">
                    <div class="label">Channel:</div>
                    <div id="channel">Loading...</div>
                </div>
                <div class="card">
                    <div class="label">Fact interval:</div>
                    <div id="fact-interval">Loading...</div>
                </div>
                <div class="card">
                    <div class="label">Image interval:</div>
                    <div id="image-interval">Loading...</div>
                </div>
                <div class="card">
                    <div class="label">Reddit interval:</div>
                    <div id="reddit-interval">Loading...</div>
                </div>
                <div class="card">
                    <div class="label">Reddit enabled:</div>
                    <div id="reddit-enabled">Loading...</div>
                </div>
            </div>

            <h2>Test Post Functions</h2>
            <button onclick="testPost('fact')">Test Fact Post</button>
            <button onclick="testPost('image')">Test Image Post</button>
            <button onclick="testPost('reddit')">Test Reddit Post</button>
            <div id="result" style="margin-top: 15px;"></div>
        </div>

        <script>
            // Function to update dashboard stats
            function updateStats() {
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('bot-status').textContent = 'Bot status: ' + data.status;
                        document.getElementById('uptime').textContent = data.uptime_human;
                        document.getElementById('channel').textContent = data.channel || 'Not set';
                        document.getElementById('fact-interval').textContent = data.intervals.main_fact_interval_minutes + ' minutes';
                        document.getElementById('image-interval').textContent = data.intervals.image_interval_minutes + ' minutes';
                        document.getElementById('reddit-interval').textContent = data.intervals.reddit_interval_minutes + ' minutes';
                        document.getElementById('reddit-enabled').textContent = data.reddit_enabled ? 'Yes' : 'No';
                    })
                    .catch(error => {
                        console.error('Error fetching status:', error);
                        document.getElementById('bot-status').textContent = 'Bot status: Error connecting';
                    });
            }
            
            // Function to test posting
            function testPost(type) {
                document.getElementById('result').textContent = 'Sending ' + type + ' post...';
                
                fetch('/api/test/post/' + type)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('result').textContent = data.message;
                        } else {
                            document.getElementById('result').textContent = 'Error: ' + data.message;
                        }
                    })
                    .catch(error => {
                        console.error('Error testing post:', error);
                        document.getElementById('result').textContent = 'Error: Could not connect to server';
                    });
            }
            
            // Update stats every 10 seconds
            updateStats();
            setInterval(updateStats, 10000);
        </script>
    </body>
    </html>
    """

# Status API endpoint
@app.route('/status')
def status():
    import config
    
    # Get default channel
    channel = os.environ.get('TELEGRAM_CHANNEL_USERNAME') or config.DEFAULT_CHANNEL
    if channel and not channel.startswith('@'):
        channel = '@' + channel
    
    # Calculate uptime
    uptime = int(time.time() - start_time)
    
    return jsonify({
        "status": "running",
        "bot_name": "Nakano Miku Bot",
        "version": "1.0.0",
        "channel": channel,
        "uptime_seconds": uptime,
        "uptime_human": f"{uptime // 86400}d {(uptime % 86400) // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s",
        "intervals": {
            "main_fact_interval_minutes": config.MAIN_POST_INTERVAL // 60,
            "image_interval_minutes": config.IMAGE_POST_INTERVAL // 60,
            "reddit_interval_minutes": config.REDDIT_POST_INTERVAL // 60
        },
        "reddit_enabled": bool(os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET")),
        "keepalive": True
    })

# Test post endpoints
@app.route('/api/test/post/<post_type>')
def test_post(post_type):
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

if __name__ == '__main__':
    # Run on a different port to avoid conflicts
    app.run(host='0.0.0.0', port=8080)