from setuptools import setup, find_packages

setup(
    name="context",
    version="0.1",
    packages=find_packages(),
    install_requires=["openai", "rich>=13.0.0", "tiktoken>=0.1.1"],
    entry_points={
        "console_scripts": [
            "context = cli:main",
        ],
    },
)
