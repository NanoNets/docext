from __future__ import annotations

import os

import requests
from litellm import completion


def sync_request(
    messages: list[dict],
    model_name: str = "hosted_vllm/Qwen/Qwen2.5-VL-3B-Instruct",
    max_tokens: int = 5000,
    num_completions: int = 1,
    format: dict | None = None,
):
    vlm_url = os.getenv("VLM_MODEL_URL", "")
    if vlm_url == "":
        raise ValueError(
            "VLM_MODEL_URL is not set. Please set it to the URL of the VLM model.",
        )
    completion_args = {
        "model": model_name,
        "messages": messages,
        "max_tokens": max_tokens,
        "n": num_completions,
        "temperature": 0,
        "api_base": vlm_url
        if model_name.startswith("hosted_vllm/") or model_name.startswith("ollama/")
        else None,
    }

    if model_name.startswith("hosted_vllm/") or model_name.startswith("ollama/"):
        completion_args["api_key"] = os.getenv("API_KEY", "EMPTY")

    # Only add format argument for Ollama models
    if model_name.startswith("ollama/") and format:
        completion_args["format"] = format
    # elif model_name.startswith("hosted_vllm/") and format: # TODO: Add this back, currently not working in colab
    #     completion_args["guided_json"] = format
    #     if "qwen" in model_name.lower():
    #         completion_args["guided_backend"] = "xgrammar:disable-any-whitespace"
    elif model_name.startswith("openrouter"):
        completion_args["response_format"] = format
    elif "gpt" in model_name.lower():
        # Only set response_format if the prompt mentions "json"
        if any("json" in m.get("text", "").lower() for m in messages if isinstance(m, dict)):
            completion_args["response_format"] = {"type": "json_object"}
        else:
            print("⚠️ Skipped response_format=json_object — prompt didn't mention 'json'.")

    response = completion(**completion_args)
    return response.json()
