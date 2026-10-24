import os, json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("No api key provided")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
    ]

    generate_content(client, messages, args.verbose)


def generate_content(client: OpenAI, messages: list[dict[str, str]], verbose=False) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Failed to get response")

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            if not result_message["content"]:
                raise Exception("No result from func call")
            if verbose:
                print(f"-> {result_message['content']}")
            else:
                print(result_message["content"])

    if verbose:
        print(f"User prompt: {messages[0]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
