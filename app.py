#!/usr/bin/env python3

import os

import aws_cdk as cdk

from cdk_sample.stack.aurora_tag_each_instance_stack import AuroraTagEachInstanceStack
from cdk_sample.stack.change_calender_stack import ChangeCalenderStack
from cdk_sample.stack.dynamodb_from_s3_stack import DynamoDBfromS3Stack
from cdk_sample.stack.sqs_policy_from_json_stack import SQSPolicyFromJsonStack
from cdk_sample.stack.step_functions_from_asl_stack import StepFunctionsFromASLStack

app = cdk.App()
env = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
ChangeCalenderStack(app, "ChangeCalenderStack", env=env)
StepFunctionsFromASLStack(app, "StepFunctionsFromASLStack", env=env)
SQSPolicyFromJsonStack(app, "SQSQueuePolicyFromJsonStack", env=env)
AuroraTagEachInstanceStack(app, "AuroraTagEachInstanceStack", env=env)
DynamoDBfromS3Stack(app, "DynamoDBfromS3", env=env)

app.synth()
