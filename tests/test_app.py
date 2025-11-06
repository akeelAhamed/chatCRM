import subprocess

def test_cli_runs():
    # Simulate running the CLI with sample input
    result = subprocess.run(
        ['python', 'src/app.py'],  # Adjust path if you have subfolder
        input='I want to retire in 15 years and prefer email communication.\n',
        text=True,
        capture_output=True
    )
    assert result.returncode == 0
    assert 'Extracted Client Profile' in result.stdout