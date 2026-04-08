import json
from src.generator.cloudfront import generate_cloudfront_tf

def main():
    with open("data/sample_input.json") as f:
        config = json.load(f)

    tf_code = generate_cloudfront_tf(config)
    print(tf_code)

if __name__ == "__main__":
    main()