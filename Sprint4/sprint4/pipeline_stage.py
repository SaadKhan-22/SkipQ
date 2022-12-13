from aws_cdk import (
    Stage
)
import aws_cdk as cdk
from constructs import Construct

from sprint4.sprint4_stack import Sprint4Stack


class SaadSp4Stage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        self.stage = Sprint4Stack(self, "SKs4AppStack")


        ####
