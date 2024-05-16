import os
import time
import boto3 
from dotenv import load_dotenv
from temporalio import activity

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION')
SECURITY_GROUP_ID = os.getenv('SECURITY_GROUP_ID')
KEY_PAIR_NAME = os.getenv('KEY_PAIR_NAME')
AMI_ID = os.getenv('AMI_ID')


aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)
ec2_client = aws_session.client('ec2')




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
