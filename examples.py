# examples of jobSched usage
from jobSched import getJobs


def experimet(param1, param2, param3):
    print("param1: %s, param2: %s, param3: %s" % (param1, param2, param3))


if __name__ == "__main__":
    # prepare parameter lists
    p1 = [1, 2, 3]
    p2 = ["a", "b", "c"]
    p3 = ["Jeff", "John", "Jack"]

    # run jobs in parallel
    for job in getJobs(params=[p1, p2, p3], num_task=4):
        experimet(*job)
