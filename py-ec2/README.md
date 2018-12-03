prerequisites: Have awscli ((pip install) or download zip, unzip and run installer) and boto3 installed. also have the aws creds configured by running the command "aws configure".

To create a new keypair run:

python create-kp.py

chmod 400 ec2-keypair.pem

To create EC2 instance(s) run:

python create-ec2-instances.py
