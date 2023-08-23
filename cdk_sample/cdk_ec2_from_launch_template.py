from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct


class CdkEc2:
    def CreateEc2FromLaunchTemplate(self, scope: Construct):
        ec2.Vpc.from_lookup(scope, "vpc-08f972a0d99b8ef35", vpc_id="vpc-08f972a0d99b8ef35")
        launch_template: ec2.LaunchTemplate = ec2.LaunchTemplate(
            scope,
            "LaunchTemplate",
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
                cpu_type=ec2.AmazonLinuxCpuType.X86_64,
            ),
            security_group=ec2.SecurityGroup.from_lookup_by_id(scope, "sg-0254554c0c4cf7f7b", "sg-0254554c0c4cf7f7b"),
            key_name="customamitest",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.SMALL),
            role=iam.Role.from_role_name(scope, "role", "service-role/aaa-role-6qk4d4wk"),
        )
        launch_template.add_security_group(
            ec2.SecurityGroup.from_lookup_by_id(scope, "sg-04136651926cb1b73", "sg-04136651926cb1b73"),
        )

        # Don't use L2 + L1 because instance_type and machine_image are required.
        # vpc_subnets = ec2.SubnetSelection(
        #     subnets=[
        #         ec2.Subnet.from_subnet_id(scope, "subnet-092d75a6a1c482cc5", "subnet-092d75a6a1c482cc5"),
        #         ec2.Subnet.from_subnet_id(scope, "subnet-03f70850fa309416b", "subnet-03f70850fa309416b"),
        #     ]
        # )
        # vpc_subnets = ec2.SubnetSelection(
        #     subnets=[
        #         ec2.Subnet.from_subnet_attributes(
        #             scope, "subnet-092d75a6a1c482cc5", subnet_id="subnet-092d75a6a1c482cc5", availability_zone="ap-northeast-1a"
        #         ),
        #         ec2.Subnet.from_subnet_attributes(
        #             scope, "subnet-03f70850fa309416b", subnet_id="subnet-03f70850fa309416b", availability_zone="ap-northeast-1c"
        #         ),
        #     ]
        # )
        # ec2_ = ec2.Instance(
        #     scope,
        #     "ec2",
        #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.SMALL),
        #     machine_image=ec2.AmazonLinuxImage(
        #         generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023,
        #         cpu_type=ec2.AmazonLinuxCpuType.X86_64,
        #     ),
        #     vpc=vpc,
        #     vpc_subnets=vpc_subnets,
        # )  # type: ignore
        # ec2_.instance.launch_template = ec2.CfnInstance.LaunchTemplateSpecificationProperty(
        #     version=launch_template.latest_version_number,
        #     launch_template_id=launch_template.launch_template_id,
        # )

        ec2.CfnInstance(
            scope,
            "ec2",
            launch_template=ec2.CfnInstance.LaunchTemplateSpecificationProperty(
                version=launch_template.latest_version_number,
                launch_template_id=launch_template.launch_template_id,
            ),
            subnet_id="subnet-03f70850fa309416b",
        )
