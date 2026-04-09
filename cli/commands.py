import typer
import json
from rich import print
from src.generator.main_generator import generate_all
from src.ai.validator import review_terraform
from src.ai.validator import suggest_fixes
from src.utils.logger import log_feedback
from src.utils.analyzer import analyze_feedback
from src.utils.analyzer import get_rejected_patterns, extract_patterns

app = typer.Typer()


# 🔹 Helper function (DRY principle)
def load_config(input_file: str):
    try:
        with open(input_file) as f:
            content = f.read().strip()

            if not content:
                print("[red]Input file is empty[/red]")
                print("[yellow]Add valid JSON configuration to the file.[/yellow]")
                raise typer.Exit()

            config = json.loads(content)

    except FileNotFoundError:
        print("[red]File not found[/red]")
        print("[yellow]Make sure the path is correct[/yellow]")
        raise typer.Exit()

    except json.JSONDecodeError:
        print("[red]Invalid JSON format[/red]")
        print("[yellow]Check for syntax errors in your JSON file[/yellow]")
        raise typer.Exit()

    if "s3" not in config and "cloudfront" not in config:
        print("[red]Invalid input: No supported resources found[/red]")
        print("[yellow]Expected keys: 's3' or 'cloudfront', make sure either is present.[/yellow]")
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

    print("\n[bold blue]AI Suggestions[/bold blue]\n")

    suggestions_list = []
    current = []

    for line in suggestions.split("\n"):
        if line.strip().startswith("- Problem"):
            if current:
                suggestions_list.append("\n".join(current))
                current = []
        current.append(line)

    if current:
        suggestions_list.append("\n".join(current))

    # Print with numbering
    for i, s in enumerate(suggestions_list):
        print(f"\n[bold green]Fix #{i}[/bold green]")
        print(s)

@app.command()
def feedback(input_file: str, index: int, action: str):
    """
    Log feedback on a specific suggestion (accept/reject)
    """

    config = load_config(input_file)

    tf_code = generate_all(config)
    suggestions = suggest_fixes(tf_code)

    # Split suggestions
    suggestions_list = []
    current = []

    for line in suggestions.split("\n"):
        if line.strip().startswith("- Problem"):
            if current:
                suggestions_list.append("\n".join(current))
                current = []
        current.append(line)

    if current:
        suggestions_list.append("\n".join(current))

    # Validate index
    if index < 0 or index >= len(suggestions_list):
        print("[red]Invalid suggestion index[/red]")
        raise typer.Exit()
    
    if action not in ["accept", "reject"]:
        print("[red]Action must be 'accept' or 'reject'[/red]")
        raise typer.Exit()

    selected_suggestion = suggestions_list[index]

    # Log only selected suggestion
    log_feedback(config, tf_code, selected_suggestion, action)

    print(f"[green]Feedback '{action}' logged for Fix #{index}[/green]")


@app.command()
def feedback_all(input_file: str, action: str):
    """
    Log feedback for ALL suggestions (accept/reject)
    """

    if action not in ["accept", "reject"]:
        print("[red]❌ Action must be 'accept' or 'reject'[/red]")
        raise typer.Exit()

    config = load_config(input_file)

    tf_code = generate_all(config)
    suggestions = suggest_fixes(tf_code)

    # Split suggestions into list
    suggestions_list = []
    current = []

    for line in suggestions.split("\n"):
        if line.strip().startswith("- Problem"):
            if current:
                suggestions_list.append("\n".join(current))
                current = []
        current.append(line)

    if current:
        suggestions_list.append("\n".join(current))

    # Log each suggestion
    for i, s in enumerate(suggestions_list):
        log_feedback(config, tf_code, s, action)

    print(f"[green]'{action}' logged for ALL ({len(suggestions_list)}) suggestions[/green]")


@app.command()
def stats():
    """
    Show feedback statistics
    """

    stats = analyze_feedback()

    if isinstance(stats, str):
        print(f"[yellow]{stats}[/yellow]")
        return

    print("\n[bold blue]Feedback Stats[/bold blue]\n")

    print(f"[green]Total:[/green] {stats['total']}")
    print(f"[green]Accepted:[/green] {stats['accepted']}")
    print(f"[red]Rejected:[/red] {stats['rejected']}")
    print(f"[bold]Acceptance Rate:[/bold] {stats['acceptance_rate']}%")

@app.command()
def patterns():
    """
    Print learned patterns
    """

    raw = get_rejected_patterns()
    patterns = extract_patterns(raw)

    print("\n[bold blue]Learned Patterns[/bold blue]\n")

    for p in patterns:
        print(f"- {p}")


@app.command()
def demo(input_file: str):
    """
    Run full TerraMake pipeline (generate → review → suggest → stats)
    """

    config = load_config(input_file)
    
    print("\n[bold cyan]TerraMake Demo[/bold cyan]\n")

    # Generate
    print("[bold blue]Generating Terraform...[/bold blue]")
    tf_code = generate_all(config)

    print("\n[green]Terraform Generated[/green]\n")

    # Review
    print("[bold blue]Reviewing Terraform...[/bold blue]\n")
    review_output = review_terraform(tf_code)
    print(review_output)

    # Suggest
    print("\n[bold blue]Suggesting Improvements...[/bold blue]\n")
    suggestions = suggest_fixes(tf_code)
    print(suggestions)

    # Stats
    print("\n[bold blue]Feedback Stats[/bold blue]\n")
    stats = analyze_feedback()

    if isinstance(stats, dict):
        print(f"Total: {stats['total']}")
        print(f"Accepted: {stats['accepted']}")
        print(f"Rejected: {stats['rejected']}")
        print(f"Acceptance Rate: {stats['acceptance_rate']}%")