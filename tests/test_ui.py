from ui import process_input
import json

def test_ui_process_input():
    output = process_input("I want to retire in 15 years and prefer email communication.")
    data = json.loads(output)
    assert isinstance(data, dict)
    assert "financial_goals" in data
