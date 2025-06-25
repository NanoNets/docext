from __future__ import annotations

import requests
from PIL import Image


def cleanup(signum, frame, vllm_server):
    print("\nReceived exit signal. Stopping vLLM server...")
    vllm_server.stop_server()
    exit(0)


def check_vllm_healthcheck(host: str, port: int):
    try:
        response = requests.get(f"https://{host}:{port}/healthcheck")
        return response.status_code == 200
    except Exception as e:
        return False


def check_ollama_healthcheck(host: str, port: int):
    try:
        response = requests.get(f"https://{host}:{port}")
        return response.status_code == 200
    except Exception as e:
        return False


if __name__ == "__main__":
    print(check_ollama_healthcheck("localhost", 11434))
    print(check_vllm_healthcheck("localhost", 8000))
