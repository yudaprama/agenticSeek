from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agenticSeek",
    version="0.1.0",
    author="Fosowl",
    author_email="mlg.fcu@gmail.com",
    description="The open, local alternative to ManusAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fosowl/agenticSeek",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.115.12",
        "celery>=5.5.1",
        "uvicorn>=0.34.0",
        "flask>=3.1.0",
        "aiofiles>=24.1.0",
        "pydantic>=2.10.6",
        "pydantic_core>=2.27.2",
        "requests>=2.31.0",
        "sacremoses>=0.0.53",
        "numpy>=1.24.4",
        "colorama>=0.4.6",
        "python-dotenv>=1.0.0",
        "ollama>=0.4.7",
        "protobuf>=3.20.3",
        "termcolor>=2.5.0",
        "ipython>=8.34.0",
        "selenium>=4.29.0",
        "markdownify>=1.1.0",
        "chromedriver-autoinstaller>=0.6.4",
        "httpx>=0.27,<0.29",
        "anyio>=3.5.0,<5",
        "distro>=1.7.0,<2",
        "jiter>=0.4.0,<1",
        "fake_useragent>=2.1.0",
        "selenium_stealth>=1.0.6",
        "undetected-chromedriver>=3.5.5",

        "sniffio",
        "tqdm>4"
    ],

    entry_points={
        "console_scripts": [
            "agenticseek=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
