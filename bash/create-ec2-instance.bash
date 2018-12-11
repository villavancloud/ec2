#!/bin/bash

ec2-authorize default -P tcp -p 22 -s 0.0.0.0/0

aws ec2 create-key-pair --key-name bashKeyPair > bashKeyPair.pem

chmod 400 bashKeyPair.pem

aws ec2 run-instances --image-id ami-011b6930a81cd6aaf --count 1 --instance-type t1.micro --key-name bashKeyPair
