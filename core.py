import os
from itertools import product

def getJobs(gpus, ppg, paramLists, jobId=0, platform='auto'):
    '''
    platform: 'slurm' or 'online'
    gpus: number of gpus
    ppg: number of processes per gpu
    paramLists: list of lists of parameters
    '''
    jobs = gpus * ppg
    if platform == 'auto':
        if 'SLURM_JOBID' in os.environ:
            platform = 'slurm'
        else:
            platform = 'online'
    print('Platform: {}'.format(platform))

    if platform == 'slurm':
        taskId = int(os.environ['SLURM_ARRAY_TASK_ID'])
        localId = int(os.environ['SLURM_LOCALID'])
        jobId = taskId * ppg + localId
        print(f'taskId: {taskId}, localId: {localId}, jobId: {jobId}')
    elif platform != 'online':
        raise ValueError('Unknown platform: {}'.format(platform))
    if jobId >= jobs:
        return ValueError('jobId must be less than {}'.format(jobs))
    jobList = []
    for i, x in enumerate(product(*paramLists)):
        if i % jobs == jobId:
            jobList.append(x)

    print(f'Running on [{platform}] with jobId: {jobId} with following parameters:\n{jobList}')
    return jobList
