import boto3
import os
ec2 = boto3.resource('ec2', region_name='us-west-1')

# create vpc
vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
vpc.create_tags(Tags=[{"Key": "Name", "Value": "vpc-made-in-python"}])
vpc.wait_until_available()

keyfile = open('ec2-keypair-made-in-python.pem','w')
key_pair = ec2.create_key_pair(KeyName='ec2-keypair-made-in-python')
KeyPairOut = str(key_pair.key_material)
keyfile.write(KeyPairOut)
os.chmod('ec2-keypair-made-in-python.pem', 0400)

# create security group
secgroup = ec2.create_security_group(
    GroupName='sec-group-made-in-python',
    Description='new security group',
    VpcId=vpc.id
)
secgroup.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='icmp',
    FromPort=-1,
    ToPort=-1
)
secgroup.create_tags(Tags=[{"Key": "Name", "Value": "security-group-made-in-python"}])

# create and attach InternetGateway
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)

# create route table
routetable = vpc.create_route_table()
route = routetable.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id
)

# create subnet
subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id)
subnet.create_tags(Tags=[{"Key": "Name", "Value": "subnet-made-in-python"}])

# associate route table with subnet
routetable.associate_with_subnet(SubnetId=subnet.id)

# create a new security instance
instances = ec2.create_instances(
    ImageId='ami-011b6930a81cd6aaf',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    KeyName='ec2-keypair-made-in-python',
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [secgroup.group_id]}]
)
instances[0].wait_until_running()
instances[0].create_tags(Tags=[{"Key": "Name", "Value": "ec2-instance-made-in-python"}])
