from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as events_target
import aws_cdk.aws_lambda as lambda_
from aws_cdk import Duration
from constructs import Construct


class CdkEventBridgeRule:
    def CreateEventBridgeRuleInvokeLambdaUseSchedule(self, scope: Construct):
        fn = lambda_.Function(
            scope,
            "MyFunc",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("exports.handler = handler.toString()"),
        )

        target = events_target.LambdaFunction(fn)
        events.Rule(
            scope,
            "ScheduleRule",
            schedule=events.Schedule.rate(Duration.hours(1)),
            targets=[target],
        )
