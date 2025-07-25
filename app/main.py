from fastapi import FastAPI, HTTPException, Header
from app.models import ChatRequest, ChatResponse, PostContent
from app.parser import extract_url, extract_timeframe
from app.strategy_generator import generate_strategy_and_captions
import openai
import yaml
import logging

# ---------- Logging Setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ---------- App Setup ----------
app = FastAPI()

# ---------- Load Config ----------
with open("config/application_local.yml", "r") as f:
    auth_config = yaml.safe_load(f)
API_TOKEN = auth_config.get("api_token", "")

with open("config/llm_config.yml", "r") as f:
    llm_config = yaml.safe_load(f)
openai.api_key = llm_config["llms"]["openai"]["api_key"]
model_name = llm_config["llms"]["openai"].get("model", "dall-e-3")

# ---------- Chat Endpoint ----------
@app.post("/chat", response_model=ChatResponse)
def chat_handler(request_data: ChatRequest, authorization: str = Header(None)):
    logger.info("🔐 Received a /chat request")

    if authorization != f"Bearer {API_TOKEN}":
        logger.warning("❌ Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")

    prompt = request_data.prompt
    logger.info(f"📝 Prompt received: {prompt}")

    url = extract_url(prompt)
    timeframe = extract_timeframe(prompt)
    logger.info(f"🔗 Parsed URL: {url}")
    logger.info(f"📆 Parsed timeframe: {timeframe}")

    try:
        strategy, captions, image_prompts = generate_strategy_and_captions(url, timeframe)
        logger.info("🤖 GPT strategy + prompts generated")
    except Exception as e:
        logger.exception("❌ GPT strategy generation failed")
        raise HTTPException(status_code=500, detail="GPT generation failed")

    posts = []
    for i, (caption, image_prompt) in enumerate(zip(captions, image_prompts), start=1):
        try:
            logger.info(f"🎨 Generating image {i}: {image_prompt}")
            response = openai.images.generate(
                model=model_name,
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
        except Exception as e:
            logger.error(f"❌ Image generation failed for post {i}: {e}")
            image_url = "Image generation failed"

        posts.append(PostContent(
            caption=caption,
            image_prompt=image_prompt,
            image_url=image_url
        ))

    logger.info("✅ Finished generating strategy and images")
    return ChatResponse(
        strategy=strategy,
        posts=posts,
        detected_url=url,
        detected_timeframe=timeframe
    )
