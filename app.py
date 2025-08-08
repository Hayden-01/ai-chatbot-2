from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

COMPANY_NAME = "Your Company Name"
WELCOME_MESSAGE = f"Welcome to {COMPANY_NAME} AI Customer Service!"

def chatbot_response(message):
    # Simple example response, customize as needed
    message = message.lower()
    if "hello" in message:
        return f"Hello! How can {COMPANY_NAME} assist you today?"
    elif "help" in message:
        return "Sure, please provide more details about your issue."
    else:
        return "Sorry, I didn't understand that. Could you please rephrase?"

@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>{{company_name}} Chatbot</title></head>
    <body>
        <h1>{{welcome_message}}</h1>
        <div id="chat"></div>
        <input id="input" placeholder="Type your message here" autofocus />
        <button onclick="sendMessage()">Send</button>
        <script>
        async function sendMessage() {
            let input = document.getElementById("input");
            let msg = input.value;
            if(!msg.trim()) return;
            input.value = "";
            let chat = document.getElementById("chat");
            chat.innerHTML += "<p><b>You:</b> " + msg + "</p>";
            let response = await fetch("/get", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: msg})
            });
            let data = await response.json();
            chat.innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";
            chat.scrollTop = chat.scrollHeight;
        }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, company_name=COMPANY_NAME, welcome_message=WELCOME_MESSAGE)

@app.route("/get", methods=["POST"])
def get_bot_response():
    data = request.get_json(force=True)
    user_message = data.get("message", "")
    bot_reply = chatbot_response(user_message)
    return jsonify({"reply": bot_reply})

def get_port():
    port_str = os.environ.get("PORT")
    if port_str is None or port_str.strip() == "":
        return 5000  # default
    try:
        port = int(port_str)
        if 1 <= port <= 65535:
            return port
        else:
            return 5000
    except Exception:
        return 5000

if __name__ == "__main__":
    port = get_port()
    app.run(host="0.0.0.0", port=port, debug=True)  
