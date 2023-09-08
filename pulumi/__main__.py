"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
#bucket = s3.Bucket('my-bucket')

buckets = ["bucket1","bucket2","bucket3"]

for x in buckets:
    new_buckets = s3.Bucket(x)

# Export the name of the bucket
pulumi.export('bucket_name', new_buckets.id)
