from aws_cdk import Stack
from constructs import Construct
from .cdk_aurora import CdkAurora  # noqa: F401
from .cdk_sqs import CdkSqs  # noqa: F401
from .cdk_event_bridge_schedule import CdkEventBridgeSchedule  # noqa: F401
from .cdk_event_bridge_rule import CdkEventBridgeRule  # noqa: F401
from .cdk_step_functions import CdkStepFunctions  # noqa: F401


class CdkSampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aurora = CdkAurora()
        aurora.CreateAuroraInstanceWithTag(self)

        sqs = CdkSqs()
        sqs.CreateSQSPolicyFromJson(self)

        ebsche = CdkEventBridgeSchedule()
        ebsche.CreateEventBridgeScheduleInvokeLambda(self)

        ebrule = CdkEventBridgeRule()
        ebrule.CreateEventBridgeRuleInvokeLambdaUseSchedule(self)

        sfn = CdkStepFunctions()
        sfn.CreateStepFunctionsFromASL(self)
