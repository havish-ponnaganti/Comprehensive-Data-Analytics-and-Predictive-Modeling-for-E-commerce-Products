import pandas as pd
import openai
import os

# Load API key from environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the CSV file
data = pd.read_csv('data/data.csv')

def chat_with_csv(question):
    data_string = data.to_string()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that can analyze and answer questions based on CSV data provided."},
                {"role": "user", "content": f"I have the following data in a CSV file:\n{data_string}\n\nCan you answer this question:\n{question}"}
            ],
            max_tokens=500,
            temperature=0.5
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer

    except Exception as e:
        print("\nError occurred:")
        print(e)
        return "An error occurred while processing your request."

while True:
    user_question = input("\nAsk a question about your CSV data (or type 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break
    response = chat_with_csv(user_question)
    print("\nResponse from the model:")
    print(response)
