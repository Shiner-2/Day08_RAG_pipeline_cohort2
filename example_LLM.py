import os
from time import perf_counter

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
model = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")

if not api_key:
    raise RuntimeError("Set NVIDIA_API_KEY or OPENAI_API_KEY in .env first.")

client = OpenAI(base_url=base_url, api_key=api_key)

start_time = perf_counter()
completion = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Xin chào"}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=False,
)
end_time = perf_counter()

if completion.choices[0].message.content is not None:
    print(completion.choices[0].message.content)
print(f"Thoi gian response: {end_time - start_time:.2f} giay")
