import typer
import json
from rich import print
from src.generator.main_generator import generate_all
from src.ai.validator import review_terraform
from src.ai.validator import suggest_fixes

app = typer.Typer()


# 🔹 Helper function (DRY principle)
def load_config(input_file: str):
    try:
        with open(input_file) as f:
            config = json.load(f)
    except FileNotFoundError:
        print("[red]File not found[/red]")
        raise typer.Exit()

    if "s3" not in config and "cloudfront" not in config:
        print("[red]Invalid input: No supported resources found[/red]")
        raise typer.Exit()

    return config


@app.command()
def generate(input_file: str, output: str = "output.tf", verbose: bool = False):
    """
    Generate Terraform from input JSON
    """

    config = load_config(input_file)

    tf_code = generate_all(config)

    with open(f"outputs/{output}", "w") as f:
        f.write(tf_code)

    if verbose:
        print("\n[bold blue]Generated Terraform:[/bold blue]\n")
        print(tf_code)

    print(f"[green]Terraform generated: outputs/{output}[/green]")


@app.command()
def show(input_file: str):
    """
    Show Terraform without saving
    """

    config = load_config(input_file)

    tf_code = generate_all(config)

    print("\n[bold blue]Terraform Output[/bold blue]\n")
    print(tf_code)


@app.command()
def review(input_file: str):
    """
    Validate Terraform using AI
    """

    config = load_config(input_file)

    print("[bold blue]Generating Terraform...[/bold blue]\n")
    tf_code = generate_all(config)
    print(tf_code)

    print("\n[bold blue]=========== AI Review ===========[/bold blue]\n")
    feedback = review_terraform(tf_code)

    # Pretty formatting
    for line in feedback.split("\n"):
        if "[SECURITY]" in line:
            print("[bold red]SECURITY[/bold red]")
        elif "[BEST_PRACTICES]" in line:
            print("\n[bold yellow]BEST PRACTICES[/bold yellow]")
        elif "[MISSING]" in line:
            print("\n[bold magenta]MISSING[/bold magenta]")
        elif line.strip().startswith("-"):
            print(f"[white]{line}[/white]")

@app.command()
def suggest(input_file: str):
    """
    Suggest fixes for Terraform using AI
    """

    config = load_config(input_file)

    print("\n[bold blue]Generating Terraform...[/bold blue]")
    tf_code = generate_all(config)

    print("\n[bold blue]AI Suggestions[/bold blue]\n")

    suggestions = suggest_fixes(tf_code)

    for line in suggestions.split("\n"):
        if "[FIXES]" in line:
            print("[bold green]FIXES[/bold green]")
        elif line.strip().startswith("- Problem"):
            print(f"\n[bold yellow]{line}[/bold yellow]")
        elif "Fix:" in line:
            print("[bold cyan]Fix:[/bold cyan]")
        else:
            print(f"[white]{line}[/white]")