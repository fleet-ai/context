from setuptools import setup, find_packages

setup(
    name="fleet-context",
    version="1.1.8",
    description="A chat interface over up-to-date Rust library documentation.",
    long_description=open("README.md", "r", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="Fleet AI",
    author_email="team@usefleet.ai",
    url="https://github.com/fleet-ai/context/tree/main",
    packages=find_packages(),
    install_requires=[
        "openai>=1.1.0",
        "rich>=13.0.0",
        "tiktoken>=0.3.3",
        "tqdm>=4.62.3",
        "fastparquet>=2023.10.0",
    ],
    py_modules=["cli", "context"],
    entry_points={
        "console_scripts": [
            "context = cli:main",
            "fleet-context = cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Rust",
    ],
    keywords="libraries, embeddings, ai",
    python_requires=">=3.9",
    project_urls={  # Optional
        "Homepage": "https://fleet.so",
        "Source": "https://github.com/fleet-ai/context",
    },
)
