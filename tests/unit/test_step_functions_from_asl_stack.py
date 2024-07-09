import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk_sample.stack.step_functions_from_asl_stack import StepFunctionsFromASLStack


def test_snapshot(snapshot):
    app = cdk.App()
    stack = StepFunctionsFromASLStack(app, "StepFunctionsFromASL")
    template = Template.from_stack(stack)
    assert template.to_json() == snapshot
