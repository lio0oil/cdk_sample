from aws_cdk import aws_rds as rds, aws_ec2 as ec2, Tags, Resource
from constructs import Construct


class CdkAurora:
    def CreateAuroraInstanceWithTag(self, scope: Construct):
        # Aurora instance with tag

        vpc = ec2.Vpc(scope, "vpc")

        writer = rds.ClusterInstance.provisioned(
            "writer",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MEDIUM),
            # instance_identifier="writer_identifire",
        )
        reader = rds.ClusterInstance.provisioned(
            "reader",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MEDIUM),
            # instance_identifier="reader_identifire",
        )

        parameter_group = rds.ParameterGroup(
            scope, "pg", engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_12_12)
        )
        Tags.of(parameter_group).add("b", "2")

        aurora: rds.DatabaseCluster = rds.DatabaseCluster(
            scope,
            "Database",
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_12_12),
            writer=writer,
            readers=[reader],
            vpc=vpc,
            parameter_group=parameter_group,
        )
        Tags.of(aurora).add("a", "1")
        print(aurora)

        print(aurora.node.children[4])

        # warning log is output
        # for construct in aurora.node.children:
        #     if isinstance(construct, Resource):
        #         for resource in construct.node.children:
        #             if isinstance(resource, rds.CfnDBInstance):
        #                 Tags.of(resource).add("c", "1")

        for construct in aurora.node.children:
            if type(construct) == Resource:
                instance = construct.node.default_child
                Tags.of(instance).add("c", "1")
