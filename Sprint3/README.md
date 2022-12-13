
# Welcome to Sprint 3! 


For this sprint, we'll be looking at CI/CD pipelines and how to automate them using AWS constructs and CodePipeline.

First, we make the stages of the project including the source, build, test, and deploy stages using AWS CodePipeline and other CI/CD modules.

The application being deployed measures the (default) latency and invocation metrics of a Web Crawler Lambda function. If any of these are in-alarm, it rolls back to the previous successful build.

## Source
We use a GitHub repository as the source for our code. The relevant CodePipelineSource is configured to **poll** the repository regularly for updates.

An authentication for the repository is performed using the **AWS Secrets Manager** which uses a generated token


## Build
The AWS CDK **Pipelines** Construct library is used to automate the build steps for our code. 

The ShellStep method takes as input the code source we defined in the previous step and takes a list of commands which it will execute when the stack is deployed. It takes commands as they're run on the terminal/shell.

## Testing
Two stages (Beta and Prod) are added to the pipeline.

For the **Beta** stage, a set of unit tests are added which check whether the details of provisioned AWS resource in the stack (as specified in the JSON template) meet certain criteria.

The second stage - **Prod** - adds a final Manual Approval step before deploying the application. This step needs to be performed manually by the person overseeing the deployment and ensures that all the preceeding steps are completed as desired.


## Deployment
The AWS **CodeDeploy** console is used for deploying this entire automated pipeline (after the single, initial deployment).


## Getting started

First, make sure you have the following installed in your system
* AWS CLI v2
* Python3 and its virtualenv package
* NVM and NPM 
* aws-cdk using NPM


After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv:

```
$ source .venv/bin/activate
```


Once the virtualenv is activated, you can install the required dependencies:

```
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

At this point you can now synthesize and deploy the CloudFormation template for this code:

```
$ cdk synth
$ cdk deploy
```
This wil deploy the pipeline to AWS and any subsequent changes you make to the code need only be pushed to the repository mentioned as the source in line 22 of the pipeline_stack.py file.
The pipeline will poll the repo for new commits and will automatically re-run if updates are detected.

## Post-Deployment
* Using the CodePipeline console on AWS will allow you to monitor all the stages of the app lifecycle.
* The Alarms section in the CloudWatch console will provide logs of the metrics defined in the stack and whether or not they are in-alarm.

Here's a list of udeful links to help you understand the process as well as code it for yourself:
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/README.html
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html
## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Happy Learning!
