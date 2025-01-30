from flask import Flask
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def handle_message(data):
    """Handles incoming messages from Nifty Island"""
    print(f"Received: {data}")
    response = f"Mork says: {data}... but darker and with BBQ sauce."
    emit("response", response)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import tweepy
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Twitter API setup
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
api = tweepy.API(auth)

@socketio.on("message")
def handle_message(data):
    """Handles incoming messages from Nifty Island"""
    print(f"Received: {data}")
    response = f"Mork says: {data}... but darker and with BBQ sauce."
    emit("response", response)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
Xfrom flask import Flask, request, jsonify
import tweepy
import os

app = Flask(__name__)

# Load Twitter API keys from environment variables
auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET"))
api = tweepy.API(auth)

@app.route('/tweet', methods=['POST'])
def tweet():
    """API Endpoint for making Mork Zuckerbarge tweet"""
    api_key = request.headers.get("Authorization")

    if api_key != os.getenv("MORK_API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        message = data.get('message', 'Default tweet if no message provided')

        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        tweet = api.update_status(message)
        return jsonify({"status": "success", "tweet_id": tweet.id_str})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/respond', methods=['POST'])
def respond():
    """API for AI-generated responses"""
    data = request.get_json()
    user_message = data.get('message', '')

    # TODO: Integrate OpenAI GPT for better responses
    ai_response = f"Mork says: {user_message}... but darker and with BBQ sauce."

    return jsonify({"response": ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
