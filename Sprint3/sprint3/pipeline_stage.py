from aws_cdk import (
    Stage
)
import aws_cdk as cdk
from constructs import Construct

from sprint3.sprint3_stack import Sprint3Stack


class SaadSp3Stage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        self.stage = Sprint3Stack(self, "SKAppStack")


        ####
