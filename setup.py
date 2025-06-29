from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smartllm-router",
    version="0.1.0",
    author="SmartLLM Router Team",
    author_email="team@smartllm-router.com",
    description="🚀 Cut your LLM API costs by up to 80% with intelligent routing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smartllm-router",
    project_urls={
        "Documentation": "https://smartllm-router.readthedocs.io",
        "Source": "https://github.com/yourusername/smartllm-router",
        "Tracker": "https://github.com/yourusername/smartllm-router/issues",
        "Demo": "https://smartllm-demo.streamlit.app",
        "Changelog": "https://github.com/yourusername/smartllm-router/releases",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Framework :: Flask",
    ],
    keywords="llm ai openai anthropic cost optimization routing machine-learning",
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.8.0",
        "google-generativeai>=0.3.0",
        "mistralai>=0.0.7",
        "tiktoken>=0.5.0",
        "numpy>=1.24.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "plotly>=5.17.0",
        "pandas>=2.0.0",
        "redis>=5.0.0",  # For distributed caching
        "prometheus-client>=0.19.0",  # For metrics
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
            "plotly>=5.17.0",
            "altair>=5.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "smartllm-dashboard=smartllm_router.dashboard:main",
            "smartllm-benchmark=smartllm_router.benchmark:main",
        ],
    },
)