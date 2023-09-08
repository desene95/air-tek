import pulumi
from pulumi_aws import ec2

def addition(x,y):
    z = x+y
    return z
    
eb_vpc = ec2.Vpc('eb_vpc',
              
              cidr_block='10.0.0.0/16',
              tags={
        "Name": "eb_vpc",
    }
    )

eb_subnet = ec2.Subnet('eb_subnet',
                    vpc_id=eb_vpc.id,
                    cidr_block='10.0.1.0/24')

pulumi.export('vpc_id', eb_vpc.id)
pulumi.export('subnet_id', eb_subnet.id)