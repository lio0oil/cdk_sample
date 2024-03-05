import json  # noqa: F401

from aws_cdk import aws_iam as iam
from aws_cdk import aws_sqs as sqs_
from constructs import Construct


class CdkSqsInvalidPolicy:
    def Create(self, scope: Construct):
        role1 = iam.Role.from_role_name(scope, "role1", "service-role/versioncheck-role-a1hjb6bh")
        role2 = iam.Role.from_role_name(scope, "role2", "role2")

        sqs = sqs_.Queue(scope, "sqs")
        exists_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["SQS:*"],
            principals=[iam.ArnPrincipal(role1.role_arn)],  # type: ignore
            resources=[sqs.queue_arn],
        )
        sqs.add_to_resource_policy(exists_policy)

        # "Invalid value for the parameter Policy" error occurs when deploying.
        # not_exists_policy = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=["SQS:*"],
        #     principals=[iam.ArnPrincipal(role2.role_arn)],  # type: ignore
        #     resources=[sqs.queue_arn],
        # )
        # sqs.add_to_resource_policy(not_exists_policy)
