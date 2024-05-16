


from temporalio import activity

#This could be async, synchronous multithread, or multiprocess. Totally Up to you!
# This information needs to be serializable
@activity.defn
async def git_activity(ci) -> str:
    
    return "pass"