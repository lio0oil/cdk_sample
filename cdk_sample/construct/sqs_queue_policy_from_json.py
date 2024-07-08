import json  # noqa: F401

from aws_cdk import aws_iam as iam
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class SQSQueuePolicyFromJson(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # SQS Policy from json
        s = sqs.Queue(scope, "SampleSQS")  # noqa: F841

        # CDKから作成
        sqs_policy_state2 = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["SQS:2*"],
            principals=[iam.ArnPrincipal("*")],  # type: ignore
            resources=["arn:aws:sqs:xxx-xxxxx-1:000000000000:dlq"],
        )
        s.add_to_resource_policy(sqs_policy_state2)

        # jsonから作成
        policy1 = """
{
    "Sid": "__owner_statement",
    "Effect": "Allow",
    "Principal": {
    "AWS": "arn:aws:iam::000000000000:root"
    },
    "Action": "SQS:1",
    "Resource": "arn:aws:sqs:xxx-xxxxx-1:000000000000:dlq"
}
"""
        # PolicyStatementなので1ステートメントしか扱えない
        sqs_policy_state1 = iam.PolicyStatement.from_json(json.loads(policy1))
        s.add_to_resource_policy(sqs_policy_state1)

        # 既存のSQSの設定から作成したい場合はStatementでループさせる
        policy3 = """
{
  "Version": "2012-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::000000000000:root"
      },
      "Action": "SQS:3*",
      "Resource": "arn:aws:sqs:xxx-xxxxx-1:000000000000:dlq"
    }
  ]
}"""

        j = json.loads(policy3)

        for stat in j["Statement"]:
            s.add_to_resource_policy(iam.PolicyStatement.from_json(stat))
