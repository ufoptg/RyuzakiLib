import os
import re

import setuptools


def read(fname, version=False):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8") as f:
        text = f.read()
    if version:
        match = re.search(r'__version__ = "(.*?)"', text)
        if match:
            return match.group(1)
        raise RuntimeError("Version string not found.")
    return text


setuptools.setup(
    name="RyuzakiLib",
    packages=setuptools.find_packages(),
    version=read("RyuzakiLib/__version__.py", version=True),  # Ensure this works properly
    license="MIT",
    description="RyuzakiLib Python Wrapper For API etc",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="TeamKillerX",
    author_email="killerx@randydev.my.id",
    url="https://github.com/TeamKillerX/RyuzakiLib/",
    keywords=["API", "RyuzakiLib", "Ryuzaki_Library", "Ryuzaki-API"],
    install_requires=[
        "requests",
        "aiohttp",
        "aiofiles",
        "pyrogram",
        "bs4",
        "google-search-results",
        "httpx[http2]",
        "Python-IO",
        "Pillow",
        "openai",
        "tqdm",
        "pre-commit",
        "gpytranslate",
        "Flask",
        "pymongo",
        "pytz",
        "urllib3",
        "pydantic",
        "typing-extensions",
        "typing",
        "deprecation",
        "ntgcalls>=1.0.2",
        "psutil",
        "screeninfo",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires="~=3.7",
)
