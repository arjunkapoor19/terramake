import json
from src.generator.s3 import generate_s3_tf

def main():
    with open("data/sample_input.json") as f:
        config = json.load(f)

    tf_code = generate_s3_tf(config)
    print(tf_code)

if __name__ == "__main__":
    main()