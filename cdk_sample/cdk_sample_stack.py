from aws_cdk import Stack
from constructs import Construct
from .cdk_aurora import CdkAurora
from .cdk_sqs import CdkSqs


class CdkSampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aurora = CdkAurora()
        aurora.CreateAuroraInstanceWithTag(self)

        sqs = CdkSqs()
        sqs.CreateSQSPolicyFromJson(self)
