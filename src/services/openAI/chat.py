import openai
from deep_translator import GoogleTranslator
import json

api_key = "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"

openai.api_key = api_key

def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']

def load_conversation():
    try:
        with open("conversation_history.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_conversation(conversation):
    with open("conversation_history.json", "w") as f:
        json.dump(conversation, f, indent=4)

def main():
    conversation_history = load_conversation()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        translated_input = GoogleTranslator(source='hy', target='en').translate(user_input)

        messages = []
        messages.extend(conversation_history)
        messages.append({'role': 'user', 'content': translated_input})

        conversation = {
            "role": "user",
            "content": translated_input
        }
        conversation_history.append(conversation)
        save_conversation(conversation_history)
        print()

        response = generate_response(messages)
        translated_response = GoogleTranslator(source='en', target='hy').translate(response)

        conversation = {
            "role": "assistant",
            "content": response
        }
        conversation_history.append(conversation)
        save_conversation(conversation_history)

        print("ChatGPT:", translated_response)

if __name__ == "__main__":
    main()