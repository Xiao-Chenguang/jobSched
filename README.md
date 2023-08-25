# jobSched

Simple array jobs Scheduler for multiple similar jobs on both [Slurm system](https://slurm.schedmd.com/overview.html) or single machine with one line of code.

There are lots of cases where we have to run the same progrem repeatedly or similar programs with different parameters.
This simple job scheduler relieves you from the typing the similar command repeatly.
```bash
python main.py --param1 1 --param2 1
python main.py --param1 2 --param2 4
...
```

## Usage
To use this scheduler, you need simply two steps:
1. Write a function to run your job, and run all the jobs squentially.
2. Use this scheduler to run all the jobs in parallel.

### Step 1: serilization

wrip your main code in a function, and run all the jobs squentially.

```python
def run_job(param1, param2):
    # do something
    return result

# run all the jobs squentially
from itertools import product

for param1, param2 in product([1,2,3], [4,5,6]):
    run_job(param1, param2)
```

### Step 2: parallization
Use this scheduler to run all the jobs in parallel.
```python
def run_job(param1, param2):
    # do something
    return result

from jobSched import getJobs

parameList = [[1,2,3], [4,5,6]]
for jobs in getJobs(paramList):
    run_job(*jobs)
```
