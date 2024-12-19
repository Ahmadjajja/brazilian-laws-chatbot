from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Vectara API credentials
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")
VECTARA_CORPUS_KEY = os.getenv("VECTARA_CORPUS_KEY")
VECTARA_URL = f"https://api.vectara.io/v2/corpora/{VECTARA_CORPUS_KEY}/query"

# OpenAI API key for GPT
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check that the environment variables are loaded correctly
if not VECTARA_API_KEY or not VECTARA_CORPUS_KEY or not OPENAI_API_KEY:
    raise ValueError("Please set VECTARA_API_KEY, VECTARA_CORPUS_KEY, and OPENAI_API_KEY in your .env file.")

# API Headers for Vectara
VECTARA_HEADERS = {
    "Accept": "application/json",
    "x-api-key": VECTARA_API_KEY
}

# API Headers for OpenAI (ChatGPT)
openai.api_key = OPENAI_API_KEY

@app.route("/query-llm", methods=["POST"])
def query_llm():
    """
    Handle POST request to receive a query and return the same query as response.
    The function will query Vectara and then use ChatGPT to process the result.
    """
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Query parameter is required."}), 400

    user_query = data['query']
    print("Received query in POST request -> ", user_query)

    # Step 1: Get the response from Vectara
    vectara_response = query_vectara_helper(user_query)

    # # Step 2: Combine Vectara's response with a custom prompt for GPT
    # gpt_prompt = f"Given the following context, answer the user's query:\nContext: {vectara_response['data']}\nUser Query: {user_query}"

    # # Step 3: Call ChatGPT (gpt-3.5-turbo) with the combined context and user query
    # gpt_response = query_chatgpt(gpt_prompt)

    # Step 4: Return the result
    return jsonify({
        "query": user_query,
        "vectara_response": vectara_response,
        # "chatgpt_response": gpt_response
    }), 200

def query_vectara_helper(user_query):
    """
    Helper function to call the Vectara API with a query from POST request.
    """
    limit = 10
    offset = 0

    query_params = {
        "query": user_query,
        "limit": limit,
        "offset": offset
    }

    try:
        response = requests.get(VECTARA_URL, headers=VECTARA_HEADERS, params=query_params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to query Vectara", "details": str(e)}

def query_chatgpt(prompt):
    """
    Call ChatGPT (gpt-3.5-turbo) model with the given prompt.
    """
    print("Started...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # This is the free model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return {"error": "Failed to query ChatGPT", "details": str(e)}

@app.route("/", methods=["get"])
def q():
    print("query_chatgpt -> ", query_chatgpt("What is AI?"))
    return "Hi..."

if __name__ == "__main__":
    app.run(debug=True)
