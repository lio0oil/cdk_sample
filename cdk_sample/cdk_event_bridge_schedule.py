from aws_cdk import aws_scheduler as sch
from aws_cdk import aws_iam as iam
from constructs import Construct
from aws_cdk import ScopedAws


class CdkEventBridgeSchedule:
    def CreateEventBridgeScheduleInvokeLambda(self, scope: Construct):
        # no official hand-written (L2) constructs

        # every 30 minutes
        sa: ScopedAws = ScopedAws(scope)

        policy: iam.Policy = iam.Policy(
            scope,
            "Policy",
            policy_name="Amazon-EventBridge-Scheduler-Execution-Policy",
            statements=[
                iam.PolicyStatement(
                    actions=["lambda:InvokeFunction"],
                    resources=[
                        # Get arn if lambda is also at the same time
                        "arn:aws:lambda:" + sa.region + ":" + sa.account_id + ":function:EventBridgeInvoke:*",
                        "arn:aws:lambda:" + sa.region + ":" + sa.account_id + ":function:EventBridgeInvoke",
                    ],
                )
            ],
        )

        principal: iam.ServicePrincipal = iam.ServicePrincipal("lambda.amazonaws.com")
        principal_with_conditions = iam.PrincipalWithConditions(
            principal,
            {"StringEquals": {"aws:SourceAccount": sa.account_id}},
        )

        role: iam.Role = iam.Role(
            scope,
            "Role",
            role_name="Amazon_EventBridge_Scheduler_LAMBDA",
            assumed_by=principal_with_conditions,
        )
        role.attach_inline_policy(policy)

        target = sch.CfnSchedule.TargetProperty(
            arn="arn:aws::" + sa.region + ":" + sa.account_id + ":function:EventBridgeInvoke",
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
