# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:20:33 2024
@author: 33674
"""

from itertools import permutations

# Function to check if a given job schedule is valid
def is_valid_schedule(job_order, tasks):
    current_time = 0  # Tracks when the CPU is free
    response_times = {}  # Dictionary to store response times

    for job in job_order:
        job_name, task_id, job_arrival, job_deadline = job
        task_duration = tasks[task_id - 1][2]  # Task duration

        # Start time: CPU starts after the job arrives and after completing prior tasks
        start_time = max(current_time, job_arrival)

        # Response time calculation
        response_time = start_time + task_duration - job_arrival
        response_times[job_name] = response_time

        # Check if response time exceeds the job deadline
        finish_time = start_time + task_duration
        if finish_time > job_deadline:  # Deadline violated
            return False, response_times  # Invalid schedule

        # Update current time after job finishes execution
        current_time = finish_time

    return True, response_times  # Valid schedule

# Generate all permutations of jobs
def find_valid_schedules(jobs, tasks):
    valid_schedules = []

    for job_order in permutations(jobs):  # Iterate through all job permutations
        is_valid, response_times = is_valid_schedule(job_order, tasks)
        if is_valid:
            valid_schedules.append((list(job_order), response_times))

    return valid_schedules

# Input Data
hyperperiod = 80
number_tasks = 7

tasks = [
    [1, 10, 2],  # Task 1: [id, deadline, duration]
    [3, 10, 3],  # Task 2
    [3, 20, 2],  # Task 3
    [4, 20, 2],  # Task 4
    [5, 40, 2],  # Task 5 (Optional)
    [6, 40, 2],  # Task 6
    [7, 80, 3],  # Task 7
]

Jobs = []

# Generate Jobs
for i in range(number_tasks):
    number_jobs = hyperperiod // tasks[i][2]
    for j in range(number_jobs):
        job_name = 10 * (i + 1) + (j + 1)  # Unique job name
        Job_arrival = j * tasks[i][2]  # Arrival time
        Job_deadline = (j + 1) * tasks[i][2]  # Deadline
        job = [job_name, tasks[i][0], Job_arrival, Job_deadline]
        Jobs.append(job)

# Find all valid schedules
valid_schedules = find_valid_schedules(Jobs, tasks)

# Output Results
if valid_schedules:
    print(f"\nNumber of valid schedules: {len(valid_schedules)}")
    for idx, (schedule, response_times) in enumerate(valid_schedules):
        print(f"\nValid Schedule {idx + 1}: {[job[0] for job in schedule]}")
        print(f"Response Times: {response_times}")
else:
    print("\nNo valid schedules found.")
