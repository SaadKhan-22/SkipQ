
# Welcome to Sprint 1 of SkipQ!


## Introduction
* In this Sprint, a basic lambda function is deployed on the cloud using the AWS Cloud Development Kit

This is a guide on how to deploy your first Lambda function using a clone of the Pegasus_Python repo.

## Setup

* Clone the repository
* Configure your aws using the command below and use your credentials at the appropriate prompts

```
$ aws --configure
```
* Setup your virtual environment using 

```
source .venv/bin/activate 
```

* Then, install the requirements using 

 ```
 pip3.8 install -r requirements.txt
 ```
* Run the command `cdk synth` to synthesize the Lambda function as specified in the code
* Run `cdk deploy` to deploy the Lambda to AWS
## How to Run
* A trigger can be added to activate the Lambda function
* The Lambda function can also be run from the console
## Output Screenshots
Configure Test Event
![Configure Test Event Screenshot](/saad/sprint1/resources/Test2Capture.jpg)


Execution Result
![Execution Result Screenshot](/saad/sprint1/resources/TestCapture.jpg)

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

__Have fun learning!__
