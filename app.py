from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# Basic chatbot logic
def chatbot_response(message, company_name):
    responses = [
        f"Hello! Thanks for contacting {company_name}. How can I help you today?",
        f"{company_name} is here to assist you. Could you provide more details?",
        f"Sure, I can help with that. Could you explain a bit more?",
        f"Let me connect you to the right department at {company_name}.",
        f"I understand. Let's get this sorted for you."
    ]
    return random.choice(responses)

@app.route("/", methods=["GET", "POST"])
def home():
    company_name = "Your Company"
    if request.method == "POST":
        user_message = request.form.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        bot_reply = chatbot_response(user_message, company_name)
        return jsonify({"reply": bot_reply})
    import os


    port = 5000
    # Simple HTML chat interface
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Customer Service Chatbot</title>
    </head>
    <body>
        <h1>Welcome to AI Customer Service Chatbot</h1>
        <form method="POST">
            <input name="message" placeholder="Type your message..." required>
            <button type="submit">Send</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == "__main__":
   
    import os

def get_port():
    port_str = os.environ.get("PORT", "")
    try:
        port = int(port_str)
        if port <= 0 or port > 65535:
            raise ValueError("Port out of range")
        return port
    except (ValueError, TypeError):
        return 5000  # default port

port = get_port()

app.run(host="0.0.0.0", port=port, debug=True)
