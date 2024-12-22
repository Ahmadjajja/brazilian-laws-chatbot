import streamlit as st
import requests

# Streamlit app title
st.title("Professional Guidance for Real Estate Registry Offices")

# Define the API URL
api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"

# Prompt input
prompt = st.text_input("Enter your Text:")

# Function to call the REST API and return the response
def get_response_from_api(prompt):
    try:
        # Define the payload
        payload = {"query": prompt}
        # Make a POST request to the API
        response = requests.post(api_url, json=payload)
        # Check if the response is successful
        if response.status_code == 200:
            return response.json().get("gemini_response", "No response from API.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Button to generate response
if st.button("Generate Response"):
    with st.spinner('Generating response...'):
        # Fetching response from the REST API
        response = get_response_from_api(prompt)
        # Displaying the response in Streamlit
        st.write(response)
