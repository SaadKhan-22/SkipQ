from aws_cdk import (
    Duration,
    Stack,
    pipelines as pipelines_,
    aws_codepipeline_actions as actions_
        
)
import aws_cdk as cdk
from constructs import Construct
from sprint4.pipeline_stage import SaadSp4Stage


# app.py --> pipeline_stack --> pipeline_stage  --> stack

class SaadPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines the source of the code for the source stage
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        source = pipelines_.CodePipelineSource.git_hub("saadkhan2022skipq/Pegasus_Python", "main",
           # This is optional
            authentication=cdk.SecretValue.secrets_manager("sk-token"),
            trigger= actions_.GitHubTrigger('POLL')
                                )
        #Defines the build section of the code
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        synth = pipelines_.ShellStep("CodeBuild", 
                input= source,
                commands = ['cd saad/Sprint4', 
                    'pip install -r requirements.txt',
                    'npm install -g aws-cdk',
                    'cdk synth'],
                primary_output_directory= "saad/Sprint4/cdk.out"
                )

                #This is a new comment


        unit_tests_step = pipelines_.ShellStep("Unit Tests",
                        commands = ['echo "Initiating tests..."',
                        "cd saad/Sprint3",
                        'echo "Installing test requirements...."',
                        "npm install -g aws-cdk",
                        'pip install -r requirements.txt',
                        'pip install -r requirements-dev.txt',                        
                        'python3 -m pytest',
                        'echo "Tests successful: Entering the final step before Production."']
                        )

        #define integration and functional tests similarly: as Steps


        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        MyPL = pipelines_.CodePipeline(self, 'FirstPipeline', synth = synth)

        beta = SaadSp4Stage(self, 'SKbeta')
        prod = SaadSp4Stage(self, 'SKprod')

        #  Unit Tests -->  Beta --> Manual Approval
        MyPL.add_stage(beta , post = [
                        pipelines_.ShellStep("PassedTests", 
                            commands = ['echo "Entering the Manual Approval step."']
                            )], pre =[unit_tests_step] )

        #As the last step, adds a manual approval for a human to oversee
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ManualApprovalStep.html
        MyPL.add_stage(prod, pre=[
        pipelines_.ManualApprovalStep("ReleaseToProd")
                ])
   #

