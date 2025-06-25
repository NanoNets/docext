FROM vllm/vllm-openai:v0.8.2 AS dev

# Install Python 3.11
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3.11 python3.11-venv python3-pip python3.11-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure Python 3.11 is default
RUN ln -sf /usr/bin/python3.11 /usr/bin/python

ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
EXPOSE 7860

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
COPY requirements.txt setup.py README.md /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY docext /app/docext

# Install application
RUN pip install --no-cache-dir -e .

# Install flash-attn separately
RUN pip install --no-cache-dir flash-attn --no-build-isolation

# Set working directory and entrypoint
WORKDIR /app/
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser
USER appuser
ENTRYPOINT ["/app/.venv/bin/python", "-m", "docext.app.app", "--no-share", "--ui_port", "7860"]
