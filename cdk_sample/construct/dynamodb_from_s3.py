from aws_cdk import RemovalPolicy
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_s3 as s3
from constructs import Construct


class DynamoDBfromS3(Construct):
    @property
    def table(self) -> dynamodb.ITable:
        return self._table

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(
            self,
            "DynamoDB-Import-Bucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Addressed in v2.123.0
        # no test
        ddbimport = dynamodb.ImportSourceSpecification(
            bucket=bucket,
            input_format=dynamodb.InputFormat.dynamo_db_json(),
            compression_type=dynamodb.InputCompressionType.GZIP,
            key_prefix="AWSDynamoDB/01690802496650-54db8cc3/data/",
        )

        table: dynamodb.Table = dynamodb.Table(  # noqa: F841
            scope,
            "DynamoDB",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            sort_key=dynamodb.Attribute(name="date", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            import_source=ddbimport,
        )

        # deleted for testing
        table.apply_removal_policy(RemovalPolicy.DESTROY)

        self._table = table

        # # s3 import is not in l2 so l1
        # cfn_table: dynamodb.CfnTable = table.node.default_child  # type: ignore  # noqa: F841

        # # Assuming the case of exporting by default from the management console.
        # # Exporting from the management console results in GZIP compression.
        # # s3_bucket specifies the bucket name.
        # # s3_key_prefix specifies the data folder where the GZIP file is located
        # import_source = dynamodb.CfnTable.ImportSourceSpecificationProperty(
        #     input_compression_type="GZIP",  # GZIP,NONE,ZSTD
        #     input_format="DYNAMODB_JSON",
        #     s3_bucket_source=dynamodb.CfnTable.S3BucketSourceProperty(
        #         s3_bucket="dynamodb-export-to-s3-import",
        #         s3_key_prefix="AWSDynamoDB/01690802496650-54db8cc3/data/",
        #     ),
        # )
        # cfn_table.import_source_specification = import_source
