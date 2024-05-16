
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities.aws_activity import create_vpc,create_subnet


@workflow.defn
class SETUP_AWS:
    @workflow.run
    async def run(self) -> str:

        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(minutes=1),
            maximum_attempts=1
        )

        vpc_id = await workflow.execute_activity(create_vpc, schedule_to_close_timeout=timedelta(minutes=5) ,retry_policy=retry_policy)
        subnet_id = await workflow.execute_activity(create_subnet,vpc_id ,schedule_to_close_timeout=timedelta(minutes=5) ,retry_policy=retry_policy)
        return subnet_id

# @workflow.defn
# class DESTROY_AWS:
#     @workflow.run
#     async def run(self) -> str:

#         vpc_id = await workflow.execute_activity(DESTROY_AWS_vpc, schedule_to_close_timeout=timedelta(minutes=5) )
#         return vpc_id

