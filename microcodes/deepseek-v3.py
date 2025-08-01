from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  model="meta-llama/llama-3.2-3b-instruct:free",
  extra_body={},
  messages=[
    {
        "role":"system",
        "content": "You are Kaya, a helpful diary assistant."
    },
    {
      "role": "user",
      "content": "Who has found the meaning of life? Answer in one line. Also, introduce yourself."
    }
  ]
)
print(completion.choices[0].message.content)