from fastapi import FastAPI, HTTPException, Header, status
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from app.models import ChatRequest, ChatResponse, PostContent
from app.strategy_generator import generate_strategy_and_captions
import openai
import yaml
import logging

# ---------- Logging ----------
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------- App Setup ----------
app = FastAPI(title="Digital Marketing API", version="1.0.0")

# ---------- Auth ----------
with open("config/application_local.yml", "r") as f:
    auth_config = yaml.safe_load(f)
API_TOKEN = auth_config.get("api_token", "")

# ---------- Image Model ----------
with open("config/llm_config.yml", "r") as f:
    llm_config = yaml.safe_load(f)
openai.api_key = llm_config["llms"]["openai"]["api_key"]
image_model_name = llm_config["llms"]["openai"].get("model", "dall-e-3")

# ---------- OpenAPI Auth ----------
bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Send your API token directly in the Authorization header (no Bearer prefix).",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "ApiTokenAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"ApiTokenAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# ---------- Routes ----------
@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse, tags=["Marketing Strategy"])
def chat_handler(request_data: ChatRequest, authorization: str = Header(None)):
    logger.info("📨 /chat request received")
    logger.info(f"📥 Authorization header received: {authorization!r}")
    logger.info(f"🔑 Expected API token: {API_TOKEN!r}")

    if not authorization:
        logger.warning("⚠️ Authorization header is missing.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header"
        )

    if authorization.strip() != API_TOKEN:
        logger.warning("❌ Invalid token received.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token"
        )

    try:
        strategy, captions, image_prompts = generate_strategy_and_captions(
            request_data.project_name,
            request_data.website_url,
            request_data.description,
            request_data.goals,
            request_data.timeframe,
        )
    except Exception as e:
        logger.exception("❌ Strategy generation failed")
        raise HTTPException(status_code=500, detail="GPT strategy generation failed")

    posts = []
    for i, (caption, image_prompt) in enumerate(zip(captions, image_prompts), start=1):
        try:
            logger.info(f"🎨 Generating image {i}: {image_prompt}")
            response = openai.images.generate(
                model=image_model_name,
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

    return ChatResponse(
        strategy=strategy,
        posts=posts,
        detected_url=str(request_data.website_url),
        detected_timeframe=request_data.timeframe
    )
