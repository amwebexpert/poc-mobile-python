import fs from "fs";

export const textToImage = async () => {
  const path =
    "https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image";

  const headers = {
    Accept: "application/json",
    Authorization: "Bearer YOUR_API_KEY",
  };

  const body = {
    width: 512,
    height: 512,
    steps: 50,
    seed: 0,
    cfg_scale: 7,
    samples: 1,
    style_preset: "enhance",
    text_prompts: [
      {
        text: "",
        weight: 1,
      },
    ],
  };

  const response = fetch(path, {
    headers,
    method: "POST",
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Non-200 response: ${await response.text()}`);
  }

  const responseJSON = await response.json();

  responseJSON.artifacts.forEach((image, index) => {
    fs.writeFileSync(
      `./out/txt2img_${image.seed}.png`,
      Buffer.from(image.base64, "base64")
    );
  });
};
