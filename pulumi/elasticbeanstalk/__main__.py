"""An AWS Python Pulumi program"""

"""An AWS Python Pulumi program"""

import sys
sys.path.append("..")
#import pulumi
import pulumi
from pulumi_aws import elasticbeanstalk
import pulumi_aws as aws
from vpc.__main__ import eb_vpc, eb_subnet
from pulumi_aws import iam, elasticbeanstalk
from datetime import timedelta
from pulumi import export


#poll_interval = timedelta(minutes=3)


#Create role and instance profile
assume_role_policy = '''{
    "Version":"2012-10-17",
    "Statement":[{
                    "Sid":"",
                    "Effect":"Allow",
                    "Principal": {
                        "Service": "elasticbeanstalk.amazonaws.com"
                        },
                    "Action":"sts:AssumeRole"}]}
    '''

assume_role_policy_ec2= '''{
    "Version":"2012-10-17",
    "Statement":[{
                    "Sid":"",
                    "Effect":"Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                        },
                    "Action":"sts:AssumeRole"}]}
    '''
eb_role = iam.Role("ebRole", assume_role_policy=assume_role_policy)
eb_ip_role = iam.Role("eb_instance_profile", assume_role_policy=assume_role_policy_ec2)

iam.RolePolicyAttachment('ebRolePolicyAttachment',
                         role=eb_role.name,
                         policy_arn='arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkEnhancedHealth'
                         )
iam.RolePolicyAttachment('ebRolePolicyAttachment-1',
                         role=eb_role.name,
                         policy_arn='arn:aws:iam::aws:policy/AWSElasticBeanstalkManagedUpdatesCustomerRolePolicy'
                         )
iam.RolePolicyAttachment('instance_profile',
                          role=eb_ip_role.name,
                          policy_arn='arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier'
                        )


iam.RolePolicyAttachment('instance_profile-1',
                          role=eb_ip_role.name,
                          policy_arn='arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess'
                        )

# Create an AWS resource (IAM Instance Profile)


eb_instance_profile = iam.InstanceProfile("eb_instance_profile", role=eb_ip_role.name )


vpc_id = eb_vpc.id

# Attach the Internet Gateway to VPC
vpc_ig= aws.ec2.InternetGateway("vpc_gw",
                     vpc_id=vpc_id,
                     tags={
                         "Name":"main"
                     }
 )

public_subnet = aws.ec2.Subnet('public_subnet',
     vpc_id=vpc_id,
     cidr_block='10.0.2.0/24', # CIDR block within the VPC's IP range
     map_public_ip_on_launch=True, # Instances get a public IP
     tags={"Name": "PublicSubnet"}) # Optional: Naming your subnet for better visibility

# # Create a Route Table
public_route_table = aws.ec2.RouteTable("public_route_table",
     vpc_id=vpc_id,
     routes=[
         aws.ec2.RouteTableRouteArgs(
             cidr_block="0.0.0.0/0",  # indicates all destinations for the traffic
             gateway_id=vpc_ig.id
         )]
 )

# # Associate the public subnet with the Route Table
public_subnet_route_table_association = aws.ec2.RouteTableAssociation('public_subnet_route_table_association',
     subnet_id=public_subnet.id,
     route_table_id=public_route_table.id)

# # Create an Elastic Beanstalk Environment and associate the Instance Profile
eb_app2 = elasticbeanstalk.Application("eb-app",
         name = "air_tek_app"
         )

eb_env2 = elasticbeanstalk.Environment("eb-env",
     application= eb_app2.name,
     solution_stack_name="64bit Amazon Linux 2023 v4.0.0 running Docker",
     settings=[
         aws.elasticbeanstalk.EnvironmentSettingArgs(
             namespace="aws:ec2:vpc",
             name="VPCId",
             value=eb_vpc.id,
         ),
         aws.elasticbeanstalk.EnvironmentSettingArgs(
             namespace="aws:ec2:vpc",
             name="Subnets",
             value=public_subnet.id,
         ),
         aws.elasticbeanstalk.EnvironmentSettingArgs(namespace="aws:autoscaling:asg",
                                                     name="MinSize", 
                                                     value="1",
                                                     ),

         aws.elasticbeanstalk.EnvironmentSettingArgs(name="MaxSize", 
                                                 value="1",
                                                namespace="aws:autoscaling:asg"),
         {
         "namespace": "aws:autoscaling:launchconfiguration",
         "name": "IamInstanceProfile",
         "value": eb_instance_profile.name
     }

],
#     poll_interval=f"{int(poll_interval.total_seconds())}s"
#     #poll_interval="30m"
  )


pulumi.export('eb_role_id', eb_role.id)
pulumi.export('instance_profile_id', eb_ip_role.id)
pulumi.export('eb_env_id', eb_env2.id)
pulumi.export('eb_env_url', eb_env2.endpoint_url)
pulumi.export('ip name', eb_instance_profile.name)
# export('poll_interval_seconds', poll_interval.total_seconds())
