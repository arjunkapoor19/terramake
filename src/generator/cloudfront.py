def generate_cloudfront_tf(config):
    cf = config.get("cloudfront")

    if not cf:
        return ""

    enabled = cf.get("enabled", True)
    origin_bucket = cf.get("origin")

    # validation
    if not origin_bucket:
        raise ValueError("CloudFront requires an origin bucket")

    resource_name = "cdn"
    origin_id = f"{origin_bucket}-origin"
    domain_name = f"{origin_bucket}.s3.amazonaws.com"

    tf = []

    tf.append(f'resource "aws_cloudfront_distribution" "{resource_name}" {{')
    tf.append(f'  enabled = {str(enabled).lower()}')
    tf.append("")

    # 🔹 Origin block
    tf.append("  origin {")
    tf.append(f'    domain_name = "{domain_name}"')
    tf.append(f'    origin_id   = "{origin_id}"')
    tf.append("  }")
    tf.append("")

    # 🔹 Default cache behavior
    tf.append("  default_cache_behavior {")
    tf.append(f'    target_origin_id       = "{origin_id}"')
    tf.append('    viewer_protocol_policy = "redirect-to-https"')
    tf.append("")
    tf.append('    allowed_methods = ["GET", "HEAD"]')
    tf.append('    cached_methods  = ["GET", "HEAD"]')
    tf.append("")
    tf.append("    forwarded_values {")
    tf.append("      query_string = false")
    tf.append("")
    tf.append("      cookies {")
    tf.append('        forward = "none"')
    tf.append("      }")
    tf.append("    }")
    tf.append("  }")
    tf.append("")

    # 🔽 Restrictions block
    tf.append("  restrictions {")
    tf.append("    geo_restriction {")
    tf.append('      restriction_type = "none"')
    tf.append("    }")
    tf.append("  }")
    tf.append("")

    # 🔹 Viewer certificate
    tf.append("  viewer_certificate {")
    tf.append("    cloudfront_default_certificate = true")
    tf.append("  }")

    tf.append("}")
    tf.append("")

    return "\n".join(tf)