#!/usr/bin/env python3

import os

import aws_cdk as cdk

from cdk_sample.stack.change_calender_stack import ChangeCalenderStack

app = cdk.App()
env = cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
ChangeCalenderStack(app, "ChangeCalenderStack", env=env)

app.synth()
