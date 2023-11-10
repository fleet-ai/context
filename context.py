import os
import pandas as pd
import requests
from tqdm import tqdm

from utils.ai import retrieve


def _download_file(url, filename):
    response = requests.get(url, stream=True, timeout=120)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


def download_embeddings(library_name: str) -> pd.DataFrame:
    """Downloads all embeddings and loads it up into a dataframe.

    Args:
        library_name (str): The library name for which to download the embeddings.
            See https://fleet.so/context for a list of all 1200+.
    """
    filename = f"libraries_{library_name}.parquet"
    url = f"https://s3.amazonaws.com/library-embeddings/{filename}"
    _download_file(url, filename)
    df = pd.read_parquet(filename)
    os.remove(filename)  # remove the file after reading
    print(df.head())
    return df


def query(user_query: str, k: int = 10, filters: dict = None) -> list:
    """Computes and returns a list of k results using hybrid search for a given user query.

    Args:
        user_query (str): The query for which to retrieve from.

        k (int, optional): The number of results to return. Defaults to 10.

        filters (dict, optional): Filters to apply to the query. You can filter based off
            any piece of metadata by passing in a dict of the format {metadata_name: filter_value}
            ie {"library_id": "1234"}.

            See the README for more details:
            https://github.com/fleet-ai/context/tree/main#using-fleet-contexts-rich-metadata

    Returns:
        List[dict]: A list of k results, each of which is a dict of the format:
        {
            "id": str, id of the chunk
            "score": float, similarity score
            "metadata": {
                "library_id": str, id of the library
                "page_id": str, id of the page
                "parent": str, id of the parent section
                "section_id": str (optional), HTML id of the section; use with url
                "section_index": int (optional), position within the section
                "text": str, text of the chunk
                "title": str, title of the section or page
                "type": str (optional), type of the chunk (None, function, class, attribute, etc)
                "url": str, url including section_id
            }
        },
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise Exception(
            "OPENAI_API_KEY environment variable not set. Please run `export OPENAI_API_KEY=<your api key>`."
        )

    return retrieve(
        user_query,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        k=k,
        filters=filters,
    )
