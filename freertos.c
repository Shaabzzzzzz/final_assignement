#include <stdio.h>
#include "FreeRTOS.h"
#include "task.h"

// Constants for tasks
#define TASK1_PERIOD pdMS_TO_TICKS(1000) // 1 second
#define TASK2_PERIOD pdMS_TO_TICKS(2000) // 2 seconds
#define TASK3_PERIOD pdMS_TO_TICKS(3000) // 3 seconds
#define TASK4_PERIOD pdMS_TO_TICKS(4000) // 4 seconds

// Function prototypes
void vPeriodicTask1(void *pvParameters);
void vPeriodicTask2(void *pvParameters);
void vPeriodicTask3(void *pvParameters);
void vPeriodicTask4(void *pvParameters);
void vAperiodicTask(void *pvParameters);

// Task handles (optional, for better control)
TaskHandle_t xAperiodicTaskHandle = NULL;

int main(void)
{
    // Create tasks
    xTaskCreate(vPeriodicTask1, "Task1", 1000, NULL, 1, NULL);
    xTaskCreate(vPeriodicTask2, "Task2", 1000, NULL, 1, NULL);
    xTaskCreate(vPeriodicTask3, "Task3", 1000, NULL, 1, NULL);
    xTaskCreate(vPeriodicTask4, "Task4", 1000, NULL, 1, NULL);

    // Optional: Aperiodic task created but not started immediately
    xTaskCreate(vAperiodicTask, "AperiodicTask", 1000, NULL, 1, &xAperiodicTaskHandle);
    vTaskSuspend(xAperiodicTaskHandle); // Suspended initially

    // Start the scheduler
    vTaskStartScheduler();

    // Infinite loop (should never reach here)
    for (;;);
}

void vPeriodicTask1(void *pvParameters)
{
    TickType_t xLastWakeTime = xTaskGetTickCount();

    for (;;)
    {
        printf("Working\n");
        vTaskDelayUntil(&xLastWakeTime, TASK1_PERIOD);
    }
}

void vPeriodicTask2(void *pvParameters)
{
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const float fahrenheit = 98.6f; // Example fixed value

    for (;;)
    {
        float celsius = (fahrenheit - 32) * 5.0 / 9.0;
        printf("Fahrenheit: %.2f, Celsius: %.2f\n", fahrenheit, celsius);
        vTaskDelayUntil(&xLastWakeTime, TASK2_PERIOD);
    }
}

void vPeriodicTask3(void *pvParameters)
{
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const long int num1 = 123456789;
    const long int num2 = 987654321;

    for (;;)
    {
        long int result = num1 * num2;
        printf("Multiplication result: %ld\n", result);
        vTaskDelayUntil(&xLastWakeTime, TASK3_PERIOD);
    }
}

void vPeriodicTask4(void *pvParameters)
{
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const int list[50] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                          10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                          20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                          30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                          40, 41, 42, 43, 44, 45, 46, 47, 48, 49};
    const int target = 25; // Element to search

    for (;;)
    {
        int left = 0, right = 49, mid;
        int found = 0;

        while (left <= right)
        {
            mid = left + (right - left) / 2;

            if (list[mid] == target)
            {
                found = 1;
                break;
            }
            else if (list[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }

        if (found)
        {
            printf("Element %d found at index %d\n", target, mid);
        }
        else
        {
            printf("Element %d not found\n", target);
        }

        vTaskDelayUntil(&xLastWakeTime, TASK4_PERIOD);
    }
}

void vAperiodicTask(void *pvParameters)
{
    for (;;)
    {
        // Simulate 100ms execution
        vTaskDelay(pdMS_TO_TICKS(100));
        printf("Aperiodic Task executed\n");

        // Suspend itself after execution
        vTaskSuspend(NULL);
    }
}

// Trigger the aperiodic task (example function)
void triggerAperiodicTask(void)
{
    if (xAperiodicTaskHandle != NULL)
    {
        vTaskResume(xAperiodicTaskHandle);
    }
}