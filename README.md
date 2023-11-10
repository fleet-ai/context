<h1 align="center">🛩️ Fleet Context</h1>

<p align="center">
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
    <a href="https://discord.gg/YTc98S77aZ"><img src="https://img.shields.io/discord/1107887761412870154?logo=discord&style=flat&logoColor=white" alt="Discord"/></a>
    <br>
    <br>
    <b>A CLI tool over the top 1221 Python libraries.</b>
    <br>
    <span>Used for library q/a & code generation with all available OpenAI models</span>
    <br>
    <br>
    <a href="https://alpha.usefleet.ai/context">Website</a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://atlas.nomic.ai/map/67dc2d8f-5161-46fe-9d73-5fda6f3f5cde/758aa80f-8f11-4f8f-b008-f402e61c48d4?xs=-41.15425&xf=41.09514&ys=-30.76443&yf=32.33730">Data Visualizer</a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://pypi.org/project/fleet-context/">PyPI</a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://x.com/fleet_ai">@fleet_ai</a>‎
    <br>
    <br>
    <br>
</p>

https://github.com/fleet-ai/context/assets/44193474/80381b25-551e-4602-8987-071e92354f6f

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

If you have an existing package that already uses the keyword `context`, you can also activate Fleet Context by running:

```shell
fleet-context
```

<br><br><br>

## API

### Downloading embeddings

You can download any library's embeddings and load it up into a dataframe by running:

```python
from context import download_embeddings

df = download_embeddings("langchain")
```

```shell
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 901k/901k [00:00<00:00, 2.64MiB/s]
                                     id                                   dense_embeddings                                           metadata                                      sparse_values
0  91cd9f22-b3b6-49e1-8672-e1e42a1cf766  [-0.014795871, -0.013938751, 0.02374646, -0.02...  {'id': '91cd9f22-b3b6-49e1-8672-e1e42a1cf766',...  {'indices': [4279915734, 3106554626, 771291085...
1  80cd620e-7408-4649-aaa7-3fe3c719b4ed  [-0.0027519625, 0.013772411, 0.0019546314, -0....  {'id': '80cd620e-7408-4649-aaa7-3fe3c719b4ed',...  {'indices': [1497795724, 573857107, 2203090375...
2  87a406ad-e413-42fc-8813-6fa042f80f6a  [-0.022883521, -0.0036436971, 0.0026068306, 0....  {'id': '87a406ad-e413-42fc-8813-6fa042f80f6a',...  {'indices': [1558403699, 640376310, 358389376,...
3  8bdd8dae-8384-414d-87d2-4390ca29d857  [-0.024882555, -0.0041470923, -0.011419726, -0...  {'id': '8bdd8dae-8384-414d-87d2-4390ca29d857',...  {'indices': [1558403699, 3778951566, 274301652...
4  8cc5eb61-317a-4196-8099-51c47ef70406  [-0.036361936, 0.0027855083, -0.013214805, -0....  {'id': '8cc5eb61-317a-4196-8099-51c47ef70406',...  {'indices': [3586802366, 1110127215, 161253108...
```

You can see a full list of supported libraries & search through them [on our website](https://fleet.so/context) at the bottom of the page.

<br>

### Querying

If you'd like to directly query from our hosted vector database, you can run:

```python
from context import query

results = query("How do I set up Langchain?")
for result in results:
    print(f"{result["metadata"]["text"]}\n{result["metadata"]["text"])}")
```
```shell
[
    {
        'id': '859e8dff-f9ec-497d-aa07-344e48b2f67b',
        'score': 0.848275101,
        'values': [],
        'metadata': {
            'library_id': '4506492b-70de-49f1-ba2e-d65bd7048a28',
            'page_id': '732e264c-c077-4978-bc93-380d7dc28983',
            'parent': '3be9bbcc-b5d6-4a91-9f72-a570c2db33e5',
            'section_id': '',
            'section_index': 0.0,
            'text': "Quickstart ## Installation\u200b To install LangChain run: - Pip - Conda pip install langchain conda install langchain -c conda-forge For more details, see our Installation guide. ## Environment setup\u200b Using LangChain will usually require integrations with one or more model providers, data stores, APIs, etc. For this example, we'll use OpenAI's model APIs. First we'll need to install their Python package: pip install openai Accessing the API requires an API key, which you can get by creating an account and heading here.",
            'title': 'Quickstart | 🦜️🔗 Langchain',
            'type': '',
            'url': 'https://python.langchain.com/docs/get_started/quickstart'
        }
    },
    # ...and 9 more
]
```

<br>

You can also set a custom k value and filters by any metadata field we support (listed below), plus `library_name`:

```python
results = query("How do I set up Langchain?", k=15, filters={"library_name": "langchain"})
```

<br>

### Using Fleet Context's rich metadata

One of the biggest advantages of using Fleet Context's embeddings is the **amount of information preserved** throughout the chunking and embeddings process. You can take advantage of the metadata to improve the quality of your retrievals significantly.

Here's a full list of metadata that we support.

**IDs**:
- **`library_id`**: the uuid of the library referenced
- **`page_id`**: the uuid of the page the chunk was retrieved from
- **`parent`**: the uuid of the section the chunk was retrieved from (not to be confused with section_id)

**Page/section information**:
- **`url`**: the url of the section or page the chunk was retrieved from, formatted as `f"{page_url}#{section_id}`
- **`section_id`**: the section's `id` field from the html
- **`section_index`**: the ordering of the chunk within the section. If there are 2 chunks that have the same parent, this will tell you which one was presented first.

**Chunk information**:
- **`title`**: the title of the section or of the page (if section title does not exist)
- **`text`**: the text, formatted in markdown. Note that markdown is removed from the embeddings for better retrieval results.
- **`type`**: the type of the chunk. Can be `None` (most common) or a defined value like `class`, `function`, `attribute`, `data`, `exception`, and more.

<br>

### Improving retrievals with Fleet Context

#### Re-ranking with `section_index`

Re-ranking is commonly known to improve results pretty dramatically. We can take that a step further and take advantage of the fact that the _ordering within each section/page_ is preserved, because it follows that ordering content in the order of which it is presented to the reader will likely derive the best results.

Use `section_index` to do a smart reranking of your chunks.

<br>

#### Parent/child retrieval with `parent`

If you notice 2 or more chunks with the same `parent` field and are relatively similar in position on the page via `section_index`, you can go up one level and query all chunks with the same `parent` uuid and pass in the entire document.

<br>

#### Better filtering and prompt construction with `type`

On retrieval, you can map intent and filter via `type`. If the user intends to generate code, you can pre-filter your retrieval to filter `type` to just `class` or `function`. You can use this in creative ways. We've found that pairing it with OpenAI's function calling works really well.

Also, `type` allow you to construct your prompt with more clarity, and display more rich information to the user. For example, adding the type to the prompt followed by the chunk will produce better results, because it allows the language model to understand what the chunk is trying to say.

Note that `type` is not guaranteed to be present and defined for all libraries — only the ones that have had their documentation generated by Sphinx/readthedocs.

<br>

#### Rich prompt construction & information presentation with `text`

Our `text` field preserves all information from the HTML elements by converting it to Markdown. This allows for two big advantages:

1. From our tests, we've discovered that language models perform better with markdown formatting than without
2. You're able to display rich information (titles, urls, images) to the user if you're sourcing a chunk

<br>

#### Precise sourcing with `url` and `section_id`

You can link the user to the exact section with `url` (if supported, it's already pre-loaded with the section within the page).

<br><br><br>

## CLI Tool

### Limit libraries

You can use the `-l` or `--libraries` followed by a list of libraries to limit your session to a certain number of libraries. Defaults to all. View a list of all supported libraries on [our website](https://fleet.so/context).

```shell
context -l langchain pydantic openai
```

<br>

### Use a different OpenAI model

You can select a different OpenAI model by using `-m` or `--model`. Defaults to `gpt-4`. You can set your model to `gpt-4-1106-preview` (gpt-4-turbo), `gpt-3.5-turbo`, or `gpt-3.5-turbo-16k`.

```shell
context -m gpt-4-1106-preview
```

<br>

### Use non-OpenAI models

You can use Claude, CodeLlama, Mistral, and many other models by
1. creating an API key on [OpenRouter](https://openrouter.ai) (visit the [Keys](https://openrouter.ai/keys) page after signing up)
2. setting `OPENROUTER_API_KEY` as an environment variable
3. specifying your model using the company prefix, e.g.:

```shell
context -m phind/phind-codellama-34b
```

OpenAI models work this way as well; just use e.g. `openai/gpt-4-32k`. Other model options are available [here](https://openrouter.ai/models).

Optionally, you can attribute your inference token usage to your app or website by setting `OPENROUTER_APP_URL` and `OPENROUTER_APP_TITLE`. Your app will show on the homepage of https://openrouter.ai if ranked.

<br>

### Using local models

Local model support is powered by [LM Studio](https://lmstudio.ai). To use local models, you can use `--local` or `-n`:

```shell
context --local
```

You need to download your local model through LM Studio. To do that:

1. Download LM Studio. You can find the download link here: https://lmstudio.ai
2. Open LM Studio and download your model of choice.
3. Click the ↔ icon on the very left sidebar
4. Select your model and click "Start Server"

The context window is defaulted to 3000. You can change this by using `--context_window` or `-w`:

```shell
context --local --context_window 4096
```

<br>

### Advanced settings

You can control the number of retrieved chunks by using `-k` or `--k_value` (defaulted to 15), and you can toggle whether the model cites its source by using `-c` or `--cite_sources` (defaults to true).

```shell
context -k 25 -c false
```

<br><br><br>

## Evaluations

### Results

#### Sampled libraries

We saw a 37-point improvement for `gpt-4` generation scores and a 34-point improvement for `gpt-4-turbo` generation scores amongst a randomly sampled set of 50 libraries.

We attribute this to a lack of knowledge for the most up-to-date versions of libraries for `gpt-4`, and a combination of relevant up-to-date information to generate with and relevance of information for `gpt-4-turbo`.

<img width="50%" src="https://github.com/fleet-ai/context/assets/44193474/1ee13497-adbe-4f80-8782-3d4172a7d956">

<br><br><br>

## Embeddings

Check out our visualized data [here](https://atlas.nomic.ai/map/67dc2d8f-5161-46fe-9d73-5fda6f3f5cde/758aa80f-8f11-4f8f-b008-f402e61c48d4?xs=-41.15425&xf=41.09514&ys=-30.76443&yf=32.33730).

You can download all embeddings [here](https://drive.google.com/drive/u/0/folders/1Gz6lx8dP9QXObQgbMn2AUvalS8s7ExU4).

<img width="100%" alt="Screenshot 2023-11-06 at 10 01 22 PM" src="https://github.com/fleet-ai/context/assets/44193474/c7aeca8a-5a62-4655-a2c6-4d16846b330d">
