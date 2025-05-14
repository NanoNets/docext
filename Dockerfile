FROM vllm/vllm-openai:v0.8.2 AS dev

# 安装 Python 3.11
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3.11 python3.11-venv python3-pip python3.11-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.11 /usr/bin/python

ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
EXPOSE 7860

WORKDIR /app

RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY requirements.txt setup.py README.md /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY docext /app/docext
RUN pip install --no-cache-dir -e .

# flash-attn 可选（没有 CUDA 也不会炸）
RUN pip install --no-cache-dir flash-attn --no-build-isolation || true

# ✅ 环境变量接口配置，不写死！
ENV API_KEY=""
ENV VLM_MODEL_URL=""
ENV MODEL_NAME="gpt-4.1"
ENV VLM_SERVER_HOST="api.openai.com"
ENV VLM_SERVER_PORT=443
ENV UI_PORT=7860

# ✅ ENTRYPOINT 使用 shell 展开 env vars
# 注意用 bash 包裹一层让变量能生效
ENTRYPOINT ["/bin/bash", "-c", "\
  /app/.venv/bin/python -m docext.app.app \
  --model_name \"$MODEL_NAME\" \
  --vlm_server_host \"$VLM_SERVER_HOST\" \
  --vlm_server_port \"$VLM_SERVER_PORT\" \
  --ui_port \"$UI_PORT\" \
  --no-share"]
