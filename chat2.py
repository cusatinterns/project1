import pandas as pd
import openai
from flask import Flask, request, jsonify

# Load real estate data from CSV
data = pd.read_csv('Book1.csv', encoding='latin-1')

# OpenAI API credentials
openai.api_key = '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'
model_name = 'gpt-3.5-turbo'

# Flask app initialization
app = Flask(__name__)

# Define a route to handle incoming messages
@app.route('/chat', methods=['POST'])
def chat():
    # Get customer message from the request
    customer_message = request.json['message']
    print(f"Customer message: {customer_message}")
    # Generate auto response using OpenAI's ChatGPT
    response = generate_auto_response(customer_message)
    print(f"Generated response: {response}")
    return jsonify({'response': response})

def generate_auto_response(question):
    # Find relevant real estate information based on the customer's question
    relevant_info = find_relevant_info(question)

    # Generate an auto response using OpenAI's ChatGPT
    prompt = f'User: {question}\nAssistant: {relevant_info}\nUser:'
    max_tokens = 50  # Set the desired length of the response

    response = openai.Completion.create(
        engine=model_name,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()

def find_relevant_info(question):
    # Implement your logic to find relevant real estate information based on the customer's question
    # You can use the 'data' DataFrame loaded from the CSV file to search for relevant information
    # This can involve querying the DataFrame, filtering, or any other relevant operations

    # Example logic: Find properties with specific features based on the question
    relevant_properties = data[data['features'].str.contains('swimming pool', case=False)]

    # Get the description of the first relevant property
    if len(relevant_properties) > 0:
        description = relevant_properties.iloc[0]['description']
    else:
        description = "I'm sorry, but I couldn't find any relevant properties."

    return description


if __name__ == '__main__':
    app.run()
