# import streamlit as st
# import requests
# 
# # Streamlit app title
# st.title("Professional Guidance for Real Estate Registry Offices")
# 
# # Initialize session state for chat history if not exists
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# 
# # Define the API URL
# # api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"
# # Uncomment for local testing
# api_url = "http://127.0.0.1:5000/query-llm"
# 
# # Function to call the REST API and return the response
# def get_response_from_api(prompt, chat_history):
#     try:
#         # Prepare payload with prompt and chat history
#         payload = {
#             "query": prompt,
#             "chat_history": chat_history
#         }
#         # Make a POST request to the API
#         response = requests.post(api_url, json=payload)
#         # Check if the response is successful
#         if response.status_code == 200:
#             return response.json().get("gpt_response", "No response from API.")
#         else:
#             return f"Error: {response.status_code} - {response.text}"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"
# 
# # Prompt input
# prompt = st.text_input("Enter your Text:")
# 
# # Button to generate response
# if st.button("Generate Response"):
#     with st.spinner('Generating response...'):
#         # Fetching response from the REST API
#         response = get_response_from_api(prompt, st.session_state.chat_history)
#         
#         # Update chat history
#         st.session_state.chat_history.append({
#             "user": prompt,
#             "assistant": response
#         })
# 
# # Display chat history
# for chat in reversed(st.session_state.chat_history):
#     st.write(f"**User:** {chat['user']}")
#     st.write(f"**Dante:** {chat['assistant']}")
#     st.markdown("---")

import streamlit as st
import requests
from datetime import datetime

# Initialize session state for chat history and messages for API
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'messages_for_api' not in st.session_state:
    st.session_state.messages_for_api = [{
        "role": "system",
        "content": """You are Dante, an AI expert in Real Estate Registry (RI) in Santa Catarina (SC). 
        When asked about previous conversations, reference them specifically. 
        Always maintain context of the entire conversation."""
    }]

# Streamlit app title
st.title("Professional Guidance for Real Estate Registry Offices")

# Define the API URL
api_url = "http://127.0.0.1:5000/query-llm"

# Function to call the REST API and return the response
def get_response_from_api(prompt, messages_history):
    try:
        # Include both the new prompt and conversation history
        payload = {
            "query": prompt,
            "conversation_history": messages_history
        }
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json().get("gpt_response", "No response from API.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Chat input
prompt = st.chat_input("Type your question here...")

# Handle new messages
if prompt:
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Add user message to API messages
    st.session_state.messages_for_api.append({
        "role": "user",
        "content": prompt
    })
    
    # Get AI response with conversation history
    with st.spinner('Generating response...'):
        response = get_response_from_api(prompt, st.session_state.messages_for_api)
        
        # Add AI response to both chat history and API messages
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.session_state.messages_for_api.append({
            "role": "assistant",
            "content": response
        })

# Display chat history in reverse chronological order
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(f"{message['content']}")
    else:
        st.chat_message("assistant").write(f"{message['content']}")

# Add a clear chat button
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.messages_for_api = [{
        "role": "system",
        "content": """You are Dante, an AI expert in Real Estate Registry (RI) in Santa Catarina (SC). 
        When asked about previous conversations, reference them specifically. 
        Always maintain context of the entire conversation."""
    }]
    st.rerun()