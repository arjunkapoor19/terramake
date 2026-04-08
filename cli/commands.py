import typer
import json
from src.generator.main_generator import generate_all
from rich import print

app = typer.Typer()


@app.command()
def generate(input_file: str, output: str = "output.tf", verbose: bool = False):
    """
    Generate Terraform from input JSON
    """
    
    # Basic file not found check
    try:
        with open(input_file) as f:
            config = json.load(f)
    except FileNotFoundError:
        print("[red] File not found[/red]")
        raise typer.Exit()
    
    
    # Basic structure check of source file
    if "s3" not in config and "cloudfront" not in config:
        print("[red]Invalid input: No supported resources found[/red]")
        raise typer.Exit()

    tf_code = generate_all(config)
    
    with open("outputs/"+output, "w") as f:
        f.write(tf_code)

    # Show command integrated with generate
    if (verbose):
        print(tf_code)

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