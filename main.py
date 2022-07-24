import os
import re
import openai
import argparse
import re

MAX_INPUT_LENGTH = 32


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")
    if validate_length(user_input):
        generate_branding_snippet(user_input)
        generate_keywords(user_input)

    else:
        raise ValueError(
            f"Input length is too long. Max input length is {MAX_INPUT_LENGTH}. Submitted length is {len(user_input)}")


def validate_length(prompt: str):
    return len(prompt) <= MAX_INPUT_LENGTH

# generate snippet


def generate_branding_snippet(prompt: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate upbeat branding snippet for {prompt}: "

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=enriched_prompt, max_tokens=50
    )
    # print(response)

    # Extract output text
    branding_text = response["choices"][0]["text"]

    # Strip whitespace
    branding_text = branding_text.strip()

    # Add "..." to truncated statements
    last_char = branding_text[-1]
    if last_char not in {".", "!", "?"}:
        branding_text += "..."

    print(f"Snippet: {branding_text}")

    return branding_text

# generate keywords


def generate_keywords(prompt: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related branding keywords for {prompt}: "

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=enriched_prompt, max_tokens=50
    )
    # print(response)

    # Extract output text from response
    keywords_text = response["choices"][0]["text"]

    # Strip whitespace
    keywords_text = keywords_text.strip()
    # put in list
    keywords_array = re.split(",|\n|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    # filter anything thats empty
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")

    return keywords_array


if __name__ == "__main__":
    main()
