#!/bin/bash

aws ec2 authorize default -P tcp -p 22 -s 0.0.0.0/0

aws ec2 create-key-pair --key-name bashKeyPair --output json | jq -r '.KeyMaterial' > bashKeyPair.pem

chmod 400 bashKeyPair.pem

IMAGE_AMI_ID=$(aws ec2 describe-images --owners amazonaws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-hvm-2.0.????????-x86_64-gp2' 'Name=state,Values=available' --output json | jq -r '.Images | sort_by(.CreationDate) | last(.[]).ImageId')

aws ec2 run-instances --image-id $IMAGE_AMI_ID --count 1 --instance-type t1.micro --key-name bashKeyPair --tag-specifications 'ResourceType=instance, Tags=[{Key=Name,Value=made-in-bash}]'
