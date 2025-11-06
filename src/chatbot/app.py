import click
from rich.console import Console
from rich.prompt import Prompt
from .portkey_client import get_response
from .models import ClientProfile

console = Console()

@click.command()
def run_chatbot():
    console.print('[bold green]Welcome to FinWise CRM Chatbot[/bold green]')
    user_input = Prompt.ask('Please describe your financial goals and preferences')
    response = get_response(user_input)
    console.print('[bold blue]Extracted Profile:[/bold blue]')
    console.print(response)

if __name__ == '__main__':
    run_chatbot()
