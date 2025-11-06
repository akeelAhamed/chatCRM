# **FinWise CRM Chatbot**

## **Overview**
FinWise CRM Chatbot is a Generative AI-powered assistant designed to streamline client onboarding for FinWise, a financial advisory firm. The chatbot interacts with clients to collect essential onboarding information, validates the data, and returns a structured JSON output ready for CRM integration.

---

## **Features**
- Conversational AI for client onboarding
- Structured JSON output for CRM integration
- Prompt engineering with YAML-based templates
- Portkey API integration for reliable model access
- Validation using Pydantic and Instructor
- Dual interface: CLI and Gradio UI
- Environment configuration via `.env`

---

## **Architecture**
```
├── .env                  # Environment variables
├── .gitignore            # Ignore unnecessary files
├── README.md             # Documentation
├── config/
│   ├── params.yaml       # Model parameters
│   └── prompts.yaml      # Prompt templates
├── pyproject.toml        # Dependencies
├── src/
│   └── chatbot/
│       ├── __init__.py
│       ├── app.py        # CLI implementation
│       ├── ui.py         # Gradio UI
│       ├── models.py     # Pydantic models
│       ├── portkey_client.py # Portkey API integration
│       └── prompt_engine.py  # Prompt loader
└── tests/
    ├── test_app.py       # CLI tests
    └── test_ui.py        # UI tests
```

---

## **Setup**
1. Install **uv**:
   ```bash
   pip install uv
   ```
2. Install dependencies:
   ```bash
   uv install
   ```
3. Add your **Portkey API key** in `.env`:
   ```
   PORTKEY_API_KEY=your_portkey_api_key_here
   ```

---

## **CLI Usage**
Run:
```bash
python src/chatbot/app.py
```

---

## **Gradio UI Usage**
Run:
```bash
python src/chatbot/ui.py
```
Access at `http://localhost:7860`.

---

## **Testing**
Run tests:
```bash
pytest tests/
```