import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "college_bot_secure_key")

# Connect to your Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_chat_response(user_input):
    user_input = user_input.strip().lower()

    # 1. Search for Personalized Info (Grades)
    if "grade" in user_input or "marks" in user_input:
        user_id = session.get('user_id')
        if user_id:
            res = supabase.table("student_grades").select("*").eq("student_id", user_id).execute()
            if res.data:
                results = [f"{g['subject_name']}: {g['grade_received']}" for g in res.data]
                return "Your grades are: " + ", ".join(results)
            return "I couldn't find any grades for your account."
        return "Please log in to see your grades."

    # 2. Search General Knowledge (Fixes the AIML 'Default Response' error)
    # This looks at your 'bot_knowledge' table in Supabase
    kb_res = supabase.table("bot_knowledge").select("bot_response").ilike("question_pattern", f"%{user_input}%").execute()
    
    if kb_res.data:
        return kb_res.data[0]['bot_response']

    # 3. Log Unanswered Questions
    supabase.table("chat_logs").insert({"user_query": user_input, "bot_response": "Unknown"}).execute()
    return "I'm not sure about that. I've logged your question for the admin!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get("message")
    response_text = get_chat_response(user_message)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)