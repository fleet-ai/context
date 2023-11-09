import os
import pandas as pd
import requests
from tqdm import tqdm


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
    filename = f"libraries_{library_name}.parquet"
    url = f"https://s3.amazonaws.com/library-embeddings/{filename}"
    _download_file(url, filename)
    df = pd.read_parquet(filename)
    os.remove(filename)  # remove the file after reading
    print(df.head())
    return df


# if __name__ == "__main__":
#     download_embeddings("llamaindex")
