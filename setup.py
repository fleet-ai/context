from setuptools import setup, find_packages

setup(
    name="context",
    version="0.1",
    description="A chat interface over up-to-date Python library documentation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Fleet AI",
    author_email="team@usefleet.ai",
    url="https://github.com/fleet-ai/context/tree/main",
    packages=find_packages(),
    install_requires=["openai", "rich>=13.0.0", "tiktoken>=0.1.1"],
    entry_points={
        "console_scripts": [
            "context = cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
