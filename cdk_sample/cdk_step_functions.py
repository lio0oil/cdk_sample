from constructs import Construct
from aws_cdk import aws_stepfunctions as sfn  # noqa: F401
from aws_cdk import aws_lambda as lambda_
from aws_cdk import ScopedAws
from pathlib import Path


class CdkStepFunctions:
    def CreateStepFunctionsFromASL(self, scope: Construct):
        fn: lambda_.IFunction = lambda_.Function(
            scope,
            "MyFunction",
            runtime=lambda_.Runtime.NODEJS_18_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("foo"),
        )

        sa: ScopedAws = ScopedAws(scope)

        file = self._get_filepath() / "asl/MyStateMachine.asl.json"

        # if replace of accountid is unnecessary, DefinitionBody.fromFile is use
        # state: sfn.IStateMachine = sfn.StateMachine(
        #     scope,
        #     "StateMachine",
        #     definition_body=sfn.DefinitionBody.from_file(str(file)),
        # )

        with open(file) as f:
            data = f.read()

        data = data.replace("${AWS::Region}", sa.region)
        data = data.replace("${AWS::AccountId}", sa.account_id)

        state: sfn.IStateMachine = sfn.StateMachine(
            scope,
            "StateMachine",
            definition_body=sfn.DefinitionBody.from_string(data),
        )

        fn.grant_invoke(state)

    def _get_filepath(self) -> Path:
        return Path(__file__).parent
