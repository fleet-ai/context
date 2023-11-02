<h1 align="center">🛩️ Fleet Context</h1>

<p align="center">
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
    <br>
    <br>
    <b>Code generation with up-to-date Python libraries.</b>
    <br>
    <br><a href="https://alpha.usefleet.ai">WIP View the site</a>‎ ‎ |‎ ‎ <a href="https://alpha.usefleet.ai/">WIP API waitlist</a>
    <br>
</p>

![Screenshot 2023-11-01 at 1 02 26 AM](https://github.com/fleet-ai/data/assets/44193474/3229b87c-74bc-46ab-afc2-bb0bc598a6d0)


<br><br><br>

## Quick Start

Install the package and run `context` to ask questions about the most up-to-date Python libraries. You will have to provide your OpenAI key to start a session.

```shell
pip install fleet-libraries
```
```shell
context
```

<br>

### Limit libraries

You can use the `-l` or `--libraries` followed by a list of libraries to limit your session to a certain number of libraries. Defaults to all.
```shell
context -l langchain pydantic openai
```

<br>

### Use a different OpenAI model

You can select a different OpenAI model by using `-m` or `--model`. Defaults to `gpt-4`. You can set your model to `gpt-4-32k` (if your organization has access), `gpt-3.5-turbo`, or `gpt-3.5-turbo-16k`.
```shell
context -m gpt-3.5-turbo
```

<br>

### Advanced settings

You can control the number of retrieved chunks by using `-k` or `--k_value` (defaulted to 10), and you can toggle whether the model cites its source by using `-c` or `--cite_sources` (defaults to true).
```shell
context -k 15 -c false
```
