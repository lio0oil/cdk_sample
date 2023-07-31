from aws_cdk import aws_dynamodb as dynamodb, RemovalPolicy
from constructs import Construct


class CdkDynamoDB:
    def CreateDynamoDBfromS3(self, scope: Construct):
        table: dynamodb.Table = dynamodb.Table(  # noqa: F841
            scope,
            "DynamoDB",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            sort_key=dynamodb.Attribute(name="date", type=dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1,
        )

        # deleted for testing
        table.apply_removal_policy(RemovalPolicy.DESTROY)

        # auto scale capacity
        table.auto_scale_read_capacity(min_capacity=1, max_capacity=10).scale_on_utilization(target_utilization_percent=75)
        table.auto_scale_write_capacity(min_capacity=1, max_capacity=10).scale_on_utilization(target_utilization_percent=75)

        # s3 import is not in l2 so l1
        cfn_table: dynamodb.CfnTable = table.node.default_child  # type: ignore  # noqa: F841

        # Assuming the case of exporting by default from the management console.
        # Exporting from the management console results in GZIP compression.
        # s3_bucket specifies the bucket name.
        # s3_key_prefix specifies the data folder where the GZIP file is located
        import_source = dynamodb.CfnTable.ImportSourceSpecificationProperty(
            input_compression_type="GZIP",  # GZIP,NONE,ZSTD
            input_format="DYNAMODB_JSON",
            s3_bucket_source=dynamodb.CfnTable.S3BucketSourceProperty(
                s3_bucket="dynamodb-export-to-s3-import",
                s3_key_prefix="AWSDynamoDB/01690802496650-54db8cc3/data/",
            ),
        )
        cfn_table.import_source_specification = import_source
