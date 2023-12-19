import os
from itertools import product
from typing import List

def getJobs(paramLists=None, gpus=1, ppg=1, jobpar=None, jobId=None, platform='auto') -> List[List]:
    '''
    platform: 'slurm' or 'shell'
    gpus: number of gpus
    ppg: number of processes per gpu
    paramLists: list of lists of parameters
    '''
    if platform == 'auto':
        if 'SLURM_ARRAY_TASK_ID' in os.environ:
            platform = 'slurm'
        else:
            platform = 'shell'
    print('Platform: {}'.format(platform))

    if platform == 'slurm':
        job_id = int(os.environ['SLURM_ARRAY_JOB_ID'])
        taskId = int(os.environ['SLURM_ARRAY_TASK_ID'])
        # gpus = int(os.environ['SLURM_ARRAY_TASK_COUNT'])
        gpus = int(os.environ['SLURM_ARRAY_TASK_MAX']) + 1
        ppg = int(os.environ['SLURM_NTASKS'])
        # min_task_id = int(os.environ['SLURM_ARRAY_TASK_MIN'])
        # max_task_id = int(os.environ['SLURM_ARRAY_TASK_MAX'])
        localId = int(os.environ['SLURM_LOCALID'])
        jobId = taskId * ppg + localId
        print(f'schedule for job: {job_id} array: {taskId+1}/{gpus} process {localId+1}/{ppg}')
    elif platform != 'shell':
        raise ValueError('Unknown platform: {}'.format(platform))
    if jobId is None:
        raise ValueError('jobId is required for platform: {}'.format(platform))
    jobs = gpus * ppg
    # if jobId >= jobs:
    #     return []
    jobList = []
    if jobpar is not None:
        for i, x in enumerate(jobpar):
            if i % jobs == jobId:
                jobList.append(x)
    elif paramLists is not None:
        for i, x in enumerate(product(*paramLists)):
            if i % jobs == jobId:
                jobList.append(x)

    print(f'Running job {jobId} on [{platform}] with following {len(jobList)} steps:')
    for i, params in enumerate(jobList):
        print('step', i, params)
    return jobList
