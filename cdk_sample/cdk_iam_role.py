from aws_cdk import aws_iam as iam
from constructs import Construct


class CdkIAMRole:
    def CreateIAMRole(self, scope: Construct):
        aws_s3_fullaccess_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")

        statement: iam.PolicyStatement = iam.PolicyStatement(
            # actions=["arn:aws:lambda:::*"],
            # resources=["lambda:InvokeFunction"],
        )
        statement.add_resources("arn:aws:lambda:::*")
        statement.add_actions("lambda:InvokeFunction")

        # want to use inline policy, use iam.Policy
        customer_managed_policy: iam.ManagedPolicy = iam.ManagedPolicy(
            scope,
            "ManagedPolicy_" + "CreateIAMRole",
            # statements=[statement],
        )

        customer_managed_policy.add_statements(statement)

        role: iam.Role = iam.Role(  # noqa: F841
            scope,
            "Role_" + "CreateIAMRole",
            # assumed_by=iam.AnyPrincipal(),
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                aws_s3_fullaccess_policy,
                customer_managed_policy,
            ],
        )
