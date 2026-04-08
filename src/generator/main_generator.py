from src.generator.s3 import generate_s3_tf
from src.generator.cloudfront import generate_cloudfront_tf


def generate_all(config):
    tf_parts = []

    # S3
    s3_tf = generate_s3_tf(config)
    if s3_tf:
        tf_parts.append(s3_tf)

    # CloudFront
    cf_tf = generate_cloudfront_tf(config)
    if cf_tf:
        tf_parts.append(cf_tf)

    return "\n\n".join(tf_parts)