from flask import Flask, request, jsonify
import asyncio
from typing import Callable, Optional
from config import Config
from github_api import github_api
import hmac
import hashlib

app = Flask(__name__)

# Store the callback function to send notifications
notification_callback: Optional[Callable] = None

def set_notification_callback(callback: Callable):
    """Set the callback function for sending notifications"""
    global notification_callback
    notification_callback = callback

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify GitHub webhook signature"""
    if not Config.WEBHOOK_SECRET:
        return True  # Skip verification if no secret is set
    
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        Config.WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    try:
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature or not verify_signature(request.data, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Check event type
        event_type = request.headers.get('X-GitHub-Event')
        if event_type != 'push':
            return jsonify({'message': 'Event ignored'}), 200
        
        # Parse payload
        payload = request.json
        commit_data = github_api.parse_webhook_payload(payload)
        
        if not commit_data:
            return jsonify({'error': 'No commits in payload'}), 400
        
        # Send notification asynchronously
        if notification_callback:
            asyncio.run_coroutine_threadsafe(
                notification_callback(commit_data),
                asyncio.get_event_loop()
            )
        
        return jsonify({'message': 'Webhook received successfully'}), 200
    
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'GitHub Webhook Server is running',
        'endpoints': {
            '/webhook': 'POST - GitHub webhook receiver',
            '/health': 'GET - Health check'
        }
    }), 200

def run_server():
    """Run the Flask server"""
    app.run(host='0.0.0.0', port=Config.PORT, debug=False)