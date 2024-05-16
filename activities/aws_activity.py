import os
import time
import boto3 
from dotenv import load_dotenv
from temporalio import activity

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION')
SECURITY_GROUP_NAME = os.getenv('SECURITY_GROUP_NAME')
KEY_PAIR_NAME = os.getenv('KEY_PAIR_NAME')
AMI_ID = os.getenv('AMI_ID')


aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)
ec2_client = aws_session.client('ec2')


'''
Plan of action

Create VPC x  (Do this for extra credit maybe?  dont' create if it already exists just pull it and return )
Create Subnet x ( Do this for extra credit maybe? hopefully don't create if it already exists just pull it and return )
Create internet gateway x
create route table x

create security groups oops 

put the route table with the subnet

launch aws t2.micro instance. 

'''

#This could be async, synchronous multithread, or multiprocess. Totally Up to you!
# This information needs to be serializable
@activity.defn
async def create_vpc() -> str:
    response = ec2_client.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = response['Vpc']['VpcId']
    
    ec2_client.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'Temporal_VPC'}])
    
    while True:
        vpc = ec2_client.describe_vpcs(VpcIds=[vpc_id])
        if vpc['Vpcs'][0]['State'] == 'available':
            break
        time.sleep(2)
    return vpc_id

@activity.defn
async def create_subnet(vpc_id):
    response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24')
    subnet_id = response['Subnet']['SubnetId']
    ec2_client.create_tags(Resources=[subnet_id], Tags=[{'Key': 'Name', 'Value': 'Temporal_Subnet'}])
    return subnet_id

@activity.defn
async def create_internet_gateway(vpc_id):
    response = ec2_client.create_internet_gateway()
    internet_gateway_id = response['InternetGateway']['InternetGatewayId']
    ec2_client.attach_internet_gateway(InternetGatewayId=internet_gateway_id, VpcId=vpc_id)
    return internet_gateway_id

@activity.defn
async def create_route_table(awsIds):
    response = ec2_client.create_route_table(VpcId=awsIds[0])
    route_table_id = response['RouteTable']['RouteTableId']
    ec2_client.create_route(RouteTableId=route_table_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=awsIds[1])
    return route_table_id

@activity.defn
async def associate_route_table(awsIds):
    ec2_client.associate_route_table(RouteTableId=awsIds[0], SubnetId= awsIds[1])

@activity.defn
async def create_security_group(vpc_id):
    response = ec2_client.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description='Temporal Created Security group',
        VpcId=vpc_id
    )
    security_group_id = response['GroupId']
    
    # Add an inbound rule only allowing my ip to ssh into the box.
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '104.28.124.166/32'}]
        }]
    )
    return security_group_id


@activity.defn
async def launch_instances(awsIds):
    networkInterfaces=[{
        'SubnetId': awsIds[0],  #subnet
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [awsIds[1]]  #security groud id 
    }]


    response = ec2_client.run_instances(ImageId=AMI_ID,InstanceType='t2.micro',KeyName=KEY_PAIR_NAME, MaxCount=1,MinCount=1,NetworkInterfaces=networkInterfaces)

    instance_id = response['Instances'][0]['InstanceId']
    ec2_client.create_tags(Resources=[instance_id], Tags=[{'Key': 'Name', 'Value': 'Temporal Instance'}])
    return instance_id
