import streamlit as st
import openai
import json

# Load your OpenAI API key
openai.api_key = "sk-proj-wyp6TCVsueBXqH1GgYNIT3BlbkFJVEsuZOPZ2PlDXr5anEIm"

# Load the JSON data
with open('employee_info.json') as f:
    employee_data = json.load(f)

# Function to query OpenAI GPT-3.5-turbo
def query_gpt3(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Streamlit UI
st.title("Employee Information Chatbot")

user_input = st.text_input("Ask a question about the employees:")

if st.button("Submit"):
    if user_input:
        # Create a prompt with the user question and the employee data
        prompt = f"Given the following employee data: {json.dumps(employee_data, indent=2)}\n\nAnswer the following question:\n{user_input}"
        
        # Query GPT-3.5-turbo
        answer = query_gpt3(prompt)
        
        # Display the answer
        st.write("Answer:")
        st.write(answer)
    else:
        st.write("Please enter a question.")
