from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="limma",
    version="0.2.1",
    author="Yash Kumar Firoziya",
    author_email="ykfiroziya@gmail.com",
    description="Language Interface Model for Machine Automation - Control ESP devices with natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firoziya/limma",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.0",
        "SpeechRecognition>=3.8.1",
        "pyttsx3>=2.90",
    ],
    package_data={
        'speech_recognition': ['*.wav'],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",   
        ],
        "mic": ["pyaudio"],
    },
    keywords="esp8266 esp32 iot microcontroller natural-language automation home-automation limma",
    project_urls={
        "Bug Reports": "https://github.com/firoziya/limma/issues",
        "Source": "https://github.com/firoziya/limma",
        "Documentation": "https://pylimma.vercel.app/docs/",
    },
)