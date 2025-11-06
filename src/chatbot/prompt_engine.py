import yaml

def load_prompts(path: str):
    with open(path, 'r') as file:
        return yaml.safe_load(file)
