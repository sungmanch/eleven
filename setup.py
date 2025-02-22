from setuptools import setup, find_packages

setup(
    name="eleven",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain-openai>=0.0.5",
        "langgraph>=0.0.10",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
)