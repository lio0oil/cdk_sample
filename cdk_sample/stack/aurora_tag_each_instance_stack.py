from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from cdk_sample.construct.aurora_tag_each_instance import AuroraTagEachInstance


class AuroraTagEachInstanceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MyVpc", create_internet_gateway=False)

        AuroraTagEachInstance(self, "Sample", vpc)
