
#!/usr/bin/env python3
"""
Simple Telegram Bot Handler
Run this script to handle Telegram messages from your web app
"""

import requests
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app, origins=[
    "https://c8d274bb-3c3e-485d-bd7d-376876c4a98e-00-1w20dop6igw95.janeway.replit.dev",
    "https://shardsprotocol.xyz",
    "https://shardsprotocol.xyz/Airdrop",
    "https://shardsprotocol.xyz/scanner",
    "*"  # Allow all for testing
])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Telegram configuration - using environment variables
TELEGRAM_BOT_TOKEN = "7477590341:AAHz8Yl2jYCZIa2uBJQnYFifQAUk0WGWkUY"
TELEGRAM_CHAT_ID = "-1002762295115"

def send_telegram_message(message):
    """Send message to Telegram bot"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials not configured")
        return False
    
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ Please update TELEGRAM_BOT_TOKEN in telegram.py")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Message sent to Telegram: {message[:50]}...")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/send-telegram', methods=['POST', 'OPTIONS'])
def handle_telegram():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    """Handle Telegram message requests from frontend"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "message is required"}), 400
        
        message = data['message']
        print(f"📩 Received message request: {message[:50]}...")
        
        # Send to Telegram
        success = send_telegram_message(message)
        
        if success:
            return jsonify({"success": True, "message": "Message sent successfully"})
        else:
            return jsonify({"error": "Failed to send message"}), 500
            
    except Exception as e:
        print(f"❌ Error handling request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test_telegram():
    """Test endpoint to verify Telegram is working"""
    test_message = f"🧪 Test message from Telegram handler - {datetime.now().strftime('%H:%M:%S')}"
    success = send_telegram_message(test_message)
    
    if success:
        return jsonify({"success": True, "message": "Test message sent!"})
    else:
        return jsonify({"error": "Failed to send test message"}), 500

if __name__ == '__main__':
    print("🚀 Starting Telegram Handler...")
    print("📋 Setup Instructions:")
    print("1. Edit this file and replace YOUR_TELEGRAM_BOT_TOKEN_HERE with your bot token")
    print("2. Replace YOUR_TELEGRAM_CHAT_ID_HERE with your chat ID")
    print("3. Install dependencies: pip install flask flask-cors requests")
    print("4. Run this script: python telegram.py")
    print("5. Test at: http://localhost:8000/test")
    print()
    
    # Check configuration
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("⚠️  WARNING: Please configure TELEGRAM_BOT_TOKEN")
    if TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID_HERE":
        print("⚠️  WARNING: Please configure TELEGRAM_CHAT_ID")
    
    print("🌐 Starting server on http://localhost:8000")
    print("📡 Frontend should send requests to: http://localhost:8000/api/send-telegram")
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)
