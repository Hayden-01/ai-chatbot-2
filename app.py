from flask import Flask, request, jsonify, render_template_string
import os
import openai

app = Flask(__name__)

# Set your OpenRouter API key here or via environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_API_KEY_HERE")
openai.api_key = OPENROUTER_API_KEY

COMPANY_NAME = "Synthara"
WELCOME_MESSAGE = f"Welcome to {COMPANY_NAME} AI Customer Service!"

def chatbot_response(message):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant for {COMPANY_NAME}."},
        {"role": "user", "content": message},
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I am having trouble right now. ({str(e)})"

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
            if (!msg.trim()) return;
            input.value = "";
            let chat = document.getElementById("chat");
            chat.innerHTML += "<p><b>You:</b> " + msg + "</p>";
            const res = await fetch("/get", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: msg})
            });
            const data = await res.json();
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
    reply = chatbot_response(user_message)
    return jsonify({"reply": reply})

def get_port():
    port_str = os.environ.get("PORT")
    if port_str is None or port_str.strip() == "":
        return 5000
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
