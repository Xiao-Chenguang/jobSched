import os
from itertools import product
from typing import List


def getJobs(
    params=None, num_task=1, num_proc=1, jobs=None, pid=None, platform="auto"
) -> List[List]:
    """Allocate jobs to each process based on platform
    Args:
        params: list of list of parameters
        num_task: number of tasks
        num_proc: number of processes per task
        jobs: list of jobs (product of params)
        pid: process id
        platform: platform to run the job
    Returns:
        list of jobs allocated to the process

    Example:
        >>> # run 4 parallel jobs: 2 tasks with 2 processes each
        >>> jobs_1 = getJobs(params=[[1, 2], [3, 4]], num_task=2, num_proc=2, pid=0, platform="shell")
        >>> assert jobs_1 == [1, 3]
    """
    if platform == "auto":
        if "SLURM_ARRAY_TASK_ID" in os.environ:
            platform = "slurm"
        else:
            platform = "shell"
    print("Platform: {}".format(platform))

    # extract total_proc and pid from SLURM env or shell
    # total_proc: total number of processes
    # pid: process id in range(0, total_proc)
    if platform == "slurm":
        job_id = int(os.environ["SLURM_ARRAY_JOB_ID"])
        task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
        # gpus = int(os.environ['SLURM_ARRAY_TASK_COUNT'])
        num_task = int(os.environ["SLURM_ARRAY_TASK_MAX"]) + 1
        num_proc = int(os.environ["SLURM_NTASKS"])  # use srun
        # min_task_id = int(os.environ['SLURM_ARRAY_TASK_MIN'])
        # max_task_id = int(os.environ['SLURM_ARRAY_TASK_MAX'])
        local_pid = int(os.environ["SLURM_LOCALID"])  # use srun
        pid = task_id * num_proc + local_pid
        print(
            f"schedule for job: {job_id} array: {task_id+1}/{num_task} process {local_pid+1}/{num_proc}"
        )
    elif platform != "shell":
        raise ValueError("Unknown platform: {}".format(platform))
    if pid is None:
        raise ValueError("jobId is required for platform: {}".format(platform))
    total_proc = num_task * num_proc

    alloc_jobs = []
    if jobs is not None:
        for i, x in enumerate(jobs):
            if i % total_proc == pid:
                alloc_jobs.append(x)
    elif params is not None:
        for i, x in enumerate(product(*params)):
            if i % total_proc == pid:
                alloc_jobs.append(x)

    print(f"Running job {pid} on [{platform}] with following {len(alloc_jobs)} steps:")
    for i, p in enumerate(alloc_jobs):
        print("step", i, p)
    return alloc_jobs

    # ppg = int(os.environ["SLURM_PPG"])  # custom ppg use export
    # localId = int(os.environ["SLURM_STEPID"])  # use srun step
