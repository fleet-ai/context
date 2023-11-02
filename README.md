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

<br><br><br>

## Evaluations & benchmarks

### Methodology

We ran a hybrid human-AI evaluation pipeline to get the both of both worlds: the efficiency and bias-free strengths of language models and the accuracy of human-based evaluations. We also heavily penalize inaccuracy, much more so than what a boilerplate gpt-4 evaluations pipeline would.

We synthetically generated a list of 50 question-answer pairs for 50 randomly sampled chunks, then 50 question-answer pairs for Langchain and Pydantic.

<br>

### Results

#### Sampled libraries

WIP

#### Langchain

We saw a 48-point improvement for gpt-3.5 and a 58-point improvement for gpt-4. We hypothesize that the reason the "before" score for gpt-4 is lower is because it's better at mentioning what it doesn't know.

The drastic jump makes sense, given the entire Langchain documentation was built after gpt-4's knowledge cutoff.

<img width="50%" src="https://github.com/fleet-ai/data/assets/44193474/ac60939d-640e-42f6-94a2-02313874f5de"/>

#### Pydantic

We saw a 34-point improvement for gpt-3.5 and a 38-point improvement for gpt-4. This is because Pydantic v1 was launched before gpt-4's knowledge cutoff, but Pydantic v2 was launched in 2022. The improvement was not as sharp, but it was still significant.

<img width="50%" src="https://github.com/fleet-ai/data/assets/44193474/d46e3b81-b806-451f-93fa-e65b20e9b1a7"/>

