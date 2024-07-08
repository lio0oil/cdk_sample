from aws_cdk import Stack
from constructs import Construct

from cdk_sample.construct.dynamodb_from_s3 import DynamoDBfromS3


class DynamoDBfromS3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        DynamoDBfromS3(self, "Sample")
