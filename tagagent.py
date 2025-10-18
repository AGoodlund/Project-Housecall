
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def get_tags_from_text(text_input):
    response = client.chat.completions.create(
        model="gpt-4o", # Or another suitable model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts keywords and tags."},
            {"role": "user", "content": f"Extract relevant tags from the following text, separated by commas: {text_input}"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    tags_string = response.choices[0].message.content.strip()
    tags = [tag.strip() for tag in tags_string.split(',')]
    return tags

# Example usage
first_input = "This article discusses the benefits of cloud computing and serverless architectures."
extracted_tags = get_tags_from_text(first_input)
print(f"Extracted Tags: {extracted_tags}")


