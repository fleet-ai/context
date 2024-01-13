# pylint: disable=E0401
# pylint: disable=W0122
# pylint: disable=W0718

import os
import sys
import argparse
import traceback
from functools import partial

from getpass import getpass
from rich import print as rprint
try:
    import panel as pn
except ImportError:
    raise ImportError(
        "Panel is not installed. Please install panel using `pip install panel`."
    )

pn.extension()

from utils.utils import print_markdown, print_exception, extract_code_blocks, print_help
from utils.stream import TextStream
from utils.ai import (
    retrieve_context,
    construct_prompt,
    get_remote_chat_response,
    get_other_chat_response,
)

from constants.cli import ARGUMENTS, LIBRARIES, OPENAI_MODELS
from constants.ai import MODELS_TO_TOKENS


def respond(k, filters, model, cite_sources, context_window, contents, user, instance):
    messages = instance.serialize()
    messages.append({"role": "user", "content": contents.strip()})
    rag_context = retrieve_context(contents, k=k, filters=filters)
    prompts = construct_prompt(
        messages,
        rag_context,
        model=model,
        cite_sources=cite_sources,
        context_window=context_window,
    )
    try:
        message = None
        if model in OPENAI_MODELS:
            for response in get_remote_chat_response(prompts, model=model):
                if response:
                    message = instance.stream(response, message=message)
        else:
            for response in get_other_chat_response(prompts, model=model):
                if response:
                    message = instance.stream(response, message=message)
    finally:
        pass
        # # Execute code blocks
        # code_blocks = extract_code_blocks(full_response)
        # if code_blocks:
        #     user_response = input("Run code? (y/n): ")
        #     if user_response not in ["y", "n"]:
        #         rprint("Invalid response. Please input 'y' or 'n'.")
        #     elif user_response == "y":
        #         try:
        #             exec(code_blocks)
        #         except Exception:
        #             exc_type, exc_value, exc_traceback = sys.exc_info()
        #             print_exception(exc_type, exc_value, exc_traceback)

        #             messages.append(
        #                 {
        #                     "role": "user",
        #                     "content": f"An exception occured. {''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}",
        #                 }
        #             )



def main():
    parser = argparse.ArgumentParser(description="Fleet Data Retriever UI", add_help=False)
    parser.add_argument("help", nargs="?", default=argparse.SUPPRESS)

    # Add arguments
    for arg in ARGUMENTS:
        if arg["type"] == bool:
            default = arg["default"] if "default" in arg else None
            parser.add_argument(
                f'-{arg["nickname"]}',
                f'--{arg["name"]}',
                dest=arg["name"],
                help=arg["help_text"],
                action="store_true",
                default=default,
            )
        elif arg["type"] == list:
            choices = arg["choices"] if "choices" in arg else None
            default = arg["default"] if "default" in arg else None

            parser.add_argument(
                f'-{arg["nickname"]}',
                f'--{arg["name"]}',
                dest=arg["name"],
                help=arg["help_text"],
                type=str,
                nargs="+",
                choices=choices,
                default=default,
            )
        else:
            choices = arg["choices"] if "choices" in arg else None
            default = arg["default"] if "default" in arg else None

            parser.add_argument(
                f'-{arg["nickname"]}',
                f'--{arg["name"]}',
                dest=arg["name"],
                help=arg["help_text"],
                type=arg["type"],
                choices=choices,
                default=default,
            )

    # Hit the retrieve endpoint
    args = parser.parse_args()
    k = args.k_value
    model = args.model
    cite_sources = args.cite_sources
    filters = {}

    if getattr(args, "help", None) is not None:
        print_help()
        return

    # If library specified, match library name to uuid
    if args.libraries:
        for library in args.libraries:
            if library not in LIBRARIES:
                rprint(
                    "Library not found. Please refer to the list of available libraries."
                )
                return
        filters["library_name"] = args.libraries

    # Get context window
    if model in OPENAI_MODELS:
        context_window = MODELS_TO_TOKENS[model]
    else:
        context_window = args.context_window

    # If local model requested, use LMStudio
    api_key = ""
    if args.local:
        model = "local-model"
        print_markdown(
            f"""---

        **You are using a local model.**
        We're working with LM Studio to provide access to local models for you. Download and start your model to get started.

        Instructions:
        1. Download LM Studio. You can find the download link here: https://lmstudio.ai
        2. Open LM Studio and download your model of choice.
        3. Click the **↔ icon** on the very left sidebar
        4. Select your model and click "Start Server"

        Note that your context window is set to {context_window}. To change this, run `context --context_window <context window>`.

        ---"""
        )

    else:
        openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")

        # Get the OpenAI API key, if not found
        if model in OPENAI_MODELS and not openai_key:
            print_markdown(
                """---
            !!!**OpenAI API key not found.**

            Please provide a key to proceed.
            ---
            """
            )
            openai_key = getpass("OpenAI API key: ")
            os.environ["OPENAI_API_KEY"] = openai_key

            print_markdown(
                """
            ---

            **Tip**: To save this key for later, run `export OPENAI_API_KEY=<your key>` on mac/linux or `setx OPENAI_API_KEY <your key>` on windows.
        
            For non-OpenAI models, you should set `OPENROUTER_API_KEY`, and optionally `OPENROUTER_APP_URL` and `OPENROUTER_APP_TITLE`.

            ---"""
            )

        # Otherwise, grab the openrouter key, if not found
        elif model not in OPENAI_MODELS and not openrouter_key:
            print_markdown(
                """---
            !!!**OpenRouter API key not found.**

            Please provide a key to proceed.
            ---
            """
            )
            api_key = getpass("OpenRouter API key: ")
            os.environ["OPENROUTER_API_KEY"] = api_key

            print_markdown(
                f"""
            ---

            **Tip**: To save this key for later, run `export OPENROUTER_API_KEY=<your key>` on mac/linux or `setx OPENROUTER_API_KEY <your key>` on windows.
        
            You can optionally set `OPENROUTER_APP_URL` and `OPENROUTER_APP_TITLE`, too.

            Note that your context window is set to {context_window}. To change this, run `context --context_window <context window>`.

            ---"""
            )

    if model == "gpt-4-1106-preview":
        print_markdown(
            """!!!Welcome to Fleet Context!
        Generate and run code using the most up-to-date libraries.
        
        *Warning*: You are using gpt-4-turbo, which is not yet stable and is rate limited at 100 requests per day. Please use with caution.
        
        """
        )
    else:
        print_markdown(
            """!!!Welcome to Fleet Context!
        Generate and run code using the most up-to-date libraries.
        
        """
        )
    partial_respond = partial(respond, k, filters, model, cite_sources, context_window)

    chat_interface = pn.chat.ChatInterface(callback=partial_respond)
    template = pn.template.FastListTemplate(main=[chat_interface], title="Fleet Context UI")
    template.show()


if __name__ == "__main__":
    main()
