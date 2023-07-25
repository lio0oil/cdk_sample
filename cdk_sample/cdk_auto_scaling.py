from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_sqs as sqs_  # noqa: F401
from aws_cdk import aws_cloudwatch as cloudwatch  # noqa: F401
from constructs import Construct
from aws_cdk import Duration


class CdkAutoScaling:
    def CreateAutoScaling(self, scope: Construct):
        vpc = ec2.Vpc.from_lookup(scope, "vpc-08f972a0d99b8ef35", vpc_id="vpc-08f972a0d99b8ef35")
        launch_template: ec2.LaunchTemplate = ec2.LaunchTemplate(
            scope,
            "LaunchTemplate",
            # machine_image=ec2.MachineImage.lookup(name="cdk_ami"),
            machine_image=ec2.WindowsImage(ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_CORE_BASE),
            security_group=ec2.SecurityGroup.from_lookup_by_id(scope, "sg-0254554c0c4cf7f7b", "sg-0254554c0c4cf7f7b"),
            key_name="customamitest",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
        )
        launch_template.add_security_group(
            ec2.SecurityGroup.from_lookup_by_id(scope, "sg-04136651926cb1b73", "sg-04136651926cb1b73"),
        )

        cfn_launch_template: ec2.CfnLaunchTemplate = launch_template.node.default_child  # type: ignore
        # cfn_launch_template.ElasticGpuSpecificationProperty(type="eg1.medium")
        cfn_launch_template.add_override(
            "Properties.LaunchTemplateData.ElasticGpuSpecifications",
            [{"Type": "eg1.medium"}],
        )

        vpc_subnets = ec2.SubnetSelection(
            subnets=[
                ec2.Subnet.from_subnet_id(scope, "subnet-092d75a6a1c482cc5", "subnet-092d75a6a1c482cc5"),
                ec2.Subnet.from_subnet_id(scope, "subnet-03f70850fa309416b", "subnet-03f70850fa309416b"),
            ]
        )

        auto_scaling_group = autoscaling.AutoScalingGroup(
            scope,
            "ASG",
            vpc=vpc,
            launch_template=launch_template,
            vpc_subnets=vpc_subnets,
            desired_capacity=0,
            max_capacity=1,
            min_capacity=0,
        )

        sqs = sqs_.Queue.from_queue_arn(scope, "dlq", "arn:aws:sqs:xxx-xxxxx-1:000000000000:dlq")
        # single metric
        # metric = sqs.metric("ApproximateNumberOfMessagesVisible")

        metric = cloudwatch.MathExpression(
            expression="visible+notvisible",
            using_metrics={
                "visible": sqs.metric("ApproximateNumberOfMessagesVisible", statistic=cloudwatch.Stats.MAXIMUM),
                "notvisible": sqs.metric("ApproximateNumberOfMessagesNotVisible", statistic=cloudwatch.Stats.MAXIMUM),
            },
        )

        # 0 to stop, 1 to start
        autoscaling.StepScalingPolicy(
            scope,
            "MyStepScalingPolicy",
            auto_scaling_group=auto_scaling_group,
            metric=metric,
            scaling_steps=[
                autoscaling.ScalingInterval(
                    change=-1,
                    # lower=0,
                    upper=0,
                ),
                autoscaling.ScalingInterval(
                    change=1,
                    lower=1,
                    upper=None,
                ),
            ],
            # the properties below are optional
            adjustment_type=autoscaling.AdjustmentType.CHANGE_IN_CAPACITY,
            cooldown=Duration.minutes(1),
            estimated_instance_warmup=Duration.minutes(0),
            # evaluation_periods=123,
            metric_aggregation_type=autoscaling.MetricAggregationType.MAXIMUM,
            # min_adjustment_magnitude=123,
        )
