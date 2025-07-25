import openai
import yaml
import json
import logging

# ---------- Logging Setup ----------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ---------- Load OpenAI Config ----------
with open("config/llm_config.yml", "r") as f:
    config = yaml.safe_load(f)
openai.api_key = config["llms"]["openai"]["api_key"]
model_name = config["llms"]["openai"].get("chat_model", "gpt-4")

# ---------- Main Logic ----------
def generate_strategy_and_captions(restaurant_url: str, date_str: str = None):
    prompt = f"""
You are a digital marketing strategist for restaurants.

A restaurant is asking for a content strategy for their business.
Their website is: {restaurant_url or "not provided"}
They want to run the marketing campaign around: {date_str or "any suitable upcoming date"}

Your job is to generate:

1. A short marketing strategy paragraph (2–4 sentences)
2. 5 post ideas, where each post includes:
   - A social media caption (for Instagram or Facebook)
   - A visual description prompt that can be used with an image generation model like DALL·E

Respond in JSON format like:
{{
  "strategy": "Your strategy text here...",
  "posts": [
    {{
      "caption": "...",
      "image_prompt": "..."
    }},
    ...
  ]
}}
"""

    logger.info("Sending prompt to GPT for strategy generation")
    try:
        response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        raw_output = response.choices[0].message.content
        logger.debug("Raw GPT response: %s", raw_output)
        parsed = json.loads(raw_output)

        strategy = parsed["strategy"]
        captions = [p["caption"] for p in parsed["posts"]]
        image_prompts = [p["image_prompt"] for p in parsed["posts"]]

        logger.info("Successfully parsed strategy and 5 post ideas")
        return strategy, captions, image_prompts

    except Exception as e:
        logger.exception("❌ Failed to parse GPT response")
        raise RuntimeError("Failed to parse GPT response: " + str(e))
