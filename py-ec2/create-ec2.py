import boto3
ec2 = boto3.resource('ec2', region_name='us-west-1')

# create vpc
vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
vpc.wait_until_available()

# create security group
secgroup = ec2.create_security_group(
    GroupName='sec-group1',
    Description='new security group',
    VpcId=vpc.id
)

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

# associate route table with subnet
routetable.associate_with_subnet(SubnetId=subnet.id)

# create a new security instance
instances = ec2.create_instances(
    ImageId='ami-011b6930a81cd6aaf',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}]
)
instances[0].wait_until_running()
