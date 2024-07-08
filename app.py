#!/usr/bin/env python3

import os

import aws_cdk as cdk

from cdk_sample.stack.change_calender_stack import ChangeCalenderStack
from cdk_sample.stack.sqs_queue_policy_from_json_stack import (
    SQSQueuePolicyFromJsonStack,
)
from cdk_sample.stack.step_functions_from_asl_stack import StepFunctionsFromASLStack

app = cdk.App()
env = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
ChangeCalenderStack(app, "ChangeCalenderStack", env=env)
StepFunctionsFromASLStack(app, "StepFunctionsFromASLStack", env=env)
SQSQueuePolicyFromJsonStack(app, "SQSQueuePolicyFromJsonStack", env=env)

app.synth()
