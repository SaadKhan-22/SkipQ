from difflib import Match
import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint3.sprint3_stack import Sprint3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py
def test_resources():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")

    #For the tests, we'll thus use the sprint3_stack template
    #This however, is not generated since it won't be instantiated on our local machine
    #Rather,the pipeline_stack will be instantiated here, and this will in turn instantiate the stack on the cloud
    #So, to write the tests, we use the template from the previous sprint (which was run on our local machine)
    
    template = assertions.Template.from_stack(stack)

    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/README.html


    #Checks whether the no. of lambda functions and persmissions == 2
    template.resource_count_is('AWS::Lambda::Function', 2)
    template.resource_count_is('AWS::Lambda::Permission', 2)

    #Tests the presence of a DynamoDB Table
    template.resource_count_is("AWS::DynamoDB::Table", 1)

    #Checks the required threshold
    #template.has_resource_properties("AWS::SNS::Topic", {"DeletionPolicy": "Delete"})
    
    #Checks whether the rule is enabled
    template.has_resource_properties("AWS::Events::Rule", {"State": "ENABLED"})

    #Tests whether the cron job is scheduled for each minute
    template.has_resource_properties("AWS::Events::Rule", {"ScheduleExpression": "cron(1 * * * ? *)"})

    #Whether or not the SNS subscription is directed at the specified email
    template.has_resource_properties("AWS::SNS::Subscription", {'Protocol': 'email' })
    template.has_resource_properties("AWS::SNS::Subscription", {"Endpoint": "saad.khan.skipq@gmail.com" })

    #Whether or not Dmensions contains a 'Health' key/value
    #template.has_resource_properties("AWS::S3::Bucket", {"PublicAccessBlockConfiguration": assertions.Match.object_like( {'Health': assertions.Match.absent()} ) })

    #template.has_resource_properties("AWS::S3::BucketPolicy", {"Bucket": assertions.Match.array_with( {"Ref"} )     })

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
