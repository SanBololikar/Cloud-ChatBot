# Cloud-Integrated Intelligent College Chatbot System

## 🚀 Project Overview
This project is a full-stack, cloud-native conversational agent designed for educational institutions. It provides a dual-interface system allowing **Students** to access personalized academic data through a chatbot and **Administrators** to manage the underlying data infrastructure via a secure dashboard.

## 🏗️ System Architecture
The application follows a modern cloud-first architecture, moving away from local file storage to a centralized, relational cloud database.



### 1. Cloud Backend (Supabase/PostgreSQL)
The database is structured to ensure data integrity and scalability:
* **`profiles`**: Manages unique student identities and departmental data.
* **`student_grades`**: Maintains a relational link to student profiles to store academic performance.
* **`bot_knowledge`**: A dynamic repository of FAQ patterns and responses for the chatbot.
* **`chat_logs`**: An automated audit trail that records every user interaction for data analysis.

### 2. Logic Layer (Python/Flask)
The server acts as a secure bridge between the frontend and the cloud database, handling:
* **Session Management**: Tracking student identities during active chats.
* **Query Logic**: Processing natural language queries to fetch data from the Knowledge Base or Grade tables.
* **Data Routing**: Handling administrative form submissions to update cloud records in real-time.

## ✨ Core Features
* **Student Personalization**: Students can login using their Roll Number to receive personalized greetings and retrieve their specific grades.
* **Admin Management Suite**: A dedicated interface for authorized personnel to register new students and update academic results without direct database access.
* **Automated Knowledge Base**: The bot uses pattern matching to answer general inquiries about college fees, admissions, and facilities.
* **Data Collection Engine**: Every message sent is automatically logged, allowing for a complete review of user needs and bot performance.

## 🛠️ Deployment & Technologies
- **Frontend**: HTML5, CSS3 (Bootstrap), and JavaScript.
- **Backend**: Flask (Python).
- **Database**: PostgreSQL hosted on Supabase.
- **Hosting**: Render (Cloud Web Services).

## 🚀 Getting Started
1. **Access the Portal**: Navigate to the live URL.
2. **Admin Setup**: Use the Admin Panel to populate student profiles and grades.
3. **Student Interaction**: Login as a student to interact with the bot and view academic data.