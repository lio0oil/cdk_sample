from aws_cdk import Stack
from constructs import Construct

from cdk_sample.construct.sqs_queue_policy_from_json import (
    SQSQueuePolicyFromJson,
)


class SQSQueuePolicyFromJsonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SQSQueuePolicyFromJson(self, "Sample")
