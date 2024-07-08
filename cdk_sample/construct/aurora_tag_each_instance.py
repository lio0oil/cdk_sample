from aws_cdk import Resource, Tags
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from constructs import Construct


class AuroraTagEachInstance(Construct):
    @property
    def db(self) -> rds.IDatabaseCluster:
        return self._db

    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        writer = rds.ClusterInstance.provisioned(
            "Writer",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
        )
        reader = rds.ClusterInstance.provisioned(
            "Reader",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
        )
        # ClusterInstance is not extended IConstruct, so tags cannot be added.
        # Tags.of(writer).add("Writer", "value")
        # Tags.of(reader).add("Reader", "value")

        parameter_group = rds.ParameterGroup(
            self, "Mypg", engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_12_12)
        )
        Tags.of(parameter_group).add("ParameterGroupKey", "ParameterGroupValue")

        aurora = rds.DatabaseCluster(
            self,
            "MyDatabase",
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_12_12),
            writer=writer,
            readers=[reader],
            vpc=vpc,
            parameter_group=parameter_group,
        )
        # This tag is assigned to each instance in addition to the cluster.
        Tags.of(aurora).add("DatabaseClusterKey", "DatabaseClusterValue")

        # Use L1 constructors to assign tags to each instance.
        for construct in aurora.node.children:
            if type(construct) == Resource:
                instance = construct.node.default_child
                Tags.of(instance).add("ClusterInstanceKey", "ClusterInstanceValue")

        self._db = aurora
