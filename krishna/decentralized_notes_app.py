from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

# === Settings ===
PINATA_API_KEY = 'a2653f0c1f9793b4f302'
PINATA_SECRET_API_KEY = 'e83c8ca6622ce639cdf2ebbf34c1d5a3063cfea519109271165c270685604755'

# === Routes ===

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <title>Simple Decentralized Notes App</title>
        <style>
            body { font-family: Arial, sans-serif; background: #fafafa; text-align: center; padding: 20px; }
            .container { width: 90%; max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; }
            textarea, input { width: 90%; padding: 10px; margin: 10px 0; }
            button { padding: 10px 20px; background-color: #2ecc71; color: white; border: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>📝 Simple Notes + Assistant</h1>

            <textarea id='noteInput' placeholder='Write your note here...'></textarea><br>
            <button onclick='submitNote()'>Submit Note</button>

            <div id='planResult'></div>
            <div id='ipfsResult'></div>

            <hr>

            <input id='chatInput' placeholder='Ask the assistant...'>
            <button onclick='sendMessage()'>Send</button>
            <div id='chatReply'></div>
        </div>

        <script>
            function submitNote() {
                const note = document.getElementById('noteInput').value;
                const formData = new FormData();
                formData.append('note', note);

                fetch('/submit_note', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('planResult').innerText = "Plan: " + data.plan;
                    document.getElementById('ipfsResult').innerHTML = 'IPFS Link: <a href="' + data.ipfs + '" target="_blank">' + data.ipfs + '</a>';
                });
            }

            function sendMessage() {
                const message = document.getElementById('chatInput').value;
                const formData = new FormData();
                formData.append('message', message);

                fetch('/chatbot', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('chatReply').innerText = "Assistant: " + data.reply;
                });
            }
        </script>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

@app.route('/submit_note', methods=['POST'])
def submit_note():
    note = request.form['note']
    plan = generate_plan(note)
    ipfs_link = upload_to_ipfs(note)
    return jsonify({"plan": plan, "ipfs": ipfs_link})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.form['message']
    return jsonify({"reply": chatbot_response(message)})

# === Functions ===

def generate_plan(note):
    if "study" in note.lower():
        return "Your Study Plan: 2 hours of focused learning daily."
    elif "health" in note.lower():
        return "Your Health Plan: Morning walks and balanced diet."
    else:
        return "Break your tasks into daily actions for best results."

def chatbot_response(message):
    if "hello" in message.lower():
        return "Hello! What do you want to plan today?"
    else:
        return "I'm here to assist you! Share your goal."

def upload_to_ipfs(content):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    payload = {
        "pinataContent": {"note": content}
    }
    try:
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()
        hash = r.json()["IpfsHash"]
        return f"https://gateway.pinata.cloud/ipfs/{hash}"
    except:
        return "IPFS upload failed."

# === Main Runner ===

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
