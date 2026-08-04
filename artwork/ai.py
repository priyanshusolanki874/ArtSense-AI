import os
import base64
import requests


API_KEY = os.getenv("OPENROUTER_API_KEY")


def analyze_artwork(image_path):

    with open(image_path, "rb") as image:
        image_data = base64.b64encode(image.read()).decode("utf-8")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },

        json={

            "model": "google/gemini-2.5-flash-lite",

            "messages": [

                {
                    "role": "user",

                    "content": [

                        {
                            "type": "text",

                            "text": """
You are a professional art teacher.

Analyze the uploaded artwork.

Return ONLY valid JSON in exactly this format:

{
    "score": 0,
    "strengths": [
        "",
        "",
        ""
    ],
    "weaknesses": [
        "",
        "",
        ""
    ],
    "suggestions": [
        "",
        "",
        ""
    ]
}

Rules:
- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT use ```json.
- Do NOT write any explanation before or after the JSON.
- Score must be between 0 and 100.
- Give exactly 3 strengths.
- Give exactly 3 weaknesses.
- Give exactly 3 suggestions.
"""
                        },

                        {
                            "type": "image_url",

                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }

                    ]
                }

            ]

        }

    )

    if response.status_code != 200:
        print(response.json())
        return "AI analysis failed."

    return response.json()["choices"][0]["message"]["content"]