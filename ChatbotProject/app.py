import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. Setup and Configurations
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_fallback_secret_key")

# Connect to your Supabase project (utpveptazuxcrmfgwzsf)
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- CHATBOT LOGIC FUNCTION ---
def get_response_from_cloud(user_input):
    query = user_input.strip().lower()
    
    # Check if the user is asking about personal data (Grades)
    if "grade" in query or "marks" in query or "result" in query:
        if 'user_id' in session:
            # Query the student_grades table you created
            res = supabase.table("student_grades").select("*").eq("student_id", session['user_id']).execute()
            if res.data:
                grades_list = [f"{item['subject_name']}: {item['grade_received']}" for item in res.data]
                return "Your grades are: " + ", ".join(grades_list)
            return "I couldn't find any grade records for your ID."
        return "Please log in first to view your personal grades."

    # General Knowledge Search: Query your 'bot_knowledge' table
    # This uses 'ilike' to find if the pattern exists within the query
    kb_res = supabase.table("bot_knowledge").select("bot_response").ilike("question_pattern", f"%{query}%").execute()
    
    if kb_res.data:
        return kb_res.data[0]['bot_response']

    # Log unanswered questions to 'chat_logs' (as seen in your screenshot)
    supabase.table("chat_logs").insert({
        "user_query": user_input, 
        "bot_response": "I don't know that yet."
    }).execute()
    
    return "I'm not sure about that. I've logged your question for the college admin!"

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"status": "error", "response": "No message received"})
    
    bot_answer = get_response_from_cloud(user_message)
    return jsonify({"status": "success", "response": bot_answer})

# Simple Login Route for Testing
@app.route('/login', methods=['POST'])
def login():
    # In a full app, you'd use supabase.auth.sign_in_with_password
    # For now, we manually set a student_id to test your 'student_grades' table
    session['user_id'] = request.form.get("student_id") 
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)