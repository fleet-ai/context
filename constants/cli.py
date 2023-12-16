OPENAI_MODELS = [
    "gpt-4-1106-preview",
    "gpt-4",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
]

ARGUMENTS = [
    {
        "name": "k_value",
        "nickname": "k",
        "help_text": "Number of chunks to return",
        "type": int,
        "default": 15,
    },
    {
        "name": "libraries",
        "nickname": "l",
        "help_text": "Limit your chat to a list of libraries. Usage: -l library1 library2 library3",
        "type": list,
    },
    {
        "name": "model",
        "nickname": "m",
        "help_text": "Specify the model. Default: gpt-4",
        "type": str,
        "default": "gpt-4"
    },
    {
        "name": "cite_sources",
        "nickname": "c",
        "help_text": "Determines whether or not the AI model cites its sources",
        "type": bool,
        "default": True,
    },
    {
        "name": "local",
        "nickname": "n",
        "help_text": "Uses LMStudio for local models",
        "type": bool,
        "default": False,
    },
    {
        "name": "context_window",
        "nickname": "w",
        "help_text": "Context window (if using local models)",
        "type": int,
        "default": 3000,
    },
]

LIBRARIES = [
    "actix-web",
    "warp",
    "rocket",
    "reqwest",
    "ndarray",
    "polars",
    "nalgebra",
    "plotters",
    "tch-rs",
    "smartcore",
    "rustls",
    "ring",
    "ndarray",
    "polars",
    "nalgebra",
    "plotters",
    "rustls",
    "ring",
    "rusoto_core",
    "rusoto_s3",
    "diesel",
    "tokio-mysql",
    "tokio-postgres",
    "tokio", 
    "async-std"
]
