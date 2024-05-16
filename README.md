# Python Temporal Example


## How to run 

You can start a virtual environment in python in order to not pollute your environment, but otherwise the worker named "calculator.py" should have everything you need to have a running working. 
I used the dev instance and also played around with the docker containers to understand a little bit more about how open source users might be scaling this out.

The architecture of this follows what seemed to be best practices. 

The worker is in a worker folder.

The workflows has two workflows, only one of which is used. That is the aws_workflow that runs the following activities. 
  - create vpc
  - create subnet
  - create internet gateway
  - create route table
  - associate route table with subnet
  - create a security group in the subnet to associate with the instance id
  - return the instance ID.

When finished running it should create a t2 micro, although that is configurable using a .env file. You'll need the following in the .env file in order to run this temporal workflow.

```
.env

AWS_ACCESS_KEY_ID=???
AWS_SECRET_ACCESS_KEY=????
AWS_REGION=us-west-1
SECURITY_GROUP_NAME=Temporal_Security_Group
KEY_PAIR_NAME=gmoney
AMI_ID=ami-0cbe318e714fc9a82  # just a standard aws ami but you could use whatever you want here too 
```

Then you can run the below to start the task.

```
temporal workflow start \
 --task-queue aws-setup-task-queue \
 --type SETUP_AWS
```

Then you can use the below command to start the worker. 

`poetry run python worker/calculator.py` Remember that poetry will be sad if you run it without a virtual environment.  

Things that I would like to implement next time are a destory if there is a failure so that I don't need to clean things up by hand. 


# Notes on implementation

This felt generally straight forward, although I needed to set the retry's to 1 since in this application, if something fails, I need to cleanup the state before I want to continue. I could absolutely just take in the values I already have to destory right after I do it but want to keep them around to show I did them. 

#TODO:

There are a few things I'll do in the coming days before the interview. 
1.) Clean up the git workflows 
2.) I'll try to work in some more distributed system concepts like 
  - Timers for the the times I'm waiting for instances to come up
  - 

