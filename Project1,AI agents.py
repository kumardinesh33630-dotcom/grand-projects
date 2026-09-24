"""
Intelligence: The "brain" that processes information and makes decisions using LLMs.
This component handles context understanding, instruction following, and response generation.

More info: https://platform.openai.com/docs/guides/text?api-mode=responses
"""

import os

from openai import OpenAI


def basic_intelligence(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Set it in your environment before running this script."
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(model="gpt-4o", input=prompt)
    return response.output_text


if __name__ == "__main__":
    try:
        result = basic_intelligence(prompt="What is artificial intelligence?")
        print("Basic Intelligence Output:")
        print(result)
    except RuntimeError as exc:
        print(exc)
