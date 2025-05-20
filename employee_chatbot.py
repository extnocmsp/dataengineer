import streamlit as st
import openai
import json
import time
from openai import RateLimitError

# ✅ Secure OpenAI client setup
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ Load employee data
with open('employee_info.json') as f:
    employee_data = json.load(f)

# ✅ GPT function with RateLimitError handling
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
        time.sleep(3)  # ✅ Delay before retrying or returning
        return "⚠️ We're currently sending too many requests. Please wait a moment and try again."

# ✅ Streamlit UI
st.title("Employee Information Chatbot")

user_input = st.text_input("Ask a question about the employees:")

if st.button("Submit"):
    if user_input:
        prompt = f"Given the following employee data: {json.dumps(employee_data, indent=2)}\n\nAnswer the following question:\n{user_input}"
        st.info("Generating your answer, please wait...")
        time.sleep(1.5)
        answer = query_gpt3(prompt)
        st.write("Answer:")
        st.write(answer)
    else:
        st.warning("Please enter a question.")
