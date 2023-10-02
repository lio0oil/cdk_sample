from aws_cdk import Stack
from constructs import Construct
from .cdk_aurora import CdkAurora  # noqa: F401
from .cdk_sqs import CdkSqs  # noqa: F401
from .cdk_event_bridge_schedule import CdkEventBridgeSchedule  # noqa: F401
from .cdk_event_bridge_rule import CdkEventBridgeRule  # noqa: F401
from .cdk_step_functions import CdkStepFunctions  # noqa: F401
from .cdk_auto_scaling import CdkAutoScaling  # noqa: F401
from .cdk_iam_role import CdkIAMRole  # noqa: F401
from .cdk_conv_str_to_instance_class import CdkConvStrToInstanceClass  # noqa: F401
from .cdk_security_group import CdkSecurityGroup  # noqa: F401
from .cdk_dynamo_db import CdkDynamoDB  # noqa: F401
from .cdk_ec2_from_launch_template import CdkEc2  # noqa: F401
from .cdk_document import CdkDocument  # noqa: F401


class CdkSampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # aurora = CdkAurora()
        # aurora.CreateAuroraInstanceWithTag(self)

        # sqs = CdkSqs()
        # sqs.CreateSQSPolicyFromJson(self)

        # ebsche = CdkEventBridgeSchedule()
        # ebsche.CreateEventBridgeScheduleInvokeLambda(self)

        # ebrule = CdkEventBridgeRule()
        # ebrule.CreateEventBridgeRuleInvokeLambdaUseSchedule(self)

        # sfn = CdkStepFunctions()
        # sfn.CreateStepFunctionsFromASL(self)

        # asc = CdkAutoScaling()
        # asc.CreateAutoScaling(self)

        # role = CdkIAMRole()
        # role.CreateIAMRole(self)

        # csi = CdkConvStrToInstanceClass()
        # csi.CreateEc2(self)

        # sg = CdkSecurityGroup()
        # sg.CreateSecurityGgroup(self)

        # ddb = CdkDynamoDB()
        # ddb.CreateDynamoDBfromS3(self)

        # ec2 = CdkEc2()
        # ec2.CreateEc2FromLaunchTemplate(self)

        doc = CdkDocument()
        doc.CreateChangeCalendar(self)
