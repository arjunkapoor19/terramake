import json
from src.generator.main_generator import generate_all


def main():
    with open("data/sample_input.json") as f:
        config = json.load(f)

    tf_code = generate_all(config)

    # print to terminal
    print(tf_code)

    # save to file
    with open("output.tf", "w") as f:
        f.write(tf_code)


if __name__ == "__main__":
    main()