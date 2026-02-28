# Prompt to Entity API

FastAPI service that extracts entities and locations from crisis text using Anthropic's Claude, deployed on AWS Lambda.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-191919?style=for-the-badge&logo=anthropic&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)

## About

This service accepts a natural-language description of a crisis scene and returns structured JSON containing the entities present, their spatial positions, approximate scales, and colors. It uses a two-stage prompt pipeline: the first prompt expands the input into a richer scene description, and the second extracts entity data into a consistent JSON schema.

## How It Works

1. A POST request sends a crisis description to the `/get-objects` endpoint.
2. **Stage 1** -- The text is inserted into `prompt_template_1.txt`, which instructs the LLM to elaborate the scene with spatial and descriptive detail.
3. **Stage 2** -- The elaborated text is inserted into `prompt_template_2.txt`, which instructs the LLM to extract entities into structured JSON with position, scale, and color fields.
4. The structured JSON is returned in the response.

## API

### `GET /`

Health check. Returns a welcome message.

### `POST /get-objects`

Extract entities from a crisis description.

**Request body:**

```json
{
  "message": "there are two trees that have fallen in the river and a boat is capsized"
}
```

**Response:**

```json
{
  "response": {
    "assets": [
      {
        "title": "tree1",
        "position": { "x": 1, "y": 3, "z": 0 },
        "scale": { "length": 6, "width": 2, "height": 5 },
        "color": "brown"
      }
    ]
  }
}
```

## Getting Started

### Prerequisites

- Python 3.9+
- An Anthropic API key

### Local Development

```bash
# Clone the repository
git clone <repo-url>
cd prompt_to_entity_api

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set your Anthropic key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Run the server
uvicorn main:app --reload
```

The interactive API docs are available at `http://localhost:8000/docs`.

### Deploying to AWS Lambda

1. Install dependencies into a local directory:

```bash
pip install -t lib -r requirements.txt
```

2. Package the deployment zip:

```bash
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py prompt_template_1.txt prompt_template_2.txt .env
```

3. Upload `lambda_function.zip` to your Lambda function.
4. Set the handler to `main.handler` in the Lambda runtime settings.
5. Under Configuration > Function URL, create a URL with auth type `NONE` and enable CORS.

## License

GPL-3.0. See [LICENSE](LICENSE) for details.
