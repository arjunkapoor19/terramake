def generate_s3_tf(config):
    s3 = config.get("s3")

    if not s3:
        return ""

    bucket_name = s3.get("bucket_name")
    public = s3.get("public", False)
    versioning = s3.get("versioning", False)

    if not bucket_name:
        raise ValueError("bucket_name is required for S3")

    resource_name = bucket_name.replace("-", "_")

    tf = []

    # S3 Bucket
    tf.append(f'resource "aws_s3_bucket" "{resource_name}" {{')
    tf.append(f'  bucket = "{bucket_name}"')
    tf.append("}")
    tf.append("")
    
    # Public Access Block (if not public)
    if not public:
        tf.append(f'resource "aws_s3_bucket_public_access_block" "{resource_name}_public_access" {{')
        tf.append(f'  bucket = aws_s3_bucket.{resource_name}.id')
        tf.append("")
        tf.append("  block_public_acls   = true")
        tf.append("  block_public_policy = true")
        tf.append("  ignore_public_acls  = true")
        tf.append("  restrict_public_buckets = true")
        tf.append("}")
        tf.append("")
        
    # Versioning
    if versioning:
        tf.append(f'resource "aws_s3_bucket_versioning" "{resource_name}_versioning" {{')
        tf.append(f'  bucket = aws_s3_bucket.{resource_name}.id')
        tf.append("")
        tf.append("  versioning_configuration {")
        tf.append('    status = "Enabled"')
        tf.append("  }")
        tf.append("}")
        tf.append("")

    return "\n".join(tf)