from jobSched import getJobs

a = range(3)
b = ["a", "b", "c"]
c = ["x", "y"]

if __name__ == "__main__":
    for pid in range(3):
        print("=" * 20, "Test Case: ", pid, "=" * 20)
        jobs = getJobs(params=[a, b, c], num_task=3, pid=pid)
        # print(jobs)
