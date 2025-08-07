import openai
import yaml
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

with open("config/llm_config.yml", "r") as f:
    config = yaml.safe_load(f)
openai.api_key = config["llms"]["openai"]["api_key"]
model_name = config["llms"]["openai"].get("chat_model", "gpt-4")

def generate_strategy_and_captions(project_name, website_url, description, goals, timeframe):
    goals_str = ", ".join(goals)
    prompt = f"""
You are a digital marketing strategist for restaurants.

Business: {project_name}
Website: {website_url}
Goals: {goals_str}
Campaign timeframe: {timeframe or "any suitable upcoming date"}
{"Description: " + description if description else ""}

Your job is to:
1. Write a short marketing strategy paragraph (2–4 sentences)
2. Generate 2 social media post ideas (each with a caption and a DALL·E-friendly image prompt)

Respond in JSON:
{{
  "strategy": "...",
  "posts": [
    {{
      "caption": "...",
      "image_prompt": "..."
    }},
    ...
  ]
}}
""".strip()

    logger.info("Sending strategy prompt to GPT")
    try:
        response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        raw_output = response.choices[0].message.content
        parsed = json.loads(raw_output)

        strategy = parsed["strategy"]
        captions = [p["caption"] for p in parsed["posts"]]
        image_prompts = [p["image_prompt"] for p in parsed["posts"]]
        return strategy, captions, image_prompts

    except Exception as e:
        logger.exception("❌ GPT strategy parsing failed")
        raise RuntimeError(f"Failed to parse GPT response: {e}")
