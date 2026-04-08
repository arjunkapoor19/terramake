import json
from src.generator.main_generator import generate_all
from src.ai.validator import validate_terraform


def main():
    with open("data/sample_input.json") as f:
        config = json.load(f)

    tf_code = generate_all(config)

    print("=== GENERATED TERRAFORM ===")
    print(tf_code)

    print("\n=== AI VALIDATION ===")
    feedback = validate_terraform(tf_code)
    print(feedback)


if __name__ == "__main__":
    main()