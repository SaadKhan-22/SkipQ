
# Welcome to Sprint 4! 


We'll be creating a CRUD API endpoint for our web crawler (from previous sprints) which will allow it to publish metrics from URls of a user's choice.

A new DynamoDB table will hold the URLs to monitor and its entries will be dynamic via CRUD REST commands.


The application being deployed measures the (default) latency and invocation metrics of a Web Crawler Lambda function. If any of these are in-alarm, it rolls back to the previous successful build.
## URL Table
A new DynamoDB table will hold the entries we need monitored, and its values will be created/read/updated/deleted via a Lambda function.
The two columns it uses are the URL_ID and URL, which store the id and name, respectively, of the URL the user enters via the API.

## Lambda
A new Lambda function will perform the required operations on the DynamoDB table by executing the API's specified commands.

## API Gateway
The AWS APIGateway construct is used to provide an interface to the lambda which allows a RESTful interface to specify user commands.


## CRUD Operations
The following is a list of the CRUD operations which will be available for a user of the API endpoint to perform :-

#### GET
Retrieves a URL from the URL Table.
#### POST 
Adds a new URL entry in the table.
#### PATCH
Updates an existing entry in the table.
#### DELETE
Deletes an entry from the table.

## Integration
Architecture from previous sprints (Sprint 3 namely) has had to be changed to allow integration with the dynamic nature of this new application: URLs are no longer constants and each requires integration with the metric-calculating Lambda (from Sprint 2) and Stack so that metric calculation, alarms, and alarm logging can be supported for it.
 



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

## Usage
The AWS API Gateway console generates a URL for interacting with the application. The required CRUD operations can be performed using this URL.

Here's a list of udeful links to help you understand the additions to the original as well as code it for yourself:
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/README.html#aws-lambda-backed-apis
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html#aws_cdk.aws_apigateway.Resource.add_method
* https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaIntegration.html

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Happy Learning!
