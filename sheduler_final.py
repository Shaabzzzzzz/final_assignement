# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 08:29:23 2025

@author: 33674
"""
hyperperiod = 80
number_tasks = 7

# Define the tasks: [id, period, duration]
tasks = [
    [1, 10, 2],  # Task 1
    [2, 10, 2],  # Task 2
    [3, 20, 2],  # Task 3
    [4, 20, 2],  # Task 4
    [5, 40, 2],  # Task 5(optional)
    [6, 40, 2],  # Task 6
    [7, 80, 3],  # Task 7
]

# Generate jobs: [job_id, task_id, arrival_time, deadline, duration]
Jobs = []
for task in tasks:
    task_id, period, duration = task
    num_jobs = hyperperiod // period
    for j in range(num_jobs):
        job_id = f"T{task_id}_J{j + 1}"
        arrival_time = j * period
        deadline = (j + 1) * period
        Jobs.append([job_id, task_id, arrival_time, deadline, duration])

# Sort jobs by arrival time, then by deadline
Jobs.sort(key=lambda x: (x[2], x[3]))

# making sure that no deadline is missed 
schedule = []  # To store the schedule as [start_time, end_time, job_id]
time = 0  # Current time
waiting_time = 0  # Total waiting time

while Jobs:
    # Get jobs that have arrived
    available_jobs = [job for job in Jobs if job[2] <= time]

    if available_jobs:
        # Select the job with the earliest deadline
        available_jobs.sort(key=lambda x: x[3])
        selected_job = available_jobs[0]
        job_id, task_id, arrival_time, deadline, duration = selected_job

        # Ensure jobs are not scheduled twice
        if any(sch[2] == job_id for sch in schedule):
            Jobs.remove(selected_job)
            continue

        # Schedule the job
        start_time = max(time, arrival_time)
        end_time = start_time + duration
        schedule.append([start_time, end_time, job_id])

        # Update waiting time
        waiting_time += start_time - arrival_time

        # Advance time and remove the job from the list
        time = end_time
        Jobs.remove(selected_job)
    else:
        # If no jobs are available, advance time
        time += 1

# Calculate total idle time
idle_time = hyperperiod - sum([slot[1] - slot[0] for slot in schedule])

# Print the schedule
print("Schedule:")
for slot in schedule:
    print(f"Job {slot[2]} runs from {slot[0]} to {slot[1]}")

print(f"\nTotal waiting time: {waiting_time}")
print(f"Total idle time: {idle_time}")
