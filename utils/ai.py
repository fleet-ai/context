# pylint: disable=W0707
# pylint: disable=W0719

import json
import tiktoken
import openai
import requests

from constants.ai import SYSTEM_PROMPT, PROMPT, API_URL


def retrieve_context(query, openai_api_key, k=10, filters=None):
    """Gets the context from our libraries vector db for a given query.

    Args:
        query (str): User input query
        k (int, optional): number of retrieved results. Defaults to 10.
    """

    # First, we query the API
    url = f"{API_URL}/query"
    headers = {"Authorization": f"Bearer {openai_api_key}"}
    params = {
        "query": query,
        "dataset": "python_libraries",
        "n_results": k,
        "filters": filters,
    }
    responses = requests.post(url, json=params, headers=headers, timeout=120).json()

    # Then, we build the prompt_with_context string
    prompt_with_context = ""
    for response in responses:
        prompt_with_context += f"\n\n### Context {response['metadata']['url']} ###\n{response['metadata']['text']}"
    return {"role": "user", "content": prompt_with_context}


def construct_prompt(
    messages,
    context_message,
    model="gpt-4-1106-preview",
    cite_sources=True,
    context_window=3000,
):
    """
    Constructs a RAG (Retrieval-Augmented Generation) prompt by balancing the token count of messages and context_message.
    If the total token count exceeds the maximum limit, it adjusts the token count of each to maintain a 1:1 proportion.
    It then combines both lists and returns the result.

    Parameters:
    messages (List[dict]): List of messages to be included in the prompt.
    context_message (dict): Context message to be included in the prompt.
    model (str): The model to be used for encoding, default is "gpt-4-1106-preview".

    Returns:
    List[dict]: The constructed RAG prompt.
    """
    # Get the encoding; default to cl100k_base
    if model == "local-model":
        encoding = tiktoken.get_encoding("cl100k_base")
    else:
        encoding = tiktoken.encoding_for_model(model)

    # 1) calculate tokens
    reserved_space = 1000
    max_messages_count = int((context_window - reserved_space) / 2)
    max_context_count = int((context_window - reserved_space) / 2)

    # 2) construct prompt
    messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    if cite_sources:
        messages.insert(-1, {"role": "user", "content": PROMPT})

    # 3) find how many tokens each list has
    messages_token_count = len(
        encoding.encode(
            "\n".join(
                [
                    f"<|im_start|>{message['role']}\n{message['content']}<|im_end|>"
                    for message in messages
                ]
            )
        )
    )
    context_token_count = len(
        encoding.encode(
            f"<|im_start|>{context_message['role']}\n{context_message['content']}<|im_end|>"
        )
    )

    # 4) Balance the token count for each
    if (messages_token_count + context_token_count) > (context_window - reserved_space):
        # context has more than limit, messages has less than limit
        if (messages_token_count < max_messages_count) and (
            context_token_count > max_context_count
        ):
            max_context_count += max_messages_count - messages_token_count
        # messages has more than limit, context has less than limit
        elif (messages_token_count > max_messages_count) and (
            context_token_count < max_context_count
        ):
            max_messages_count += max_context_count - context_token_count

    # 5) Cut each list to the max count

    # Cut down messages
    while messages_token_count > max_messages_count:
        removed_encoding = encoding.encode(
            f"<|im_start|>{messages[1]['role']}\n{messages[1]['content']}<|im_end|>"
        )
        messages_token_count -= len(removed_encoding)
        if messages_token_count < max_messages_count:
            messages = (
                [messages[0]]
                + [
                    {
                        "role": messages[1]["role"],
                        "content": encoding.decode(
                            removed_encoding[
                                : min(
                                    int(max_messages_count - messages_token_count),
                                    len(removed_encoding),
                                )
                            ]
                        )
                        .replace("<|im_start|>", "")
                        .replace("<|im_end|>", ""),
                    }
                ]
                + messages[2:]
            )
        else:
            messages = [messages[0]] + messages[2:]

    # Cut down context
    if context_token_count > max_context_count:
        # Taking a proportion of the content chars length
        reduced_chars_length = int(
            len(context_message["content"]) * (max_context_count / context_token_count)
        )
        context_message["content"] = context_message["content"][:reduced_chars_length]

    # 6) Combine both lists
    messages.insert(-1, context_message)

    return messages


def get_openai_chat_response(messages, model="gpt-4-1106-preview"):
    """
    Returns a streamed OpenAI chat response.

    Parameters:
    messages (List[dict]): List of messages to be included in the prompt.
    model (str): The model to be used for encoding, default is "gpt-4-1106-preview".

    Returns:
    str: The streamed OpenAI chat response.
    """
    try:
        response = openai.chat.completions.create(
            model=model, messages=messages, temperature=0.2, stream=True
        )

        for chunk in response:
            current_context = chunk.choices[0].delta.content
            yield current_context

    except openai.AuthenticationError as error:
        print("401 Authentication Error:", error)
        raise Exception("Invalid OPENAI_API_KEY. Please re-run with a valid key.")

    except Exception as error:
        print("Streaming Error:", error)
        raise Exception("Internal Server Error")


def get_local_chat_response(messages):
    """
    Returns a streamed chat response from a local server.

    Parameters:
    messages (List[dict]): List of messages to be included in the prompt.
    model (str): The model to be used for encoding, default is "gpt-4-1106-preview".

    Returns:
    str: The streamed chat response.
    """
    try:
        url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": -1,
            "stream": True,
        }
        response = requests.post(
            url, headers=headers, data=json.dumps(data), stream=True, timeout=120
        )

        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=None):
                decoded_chunk = chunk.decode()
                if (
                    "data:" in decoded_chunk and decoded_chunk.split("data:")[1].strip()
                ):  # Check if the chunk is not empty
                    try:
                        chunk_dict = json.loads(decoded_chunk.split("data:")[1].strip())
                        yield chunk_dict["choices"][0]["delta"].get("content", "")
                    except json.JSONDecodeError:
                        pass
        else:
            print(f"Error: {response.status_code}, {response.text}")
            raise Exception("Internal Server Error")

    except requests.exceptions.RequestException as error:
        print("Request Error:", error)
        raise Exception("Invalid request. Please check your request parameters.")
