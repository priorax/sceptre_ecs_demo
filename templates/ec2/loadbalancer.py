from troposphere import Template, Parameter, Ref, Output, GetAtt
import troposphere.elasticloadbalancingv2 as elb
import troposphere.ec2 as ec2

class LoadBalancer(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.albname_param = self.template.add_parameter(
            Parameter(
                "albname",
                Type="String"
            )
        )
        self.vpc_param = self.template.add_parameter(
            Parameter(
                "vpcid",
                Type="String"
            )
        )
        self.subnet1_param = self.template.add_parameter(
            Parameter(
                "subnet1",
                Type="String"
            )
        )
        self.subnet2_param = self.template.add_parameter(
            Parameter(
                "subnet2",
                Type="String"
            )
        )
        self.sceptre_user_data = sceptre_user_data
        self.add_alb()
        self.add_security_group()
        self.add_outputs()

    def add_alb(self):
        self.alb = self.template.add_resource(elb.LoadBalancer(
            "ALB",
            Name=Ref(self.albname_param),
            Scheme="internet-facing",
            Subnets=[Ref(self.subnet1_param), Ref(self.subnet2_param)]
        ))

    def add_security_group(self):
        self.sg = self.template.add_resource(
        ec2.SecurityGroup(
            "InstanceSecurityGroup",
            GroupDescription="Enable HTTP access on the inbound port",
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol="tcp",
                    FromPort=80,
                    ToPort=80,
                    CidrIp="0.0.0.0/0",
                )
            ],
            VpcId=Ref(self.vpc_param)
        )
    )

    def add_outputs(self):
        self.template.add_output(
            Output(
                "ALBSecurityGroup",
                Value=GetAtt(self.sg, "GroupId")
            )
        )


def sceptre_handler(sceptre_user_data):
    lb = LoadBalancer(sceptre_user_data)
    return lb.template.to_json()
