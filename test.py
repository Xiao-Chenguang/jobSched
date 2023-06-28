from jobSched import getJobs

a = range(3)
b = ['a', 'b', 'c']
c = ['x', 'y']

if __name__ == '__main__':
    for id in range(3):
        print('='*20, 'Test Case: ', id, '='*20)
        jobs = getJobs(paramLists=[a, b, c], ppg=3, jobId=id)
        # print(jobs)