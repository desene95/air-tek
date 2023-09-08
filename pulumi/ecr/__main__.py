"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ecr 

cont_registry = ecr.Repository("air_tek_registry")

pulumi.export('rep_url', cont_registry.repository_url)


