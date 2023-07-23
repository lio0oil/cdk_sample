from aws_cdk import aws_scheduler as sch
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct
from aws_cdk import ScopedAws


class CdkEventBridgeSchedule:
    def CreateEventBridgeScheduleInvokeLambda(self, scope: Construct):
        # no official hand-written (L2) constructs

        # every 30 minutes

        fn: lambda_.Function = lambda_.Function(
            scope,
            "Func_" + "CreateEventBridgeScheduleInvokeLambda",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("exports.handler = handler.toString()"),
        )

        sa: ScopedAws = ScopedAws(scope)

        policy: iam.ManagedPolicy = iam.ManagedPolicy(
            scope,
            "Policy",
            managed_policy_name="Amazon-EventBridge-Scheduler-Execution-Policy",
            statements=[
                iam.PolicyStatement(
                    actions=["lambda:InvokeFunction"],
                    resources=[
                        fn.function_arn + ":*",
                        fn.function_arn,
                    ],
                )
            ],
        )

        principal: iam.ServicePrincipal = iam.ServicePrincipal("scheduler.amazonaws.com")
        principal_with_conditions = iam.PrincipalWithConditions(
            principal,
            {"StringEquals": {"aws:SourceAccount": sa.account_id}},
        )

        role: iam.Role = iam.Role(
            scope,
            "EventBridgeRole",
            role_name="Amazon_EventBridge_Scheduler_LAMBDA",
            assumed_by=principal_with_conditions,
        )
        role.add_managed_policy(policy)

        target = sch.CfnSchedule.TargetProperty(
            arn=fn.function_arn,
            role_arn=role.role_arn,
        )

        flexible_time_window_property = sch.CfnSchedule.FlexibleTimeWindowProperty(mode="OFF")

        sch.CfnSchedule(
            scope,
            "EventBridgeSchedule",
            flexible_time_window=flexible_time_window_property,
            schedule_expression="rate(30 minutes)",
            target=target,
        )
