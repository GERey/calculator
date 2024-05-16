import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities.aws_activity import create_vpc,create_subnet,create_internet_gateway,create_route_table,associate_route_table,create_security_group,launch_instances

from workflows.aws_workflow import SETUP_AWS


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="aws-setup-task-queue",
        workflows=[SETUP_AWS],
        activities=[create_vpc,create_subnet,create_internet_gateway,create_route_table,associate_route_table,create_security_group,launch_instances]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
                    

'''
temporal workflow start \
 --task-queue aws-setup-task-queue \
 --type SETUP_AWS

 '''