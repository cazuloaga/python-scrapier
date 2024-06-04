import functools
import time
import random
import openai
from openai import OpenAI
from app.config import settings
import json

openai_client = OpenAI(api_key=settings.openai_api_key)
openai_model = 'gpt-3.5-turbo'

def retry_with_exponential_backoff(
        func,
        initial_delay: float = 3,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 2,
        errors: tuple = (openai.RateLimitError, openai.InternalServerError, openai.APIConnectionError)
    
        # TODO - timeout
):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Retry a function with exponential backoff."""
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except errors as e:
                print("retrying...")
                print(e)
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded. {e}"
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

    return wrapper

@retry_with_exponential_backoff
def chat_completions_with_backoff(messages:list, model:str = openai_model, client: OpenAI = openai_client, json_format: bool = False):
    if not json_format:
        completion = client.chat.completions.create(
        model=model,
        messages = messages,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    else:
        completion = client.chat.completions.create(
        model=model,
        messages = messages,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type":"json_object"}
        )


    return completion.choices[0].message

def call_chat_GPT(prompt, json_format=False):
    msg = [{"role":"user","content":prompt}        ]
    return chat_completions_with_backoff(msg, json_format=json_format)