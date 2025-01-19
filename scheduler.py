
hyperperiod =80
number_tasks = 7

tasks = [
    [1, 10, 2],  # Task 1: [id, deadline, duration]
    [2, 10, 2],  # Task 2
    [3, 20, 2],  # Task 3
    [4, 20, 2],  # Task 4
    [5, 40, 2],  # Task 5 (Optional)
    [6, 40, 2],  # Task 6
    [7, 80, 3],  # Task 7
]


Jobs = []

# Loop through each task and generate jobs
for i in range(number_tasks):
    # Calculate the number of jobs for the task in the given hyperperiod
    number_jobs = hyperperiod // tasks[i][2]
    
    # Generate jobs for each task
    for j in range(number_jobs):
        job_name = 10 * (i + 1) + (j + 1)  # Job name
        
        # Job arrival time and job deadline
        Job_arrival = j * tasks[i][2]
        Job_deadline = (j + 1) * tasks[i][2]
        
       
        job = [job_name, tasks[i][0], Job_arrival, Job_deadline]
        Jobs.append(job)

#%%
# Updated schedule function to check response time < deadline
def schedule_job_tasks_fcfs_with_deadline_check(jobs, tasks):
    total_waiting_time = 0
    total_response_time = 0
    missed_tasks = []  # List of jobs missing deadlines
    skipped_tasks = []  # Skipped optional jobs
    response_times = {}  # Response time for each job

    jobs.sort(key=lambda x: x[2])  # Sort jobs by their arrival time

    current_time = 0
    valid_schedule = []  # List to store valid jobs

    for job in jobs:
        job_name, task_id, job_arrival, job_deadline = job

        # Optional Task Handling (Task 5)
        if task_id == 5:  # Task 5 is optional
            task_duration = tasks[task_id - 1][2]
            if current_time + task_duration > job_deadline:
                skipped_tasks.append(job_name)  # Skip optional job
                continue

        # Ensure job arrives before execution
        if current_time < job_arrival:
            current_time = job_arrival

        task_duration = tasks[task_id - 1][2]  # Duration of the task

        # Check if response time exceeds deadline
        response_time = current_time + task_duration - job_arrival
        if current_time + task_duration > job_deadline:  # Response exceeds deadline
            missed_tasks.append(job_name)  # Job cannot meet deadline
            return None, None, None, missed_tasks, skipped_tasks, None  # Prune this schedule

        # Calculate waiting time
        waiting_time = current_time - job_arrival
        total_waiting_time += waiting_time

        # Record response time
        total_response_time += response_time
        response_times[job_name] = response_time

        # Update current time and valid schedule
        current_time += task_duration
        valid_schedule.append(job_name)

    return valid_schedule, total_waiting_time, total_response_time, missed_tasks, skipped_tasks, response_times


# Execution
valid_schedule, total_waiting_time, total_response_time, missed_tasks, skipped_tasks, response_times = schedule_job_tasks_fcfs_with_deadline_check(Jobs, tasks)

# Print results
if valid_schedule:
    print("\nValid schedule:")
    print(valid_schedule)
    print(f"Total waiting time: {total_waiting_time}")
    print(f"Total response time: {total_response_time}")
    print(f"Response times: {response_times}")
else:
    print("\nInvalid schedule: Response time exceeds deadline for one or more jobs.")
    print(f"Missed tasks: {missed_tasks}")

#%%
def schedule_jobs_edf(jobs, tasks):
    total_waiting_time = 0
    total_idle_time = 0
    response_times = {}
    skipped_tasks = []
    missed_tasks = []
    current_time = 0
    schedule = []

    # Sort jobs initially by arrival time
    jobs.sort(key=lambda x: x[2])

    while jobs:
        # Get ready jobs (those that have arrived)
        ready_jobs = [job for job in jobs if job[2] <= current_time]

        if ready_jobs:
            # Sort ready jobs by their deadlines (EDF scheduling)
            ready_jobs.sort(key=lambda x: x[3])

            # Pick the job with the earliest deadline
            current_job = ready_jobs[0]
            job_name, task_id, job_arrival, job_deadline = current_job

            # Optional task (Task 5 handling)
            if task_id == 5:
                task_duration = tasks[task_id - 1][2]
                if current_time + task_duration > job_deadline:
                    skipped_tasks.append(job_name)
                    jobs.remove(current_job)
                    continue

            # Calculate waiting time and update total
            waiting_time = current_time - job_arrival
            total_waiting_time += waiting_time

            # Response time (finish time - arrival time)
            task_duration = tasks[task_id - 1][2]
            response_time = current_time + task_duration - job_arrival
            response_times[job_name] = response_time

            # Update schedule
            schedule.append((current_time, job_name))

            # Update current time
            current_time += task_duration
            jobs.remove(current_job)
        else:
            # No ready jobs → idle time
            schedule.append((current_time, "Idle"))
            total_idle_time += 1
            current_time += 1

    return schedule, total_waiting_time, total_idle_time, skipped_tasks, missed_tasks, response_times


# Execution
schedule, total_waiting_time, total_idle_time, skipped_tasks, missed_tasks, response_times = schedule_jobs_edf(Jobs, tasks)

# Print the results
print("EDF Schedule:")
for time, job in schedule:
    print(f"Time {time}: {job}")

print(f"\nTotal Waiting Time: {total_waiting_time}")
print(f"Total Idle Time: {total_idle_time}")

