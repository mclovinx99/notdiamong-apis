from flask import Flask, request, jsonify
from notdiamond import NotDiamond
import os
 
# Load environment variables from .env fil
 
# Retrieve the API key from the environment
NOTDIAMOND_API_KEY = os.getenv("NOTDIAMOND_API_KEY")  # os.getenv("NOTDIAMOND_API_KEY")
if NOTDIAMOND_API_KEY is None:
    raise ValueError("No API key found. Make sure it's set in the .env file.")
 
# Initialize the NotDiamond client with your API key
client = NotDiamond(api_key=NOTDIAMOND_API_KEY)
 
app = Flask(__name__)
 
@app.route('/chat', methods=['POST'])
def chat():
    # Extract the user input from the POST request
    data = request.get_json()
    user_input = data.get('user_input')
 
    if not user_input:
        return jsonify({'error': 'Missing user_input in request body'}), 400
 
    # Send the user input to the NotDiamond API
    result, session_id, provider = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        model=['openai/gpt-4o']  # Replace with the correct NotDiamond model
    )
 
    # Return the result as a JSON response
    return jsonify({
        'session_id': session_id,
        'llm_called': provider.model,
        'llm_output': result.content
    })
 
if __name__ == '__main__':
    app.run(debug=True)