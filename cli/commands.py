import typer
import json
from src.generator.main_generator import generate_all
from rich import print

app = typer.Typer()


@app.command()
def generate(input_file: str, output: str = "output.tf"):
    """
    Generate Terraform from input JSON
    """
    with open(input_file) as f:
        config = json.load(f)

    tf_code = generate_all(config)

    with open(output, "w") as f:
        f.write(tf_code)

    print("[green]Terraform generated: output.tf[/green]")


@app.command()
def show(input_file: str):
    """
    Show Terraform without saving
    """
    with open(input_file) as f:
        config = json.load(f)

    tf_code = generate_all(config)

    print(tf_code)