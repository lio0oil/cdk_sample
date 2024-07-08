from aws_cdk import Stack
from constructs import Construct

from cdk_sample.construct.sqs_policy_from_json import SQSPolicyFromJson


class SQSPolicyFromJsonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SQSPolicyFromJson(self, "Sample")
