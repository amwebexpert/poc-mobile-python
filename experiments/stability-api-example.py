import base64
import requests

url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image"

body = {
  "width": 512,
  "height": 512,
  "steps": 50,
  "seed": 0,
  "cfg_scale": 7,
  "samples": 1,
  "style_preset": "enhance",
  "text_prompts": [
    {
      "text": "",
      "weight": 1
    }
  ],
}

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_API_KEY",
}

response = requests.post(
  url,
  headers=headers,
  json=body,
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

for i, image in enumerate(data["artifacts"]):
    seed = image["seed"]
    filename = f"./out/txt2img_{seed}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(image["base64"]))
