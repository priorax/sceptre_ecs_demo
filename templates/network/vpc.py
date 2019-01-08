from troposphere import Template, Output, Tags, Ref
from troposphere.ec2 import VPC,InternetGateway, VPCGatewayAttachment

class SceptreVPC():
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId') 
        self.sceptre_user_data = sceptre_user_data
        self.make_vpc()
        self.make_igw()
        self.make_outputs()
    
    def make_vpc(self):
        self.vpc = self.template.add_resource(
            VPC(
                'VPC',
                CidrBlock=self.sceptre_user_data["CidrRange"],
                Tags=Tags(
                    Name=self.sceptre_user_data["VpcName"]
                    )
                )
            )
    def make_igw(self):
        self.internet_gateway  = self.template.add_resource(
             InternetGateway(
                 'InternetGateway',
                 Tags=Tags(
                     Application=self.ref_stack_id
                     )
                    )
                )
        self.gatewayAttachment = self.template.add_resource(
            VPCGatewayAttachment(
                'AttachGateway',
                VpcId=Ref(self.vpc),
                InternetGatewayId=Ref(self.internet_gateway)))

    def make_outputs(self):
        self.vpc_output = self.template.add_output(
            Output(
                "VPC",
                Value=Ref(self.vpc)
            )
        )
        self.internetgateway_output = self.template.add_output(
            Output(
                "InternetGateway",
                Value=Ref(self.internet_gateway)
            )
        )

def sceptre_handler(sceptre_user_data):
    vpc = SceptreVPC(sceptre_user_data)
    return vpc.template.to_json()
