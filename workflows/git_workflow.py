
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.git_activity import git_activity
  
@workflow.defn
class cicd:
    @workflow.run
    async def run(self,cicd: str) -> str:
        return await workflow.excute_activity(
            git_activity,
            cicd,
            schedule_to_close_timeout=timedelta(seconds=5)
        )