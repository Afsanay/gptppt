import os
import openai


def get_images(topic: str, api_key: str):
    openai.api_key = api_key
    prompt = f"Generate images on topic {topic}. Do not produce disfigured or text-based images"
    response = openai.Image.create(
        prompt=topic,
        n=4,
        size="1024x1024"
    )
    urls = []
    for i in range(4):
        urls.append(response.data[i].url)
    return urls

# print(get_images("India","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"))
