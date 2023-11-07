<h1 align="center">🛩️ Fleet Context</h1>

<p align="center">
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
    <br>
    <br>
    <b>A CLI tool over the top 1200 Python libraries.</b>
    <br>
    <span>Used for library q/a & code generation with gpt-4-turbo</span>
    <br>
    <br>
    <a href="https://alpha.usefleet.ai/context">Website</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://atlas.nomic.ai/map/ab7a1860-a8ed-4c71-a181-3fa8bc4ad1ce/03b0f694-13bf-464c-9b85-abb6e4286770">Data visualizer</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://pypi.org/project/fleet-context/1.0.7/">PyPI</a>‎
    <br>
    <br>
    <br>
</p>

<img width="100%" alt="Screenshot 2023-11-06 at 10 01 22 PM" src="https://github.com/fleet-ai/context/assets/44193474/c7aeca8a-5a62-4655-a2c6-4d16846b330d">

<br><br><br>

## Quick Start

Install the package and run `context` to ask questions about the most up-to-date Python libraries. You will have to provide your OpenAI key to start a session.

```shell
pip install fleet-context
context
```

If you'd like to run the CLI tool locally, you can clone this repository, cd into it, then run:

```shell
pip install -e .
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

You can select a different OpenAI model by using `-m` or `--model`. Defaults to `gpt-4-1106-preview` (gpt-4-turbo). You can set your model to `gpt-4` if you want more stable gpt-4 results, `gpt-3.5-turbo`, or `gpt-3.5-turbo-16k`.

```shell
context -m gpt-3.5-turbo
```

<br>

### Advanced settings

You can control the number of retrieved chunks by using `-k` or `--k_value` (defaulted to 10), and you can toggle whether the model cites its source by using `-c` or `--cite_sources` (defaults to true).

```shell
context -k 15 -c false
```

<br><br><br>

## Evaluations

### Results

#### Sampled libraries

We saw a 37-point improvement for `gpt-4` generation scores and a 34-point improvement for `gpt-4-turbo` generation scores amongst a randomly sampled set of 50 libraries.

We attribute this to a lack of knowledge for the most up-to-date versions of libraries for `gpt-4`, and a combination of relevant up-to-date information to generate with and relevance of information for `gpt-4-turbo`.

<img width="50%" src="https://github.com/fleet-ai/context/assets/44193474/1ee13497-adbe-4f80-8782-3d4172a7d956">
