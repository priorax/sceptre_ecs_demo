from troposphere import Template, Parameter, Ref
import troposphere.elasticloadbalancingv2 as elb
import troposphere.ec2 as ec2

class LoadBalancer(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptre_user_data = sceptre_user_data
        self.add_alb()
        self.add_security_group()
        self.add_outputs()

    def add_alb(self):
        self.alb = self.template.add_resource(elb.LoadBalancer(
            self.sceptre_user_data["alb_name"],
            Name="ApplicationElasticLB",
            Scheme="internet-facing",
            Subnets=[self.sceptre_user_data["subnet1"], self.sceptre_user_data["subnet2"]]
        ))

    def add_security_group(self):
        self.sg = self.template.template.add_resource(
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
            ]
        )
    )

    def add_outputs(self):
        self.template.add_output(
            Output(
                "ALBSecurityGroup",
                Value=Ref(self.sg)
            )
        )


def sceptre_handler(sceptre_user_data):
    lb = LoadBalancer(sceptre_user_data)
    return lb.template.to_json()
2