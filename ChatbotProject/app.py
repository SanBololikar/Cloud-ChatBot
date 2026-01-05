import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, find_dotenv
from supabase import create_client
import aiml

load_dotenv(find_dotenv())

# Setup Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# Setup AIML
kern = aiml.Kernel()
kern.learn("knowledge.aiml")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_msg = request.form['message']
    bot_reply = kern.respond(user_msg) or "I'm sorry, I don't understand that yet."

    # Save to Supabase Cloud
    data = {"user_query": user_msg, "bot_response": bot_reply}
    try:
        supabase.table("chat_logs").insert(data).execute()
    except Exception as e:
        print(f"Cloud Save Error: {e}")

    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    print("Website running at http://127.0.0.1:5000")
    app.run(debug=True)