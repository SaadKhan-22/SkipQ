from cgitb import handler
from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_events as events_,
    aws_events_targets as target_,
    aws_cloudwatch as cloudwatch_,
    aws_cloudwatch_actions as cw_actions_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as db
    
)
from constructs import Construct
from resources import constants

class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Automated Lambda for Web Health
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        Lambda_role = self.create_Lambda_role()
        WH_lambda = self.create_lambda("WebHealthLambda", "./resources", "WH_lambda.lambda_handler", Lambda_role)
        WH_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        

        table = self.create_table(id = "SaadKAlarmTable")
        table.apply_removal_policy(RemovalPolicy.DESTROY)

        DB_lambda = self.create_lambda("DynamoDBLambda", "./resources", "DB_lambda.lambda_handler", Lambda_role)
        DB_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        tname = table.table_name

        DB_lambda.add_environment(key = 'SaadKAlarmsTableName', value = tname)

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint1Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        schedule = events_.Schedule.cron( minute="1")
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events/Schedule.html

        target = target_.LambdaFunction(handler = WH_lambda)
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets/README.html

        rule = events_.Rule(self, "WHlambdaEventRule",
        description = "Sets the rule for auto events for the Lambda",
        schedule = schedule,
        targets = [target]  )

        rule.apply_removal_policy(RemovalPolicy.DESTROY)
        



#define threshold and create an alarm

        dimensions = {'URL': constants.URL_TO_MONITOR}

#https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html
        availMetric = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE, metric_name  = constants.URL_MONITOR_METRIC_NAME_AVAILABILITY, 
        dimensions_map = dimensions, 
        label=None, period = Duration.minutes(1) )

        latMetric = cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE, metric_name = constants.URL_MONITOR_METRIC_NAME_LATENCY,
        dimensions_map = dimensions, 
        label=None, period = Duration.minutes(1) )



#https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html
        availAlarm = cloudwatch_.Alarm( self , "AvailabilityAlarm",
            comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            threshold= 1,
            evaluation_periods=1,
            metric = availMetric
             )
        availAlarm.apply_removal_policy(RemovalPolicy.DESTROY)

        latAlarm = cloudwatch_.Alarm( self , "LatencyAlarm",
            threshold= 0.3,
            evaluation_periods=1,
            metric= latMetric
                )
        latAlarm.apply_removal_policy(RemovalPolicy.DESTROY)


        topic = sns_.Topic(self, "WebHealthAlarm")
        latAlarm.add_alarm_action(cw_actions_.SnsAction(topic))
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html


        topic.add_subscription(subscriptions_.EmailSubscription("saad.khan.skipq@gmail.com"))
        topic.add_subscription(subscriptions_.LambdaSubscription(DB_lambda))
        
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.apply_removal_policy(RemovalPolicy.DESTROY)

#creating lambda 
    def create_lambda(self, id_ , path, handler, role):
        return lambda_.Function(self, id_,
        runtime = lambda_.Runtime.PYTHON_3_8,
        handler = handler,
        code = lambda_.Code.from_asset(path),
        role = role
        
        )

    def create_Lambda_role(self):

        Lambda_role = iam_.Role(self, "Lambda Role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies= [iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                               iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess') ]
            )
      
        return Lambda_role

    def create_table(self, id):
        table = db.Table(self, id,
       partition_key = db.Attribute(name="AlarmName", type = db.AttributeType.STRING),
       removal_policy= RemovalPolicy.DESTROY,
       sort_key = db.Attribute(name="Timestamp", type = db.AttributeType.STRING)  
                                    )
        return table