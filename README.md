# 🤖 AI Marketing Strategy Generator

This project provides a backend API that uses GPT-4 and DALL·E to generate digital marketing strategies and social media content — including **captions** and **AI-generated images** — for restaurant businesses.

---

## 🚀 Features

- 🔎 Extracts restaurant website & campaign timeframe from user prompts
- 🧠 Uses **GPT-4** to generate:
  - Marketing strategy
  - 5 social media post captions
  - 5 visual prompts for DALL·E
- 🎨 Uses **DALL·E** to generate images based on prompts
- 🔐 Token-based API authorization
- 🐳 Deployable via Docker

---

## 📦 Example Request

```
POST /chat
Authorization: Bearer your-secret-token
Content-Type: application/json

{
  "prompt": "Promote my Italian bistro next week. Website: https://bellissimofood.com"
}
```

---

## 📦 Example Response

```json
{
  "strategy": "Engage customers with authentic Italian dishes, focusing on freshness and family dining...",
  "posts": [
    {
      "caption": "Experience the taste of Italy this weekend 🍝",
      "image_prompt": "A cozy Italian bistro with wine, pasta and candlelight",
      "image_url": "https://..."
    },
    ...
  ],
  "detected_url": "https://bellissimofood.com",
  "detected_timeframe": "2025-08-01"
}
```

---

## 🛠️ Setup

### 1. Clone the project

```bash
git clone https://github.com/Anishyou/ai-marketing.git
cd ai-marketing
```

### 2. Add your config files

Create the following in `config/`:

#### `application_local.yml`
```yaml
api_token: your-secret-token
```

#### `llm_config.yml`
```yaml
llms:
  openai:
    api_key: YOUR_OPENAI_API_KEY
    model: dall-e-3
    chat_model: gpt-4
```

---

### 3. Run with Docker

```bash
docker-compose up --build
```

App will be available at:  
📍 `http://localhost:8080/chat`

---

## 🧪 Testing with Postman

- POST to `http://localhost:8080/chat`
- Headers:
  ```
  Authorization: Bearer your-secret-token
  Content-Type: application/json
  ```
- Body (JSON):
  ```json
  {
    "prompt": "Promote our burger joint next week. Website: https://burgerblast.com"
  }
  ```

---

## 📁 Project Structure

```
ai-marketing/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   └── strategy_generator.py
├── config/
│   ├── application_local.yml
│   └── llm_config.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚠️ Notes

- This is an MVP — the LLM prompt is currently static.
- `next week` or similar phrases are parsed to real dates internally.
- DALL·E is used directly via OpenAI’s API.

---

## 📌 Roadmap Ideas

- ✅ Add logging (done)
- 🔒 Switch to OAuth or JWT
- 🖼️ Support Midjourney or local image models
- 🌍 Holiday-aware content planning
- 📊 Frontend dashboard (optional)

---

