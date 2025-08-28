from setuptools import setup, find_packages
import os

# Read README
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Language Interface Model for Machine Automation - Control ESP devices with natural language"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["requests>=2.25.0"]

setup(
    name="limma",
    version="0.1.0",
    author="Yash Kumar Firoziya",
    author_email="ykfiroziya@gmail.com",
    description="Language Interface Model for Machine Automation - Control ESP devices with natural language",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/firoziya/limma",
    project_urls={
        "Bug Reports": "https://github.com/firoziya/limma/issues",
        "Source": "https://github.com/firoziya/limma",
        "Documentation": "https://pylimma.vercel.app/docs/",
        "Homepage": "https://github.com/firoziya/limma",
        "API Key": "https://pylimma.vercel.app/",
        "Changelog": "https://github.com/firoziya/limma/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        "Topic :: Home Automation",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "twine>=3.0",
        ],
        "voice": [
            "pyvoicekit",
        ],
    },
    keywords=[
        "esp8266", "esp32", "iot", "microcontroller", 
        "natural-language", "automation", "home-automation", "limma"
    ],
    include_package_data=True,
    zip_safe=False,
    license="Apache-2.0",
    platforms=["any"],
)
