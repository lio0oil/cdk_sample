from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class CdkConvStrToInstanceClass:
    def CreateEc2(self, scope: Construct):
        vpc = ec2.Vpc(scope, "vpc")

        # ec2.Instance(scope, "EC2", instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO))

        instance_class = "T3"
        instance_size = "MICRO"
        ec2.Instance(
            scope,
            "EC2",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass[instance_class], ec2.InstanceSize[instance_size]),
            vpc=vpc,
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023),
        )
