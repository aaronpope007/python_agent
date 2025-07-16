import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) == 1:
        print("You must provide a prompt in the form of a string")
        sys.exit(1)
    else:
        ai_response = client.models.generate_content(model='gemini-2.0-flash-001', contents=sys.argv[1])
        print(ai_response.text)
        print(f"Prompt tokens: {ai_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {ai_response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
