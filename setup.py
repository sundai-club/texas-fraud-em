from setuptools import setup, find_packages

setup(
    name="Fraud_Agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "python-dotenv"
    ],
) 