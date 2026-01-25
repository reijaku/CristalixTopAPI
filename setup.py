from setuptools import setup, find_packages

setup(
    name="cristalix",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "curl-cffi",
    ],
    python_requires=">=3.10",
    description="Python SDK для Cristalix API (Players & Statistics)",
    url="https://github.com/reijaku/CristalixTopAPI",
    author="Anton",
    author_email="atrofimov619@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
