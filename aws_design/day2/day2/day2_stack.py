from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as api_,
    aws_lambda as lambda_,
    RemovalPolicy,
    CfnOutput,
    aws_iam as iam_
    
    # aws_sqs as sqs,
)
from constructs import Construct

class Day2Stack(Stack):

    def _init_(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super()._init_(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()

        #Setting up api lambda
        api_lambda = self.create_lambda("SK_API_DAY2", 'api_lambda.lambda_handler', "./resources", lambda_role)
        api_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        #Api gateway 1
        app_api = api_.LambdaRestApi(self, 'API-SK Day2 1', handler=api_lambda, proxy=False)
        app_api.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        # Create CRUD Ops to API
        alarms = app_api.root.add_resource("events")
        alarms.add_method("POST")
        
        # Print API URL 1.0
        self._api_url = CfnOutput(self, 'SK_API_URL 1', value=app_api.url, description="API URL used to call API Lambda")

        #Api gateway2
        app_api = api_.LambdaRestApi(self, 'API-SK- Day2 2', handler=api_lambda, proxy=False)
        app_api.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        # Create CRUD Ops to API
        alarms = app_api.root.add_resource("events")
        alarms.add_method("POST")
        
        # Print API URL 2.0
        self._api_url = CfnOutput(self, 'SK_API_URL 2', value=app_api.url, description="API URL used to call API Lambda")
        
        
        
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
    def create_lambda(self, id, handler, path,role):
        return lambda_.Function(self, id,
                        runtime=lambda_.Runtime.PYTHON_3_8,
                        handler=handler,
                        code=lambda_.Code.from_asset(path),
                        timeout=Duration.seconds(15),
                        role=role
                    )
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html
    def create_lambda_role(self):
        return iam_.Role(self, "lambda-role",
                        assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')

                        ]
                    )