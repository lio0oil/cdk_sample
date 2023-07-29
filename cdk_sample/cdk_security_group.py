from aws_cdk import aws_ec2 as ec2
from constructs import Construct

import json  # noqa: F401


class CdkSecurityGroup:
    def CreateSecurityGgroup(self, scope: Construct):
        vpc = ec2.Vpc.from_lookup(scope, "vpc-08f972a0d99b8ef35", vpc_id="vpc-08f972a0d99b8ef35")

        refsg: ec2.SecurityGroup = ec2.SecurityGroup(scope, "sg2", vpc=vpc, allow_all_outbound=True)

        sg: ec2.SecurityGroup = ec2.SecurityGroup(scope, "sg1", vpc=vpc, allow_all_outbound=True)

        # inbound rule
        # all ip
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        # prefix list
        sg.add_ingress_rule(ec2.Peer.prefix_list("pl-0c3a8d0752aa790ae"), ec2.Port.tcp(3389), "RDP")
        # cidr
        sg.add_ingress_rule(ec2.Peer.ipv4("10.0.2.0/24"), ec2.Port.tcp(5432), "postgreSQL")
        # security group
        sg.add_ingress_rule(ec2.Peer.security_group_id(refsg.security_group_id), ec2.Port.tcp(3306), "MySQL")
