from pathlib import Path

from aws_cdk import Aws
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_stepfunctions as sfn
from constructs import Construct


class StepFunctionsFromASL(Construct):
    @property
    def state_machine(self) -> sfn.IStateMachine:
        return self._state_machine

    @property
    def function(self) -> lambda_.IFunction:
        return self._function  # type: ignore

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        fn: lambda_.Function = lambda_.Function(
            self,
            "MyFunction",
            runtime=lambda_.Runtime.NODEJS_18_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("foo"),
        )

        file = self._get_filepath().parent / "asl/MyStateMachine.asl.json"

        # if replace of accountid is unnecessary, DefinitionBody.fromFile is use
        # state: sfn.IStateMachine = sfn.StateMachine(
        #     self,
        #     "StateMachine",
        #     definition_body=sfn.DefinitionBody.from_file(str(file)),
        # )

        with open(file) as f:
            data = f.read()

        # Use CloudFormation pseudo parameters to replace
        data = data.replace("${AWS::Region}", Aws.REGION)
        data = data.replace("${AWS::AccountId}", Aws.ACCOUNT_ID)

        state: sfn.StateMachine = sfn.StateMachine(
            self,
            "StateMachine",
            definition_body=sfn.DefinitionBody.from_string(data),
        )

        fn.grant_invoke(state)

        self._function = fn
        self._state_machine = state

    def _get_filepath(self) -> Path:
        return Path(__file__).parent
