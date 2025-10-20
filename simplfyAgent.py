import openai
import os
import json

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_specialty(specialty):
    """
    Takes a doctor's specialty, converts it to a tag, and simplifies it to an everyday term.
    """
    try:
        completion = openai.chat.completions.create(
            model="gpt-4o", # Using a recent, powerful model
            messages=[
                {"role": "system", "content": "You are an assistant that creates technical tags and simplifies medical terminology for a general audience."},
                {"role": "user", "content": f"""
                You will be provided with a medical specialty. Your task is to:
                1.  Generate a simple, lowercase, hyphenated tag from the specialty.
                2.  Explain the specialty using simple, everyday language.

                Return the output in a JSON object with two keys: "tag" and "everyday_term".

                Medical specialty: {specialty}
                """}
            ],
            response_format={ "type": "json_object" } # Ensure the response is in JSON format
        )

        response_content = completion.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Example Usage ---
specialty_input = "Cardiothoracic Surgery"
results = process_specialty(specialty_input)

if results:
    print(f"Original Specialty: {specialty_input}")
    print(f"Generated Tag: {results['tag']}")
    print(f"Simplified Term: {results['everyday_term']}")
