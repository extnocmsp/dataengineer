import streamlit as st
import openai
import json
import time
import datetime
import requests
from openai import RateLimitError

# ✅ OpenAI API
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ Load employee data
with open('splanprojectcontent.json') as f:
    employee_data = json.load(f)

# ✅ Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.datetime.now()

# ✅ Check for session expiration
if (datetime.datetime.now() - st.session_state.session_start).seconds > 600:
    st.warning("Session expired after 10 minutes of inactivity.")
    st.session_state.clear()
    st.experimental_rerun()

# ✅ IP address capture
if "ip_address" not in st.session_state:
    try:
        st.session_state.ip_address = requests.get("https://api.ipify.org").text
    except:
        st.session_state.ip_address = "Unknown"

# ✅ Greeting message
st.title("Splan Chatbot Project 🤖")
st.markdown("👋 Welcome! How can I assist you today?")

# ✅ GPT function
def query_gpt3(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        time.sleep(5)
        return "⚠️ Too many requests. Please wait and try again."

# ✅ User Input
user_input = st.text_input("Ask a question about the employees:")

if st.button("Submit"):
    if user_input:
        prompt = f"Given the following employee data: {json.dumps(employee_data, indent=2)}\n\nAnswer this question:\n{user_input}"
        st.info("Generating your answer, please wait...")
        time.sleep(2)

        answer = query_gpt3(prompt)

        st.write("Answer:")
        st.write(answer)

        # ✅ Save to chat history
        st.session_state.chat_history.append({"user": user_input, "bot": answer})

    else:
        st.warning("Please enter a question.")

# ✅ Ask for user consent to save chat after 3 turns
if len(st.session_state.chat_history) >= 3 and "consent" not in st.session_state:
    consent = st.radio("Can we save this conversation to improve our services?", ("Yes", "No"))
    if consent:
        st.session_state.consent = consent

# ✅ After 5 Q&As, ask to email chat
if len(st.session_state.chat_history) >= 5 and "email_sent" not in st.session_state:
    if st.checkbox("📤 Would you like to receive this chat by email?"):
        email = st.text_input("Enter your email to receive chat log:")
        if st.button("Send Email"):
            # Simulated email logic (Replace with SendGrid or SMTP)
            st.success("📬 Chat log will be sent to your email (simulation).")
            st.session_state.email_sent = True

# ✅ Ask for details only when user confirms satisfaction
if len(st.session_state.chat_history) >= 5 and st.button("✅ Yes, I'm satisfied"):
    with st.form("user_details"):
        first = st.text_input("First Name")
        last = st.text_input("Last Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        submit = st.form_submit_button("Submit")
        if submit:
            # Simulated user data saving
            st.success("🎉 Thanks! Your feedback has been recorded.")
