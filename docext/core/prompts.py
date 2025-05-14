from __future__ import annotations

import pandas as pd
from PIL import Image

from docext.core.utils import encode_image


def _get_name_desc_prompt(fields: list[str], fields_description: list[str]) -> str:
    return "\n".join(
        [
            f"{field.replace(' ', '_').lower()}: {description}"
            for field, description in zip(fields, fields_description)
        ],
    )


def _get_fields_output_format(fields: list[str]) -> dict:
    return {field.replace(" ", "_").lower(): "..." for field in fields}


def get_fields_messages(
    fields: list[str],
    fields_description: list[str],
    filepaths: list[str],
) -> list[dict]:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Extract the following fields from the documents:\n {_get_name_desc_prompt(fields, fields_description)}.",
                },
                {"type": "text", "text": f"Documents:\n"},
                *[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(filepath)}",
                        },
                    }
                    for filepath in filepaths
                ],
                {
                    "type": "text",
                    "text": f"Return a JSON with the following format:\n {_get_fields_output_format(fields)}. If a field is not found, return '' for that field. Do not give any explanation.",
                },
            ],
        },
    ]
    return messages


def _get_tables_output_format(columns: list[str]) -> str:
    return pd.DataFrame({col: [".."] for col in columns}).to_markdown(index=False)


def get_tables_messages(
    columns_names: list[str],
    columns_description: list[str],
    filepaths: list[str],
) -> list[dict]:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Extract the following columns from the documents:\n {_get_name_desc_prompt(columns_names, columns_description)}.",
                },
                {"type": "text", "text": f"Documents:\n"},
                *[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(filepath)}",
                        },
                    }
                    for filepath in filepaths
                ],
                # {
                #     "type": "text",
                #     "text": f"Return the table as an markdown table:\n {_get_tables_output_format(columns_names)}. If a cell is not found, return '' for that column. Do not give any explanation.",
                # },
                {
                    "type": "text",
                    "text": f"Return the table in markdown format (or JSON if possible). Example:\n {_get_tables_output_format(columns_names)}. If a cell is not found, return '' for that column. Do not give any explanation.",
                }

            ],
        },
    ]
    return messages
