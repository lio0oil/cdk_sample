from aws_cdk import Stack
from constructs import Construct

from cdk_sample.construct.step_functions_from_asl import StepFunctionsFromASL


class StepFunctionsFromASLStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        StepFunctionsFromASL(self, "Sample")
