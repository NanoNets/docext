# PDF to Markdown API Documentation

Convert PDF documents and images to high-quality markdown format using vision-language models.

## Table of Contents
- [PDF to Markdown API Documentation](#pdf-to-markdown-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Quickstart](#quickstart)
    - [Installation](#installation)
    - [Web Interface](#web-interface)
    - [API Access](#api-access)
  - [Requirements](#requirements)
  - [Supported Models \& Platforms](#supported-models--platforms)
    - [Models with vLLM (Linux)](#models-with-vllm-linux)

## Features

- **LaTeX Equation Recognition**: Convert both inline and block LaTeX equations in images to markdown.
- **Intelligent Image Description**: Generate a detailed description for all images in the document within `<img></img>` tags.
- **Signature Detection**: Detect and mark signatures and watermarks in the document. Signatures text are extracted within `<signature></signature>` tags.
- **Watermark Detection**: Detect and mark watermarks in the document. Watermarks text are extracted within `<watermark></watermark>` tags.
- **Page Number Detection**: Detect and mark page numbers in the document. Page numbers are extracted within `<page_number></page_number>` tags.
- **Checkboxes and Radio Buttons**: Converts form checkboxes and radio buttons into standardized Unicode symbols (☐, ☑, ☒).
- **Table Detection**: Convert complex tables into html tables.

## Getting Started
### Quickstart
- [Colab notebook for onprem deployment](https://colab.research.google.com/drive/1uKO70sctH8G59yYH_rLW6CPK4Vj2YmI6?usp=sharing)

### Installation
```bash
# create a virtual environment
## install uv if not installed
curl -LsSf https://astral.sh/uv/install.sh | sh
## create a virtual environment with python 3.11
uv venv --python=3.11
source .venv/bin/activate

# Install from PyPI
uv pip install docext

# Or install from source
git clone https://github.com/nanonets/docext.git
cd docext
uv pip install -e .
```

### Web Interface

docext includes a Gradio-based web interface for easy document processing:

```bash
# Start the web interface with default configs
python -m docext.app.app --model_name hosted_vllm/nanonets/Nanonets-OCR-s

# Start the web interface with custom configs
python -m docext.app.app --model_name hosted_vllm/nanonets/Nanonets-OCR-s --max_img_size 1024 --concurrency_limit 16 # `--help` for more options
```

The interface will be available at `http://localhost:7860` with default credentials: (You can change the port by using `--server_port` flag)

- Username: `admin`
- Password: `admin`

Check [Supported Models](#supported-models--platforms) section for more options for the model.

### API Access

```python
import time
from gradio_client import Client, handle_file

def convert_pdf_to_markdown(
    client_url: str,
    username: str,
    password: str,
    file_paths: list[str]
):
    """
    Convert PDF/images to markdown using the API

    Args:
        client_url: URL of the docext server
        username: Authentication username
        password: Authentication password
        file_paths: List of file paths to convert

    Returns:
        str: Converted markdown content
    """
    client = Client(client_url, auth=(username, password))

    # Prepare file inputs
    file_inputs = [{"image": handle_file(file_path)} for file_path in file_paths]

    # Convert to markdown (non-streaming)
    result = client.predict(
        images=file_inputs,
        api_name="/process_markdown_streaming"
    )

    return result

# Example usage
# client url can be the local host or the public url like `https://6986bdd23daef6f7eb.gradio.live/`
CLIENT_URL = "http://localhost:7860"

# Single image conversion
markdown_content = convert_pdf_to_markdown(
    CLIENT_URL,
    "admin",
    "admin",
    ["assets/invoice_test.pdf"]
)
print(markdown_content)

# Multiple files conversion
markdown_content = convert_pdf_to_markdown(
    CLIENT_URL,
    "admin",
    "admin",
    ["assets/invoice_test.jpeg", "assets/invoice_test.pdf"]
)
print(markdown_content)
```
## Requirements

- Python 3.11+
- CUDA-compatible GPU (for optimal performance). Use Google Colab for free GPU access.
- Dependencies listed in requirements.txt

## Supported Models & Platforms
### Models with vLLM (Linux)

We recommend using the `hosted_vllm/nanonets/Nanonets-OCR-s` model for best performance. The model is trained to do OCR with semantic tagging. But, you can use any other VLM models supported by vLLM. Also, it is a 3B model, so it can run on a GPUs with small VRAM.

Examples:
| Model | `--model_name` |
|-------|--------------|
| Nanonets-OCR-s | `hosted_vllm/nanonets/Nanonets-OCR-s` |
| Qwen/Qwen2.5-VL-7B-Instruct-AWQ | `hosted_vllm/Qwen/Qwen2.5-VL-7B-Instruct-AWQ` |
| Qwen/Qwen2.5-VL-7B-Instruct | `hosted_vllm/Qwen/Qwen2.5-VL-7B-Instruct` |
| Qwen/Qwen2.5-VL-32B-Instruct | `hosted_vllm/Qwen/Qwen2.5-VL-32B-Instruct` |
