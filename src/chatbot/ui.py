import gradio as gr
from dotenv import load_dotenv
import instructor
from openai import OpenAI
from models import ClientProfile
from prompt_engine import load_prompts

# Load environment variables
load_dotenv()

# Patch OpenAI client with Instructor for structured output
client = instructor.patch(OpenAI())

# Load system prompt from YAML
prompts = load_prompts("config/prompts.yaml")
system_prompt = prompts["system_prompt"]

def process_input(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        response_model=ClientProfile
    )
    return response.json(indent=2)

# Launch Gradio interface
iface = gr.Interface(fn=process_input, inputs="text", outputs="text", title="FinWise CRM Chatbot")
iface.launch()