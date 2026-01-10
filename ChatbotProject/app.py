import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_fallback_secret_key")

# Supabase Setup
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- ROUTES ---

@app.route('/')
def home():
    """Student Chatbot Interface"""
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    """Admin Dashboard Interface"""
    return render_template('admin.html')

# --- ADMIN ACTIONS (Data Collection) ---

@app.route('/admin/add_student', methods=['POST'])
def add_student():
    roll_no = request.form.get('roll_no')
    full_name = request.form.get('full_name')
    dept = request.form.get('dept')

    try:
        # We generate a random UUID for the profile since we aren't using Auth Signup for this test
        import uuid
        new_id = str(uuid.uuid4())
        
        data = {
            "id": new_id,
            "student_roll_no": roll_no,
            "full_name": full_name,
            "department": dept
        }
        supabase.table("profiles").insert(data).execute()
        return "Student Registered Successfully! <a href='/admin'>Go Back</a>"
    except Exception as e:
        return f"Error: {str(e)} <a href='/admin'>Go Back</a>"

@app.route('/admin/add_grade', methods=['POST'])
def add_grade():
    roll_no = request.form.get('roll_no')
    subject = request.form.get('subject')
    grade = request.form.get('grade')

    try:
        # 1. Find the student UUID using the Roll Number
        student_query = supabase.table("profiles").select("id").eq("student_roll_no", roll_no).execute()
        
        if not student_query.data:
            return "Error: Roll Number not found. <a href='/admin'>Go Back</a>"
        
        student_uuid = student_query.data[0]['id']

        # 2. Insert Grade
        grade_data = {
            "student_id": student_uuid,
            "subject_name": subject,
            "grade_received": grade,
            "semester": 1 # Defaulting to 1 for this test
        }
        supabase.table("student_grades").insert(grade_data).execute()
        return "Grade Assigned Successfully! <a href='/admin'>Go Back</a>"
    except Exception as e:
        return f"Error: {str(e)} <a href='/admin'>Go Back</a>"

# --- CHATBOT LOGIC ---

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message", "").lower()
    bot_response = "I'm sorry, I don't have information on that. I have logged your question for the admin."

    try:
        # 1. Search Knowledge Base
        kb_query = supabase.table("bot_knowledge").select("bot_response").ilike("question_pattern", f"%{user_input}%").execute()
        
        if kb_query.data:
            bot_response = kb_query.data[0]['bot_response']

        # 2. AUTOMATIC DATA COLLECTION (Requirement Check)
        # We log EVERY chat to the chat_logs table
        log_data = {
            "user_query": user_input,
            "bot_response": bot_response
        }
        supabase.table("chat_logs").insert(log_data).execute()

    except Exception as e:
        print(f"Database error: {e}")

    return jsonify({"response": bot_response})

# --- STUDENT LOGIN TEST ---
@app.route('/login_test/<roll_no>')
def login_test(roll_no):
    """Simple route to simulate a student logging in"""
    session['roll_no'] = roll_no
    return f"Logged in as {roll_no}. <a href='/'>Go to Chat</a>"

if __name__ == '__main__':
    app.run(debug=True)