import json
from datetime import datetime
from groq import Groq

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

def groq_generate(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content if response.choices else "No response generated."

def main():
    prompt = input("Enter your prompt: ")

    response_text = groq_generate(prompt)

    print("Response:")
    print(response_text)

    record = {
        "prompt": prompt,
        "response": response_text,
        "temperature": 0.7,
        "timestamp": str(datetime.now())
    }

    with open("prompt.json", "w") as file:
        json.dump(record, file, indent=4)

if __name__ == "__main__":
    main()
