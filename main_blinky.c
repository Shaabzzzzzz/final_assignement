/*
 * FreeRTOS V202107.00
 * Copyright (C) 2020 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * https://www.FreeRTOS.org
 * https://github.com/FreeRTOS
 *
 */

/******************************************************************************
 * NOTE 1: The FreeRTOS demo threads will not be running continuously, so
 * do not expect to get real time behaviour from the FreeRTOS Linux port, or
 * this demo application.  Also, the timing information in the FreeRTOS+Trace
 * logs have no meaningful units.  See the documentation page for the Linux
 * port for further information:
 * https://freertos.org/FreeRTOS-simulator-for-Linux.html
 *
 * NOTE 2:  This project provides two demo applications.  A simple blinky style
 * project, and a more comprehensive test and demo application.  The
 * mainCREATE_SIMPLE_BLINKY_DEMO_ONLY setting in main.c is used to select
 * between the two.  See the notes on using mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
 * in main.c.  This file implements the simply blinky version.  Console output
 * is used in place of the normal LED toggling.
 *
 * NOTE 3:  This file only contains the source code that is specific to the
 * basic demo.  Generic functions, such FreeRTOS hook functions, are defined
 * in main.c.
 ******************************************************************************
 *
 * main_blinky() creates one queue, one software timer, and two tasks.  It then
 * starts the scheduler.
 *
 * The Queue Send Task:
 * The queue send task is implemented by the prvQueueSendTask() function in
 * this file.  It uses vTaskDelayUntil() to create a periodic task that sends
 * the value 100 to the queue every 200 milliseconds (please read the notes
 * above regarding the accuracy of timing under Linux).
 *
 * The Queue Send Software Timer:
 * The timer is an auto-reload timer with a period of two seconds.  The timer's
 * callback function writes the value 200 to the queue.  The callback function
 * is implemented by prvQueueSendTimerCallback() within this file.
 *
 * The Queue Receive Task:
 * The queue receive task is implemented by the prvQueueReceiveTask() function
 * in this file.  prvQueueReceiveTask() waits for data to arrive on the queue.
 * When data is received, the task checks the value of the data, then outputs a
 * message to indicate if the data came from the queue send task or the queue
 * send software timer.
 *
 * Expected Behaviour:
 * - The queue send task writes to the queue every 200ms, so every 200ms the
 *   queue receive task will output a message indicating that data was received
 *   on the queue from the queue send task.
 * - The queue send software timer has a period of two seconds, and is reset
 *   each time a key is pressed.  So if two seconds expire without a key being
 *   pressed then the queue receive task will output a message indicating that
 *   data was received on the queue from the queue send software timer.
 *
 * NOTE:  Console input and output relies on Linux system calls, which can
 * interfere with the execution of the FreeRTOS Linux port. This demo only
 * uses Linux system call occasionally. Heavier use of Linux system calls
 * may crash the port.
 */

#include <stdio.h>
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

#define mainQUEUE_LENGTH                   ( 2 )
#define mainTASK_1_PERIOD_MS               pdMS_TO_TICKS( 1000UL )
#define mainTASK_2_PERIOD_MS               pdMS_TO_TICKS( 1000UL )
#define mainTASK_3_PERIOD_MS               pdMS_TO_TICKS( 1000UL )
#define mainTASK_4_PERIOD_MS               pdMS_TO_TICKS( 1000UL )
#define mainTASK_5_PERIOD_MS               pdMS_TO_TICKS( 200UL )

/* Task Priorities */
#define mainTASK_1_PRIORITY                ( tskIDLE_PRIORITY + 4 )
#define mainTASK_2_PRIORITY                ( tskIDLE_PRIORITY + 3 )
#define mainTASK_3_PRIORITY                ( tskIDLE_PRIORITY + 2 )
#define mainTASK_4_PRIORITY                ( tskIDLE_PRIORITY + 1 )
#define mainTASK_5_PRIORITY                ( tskIDLE_PRIORITY + 5 )

/* Task Function Declarations */
static void prvTask1( void * pvParameters );
static void prvTask2( void * pvParameters );
static void prvTask3( void * pvParameters );
static void prvTask4( void * pvParameters );
static void prvTask5( void * pvParameters );
static void prvInputTask( void * pvParameters );

/* Global Variables */
static QueueHandle_t xQueue = NULL;

void main_blinky( void )
{
    xQueue = xQueueCreate( mainQUEUE_LENGTH, sizeof( uint32_t ) );

    if( xQueue != NULL )
    {
        /* Create Tasks */
        xTaskCreate( prvTask1, "Task1", configMINIMAL_STACK_SIZE, NULL, mainTASK_1_PRIORITY, NULL );
        xTaskCreate( prvTask2, "Task2", configMINIMAL_STACK_SIZE, NULL, mainTASK_2_PRIORITY, NULL );
        xTaskCreate( prvTask3, "Task3", configMINIMAL_STACK_SIZE, NULL, mainTASK_3_PRIORITY, NULL );
        xTaskCreate( prvTask4, "Task4", configMINIMAL_STACK_SIZE, NULL, mainTASK_4_PRIORITY, NULL );
        xTaskCreate( prvTask5, "Task5", configMINIMAL_STACK_SIZE, NULL, mainTASK_5_PRIORITY, NULL );
        xTaskCreate( prvInputTask, "InputTask", configMINIMAL_STACK_SIZE, NULL, mainTASK_5_PRIORITY, NULL );

        vTaskStartScheduler();
    }

    for( ; ; ) {}
}

/* Task Implementations */
static void prvTask1( void * pvParameters )
{
    for( ; ; )
    {
        vTaskDelay( mainTASK_1_PERIOD_MS );
        printf("Working\n");
    }
}

static void prvTask2( void * pvParameters )
{
    const float fahrenheit = 100.0;
    const float celsius = (fahrenheit - 32) * 5 / 9;
    for( ; ; )
    {
        vTaskDelay( mainTASK_2_PERIOD_MS );
        printf("Fahrenheit to Celsius: %.2f°C\n", celsius);
    }
}

static void prvTask3( void * pvParameters )
{
    const long int a = 1234567890;
    const long int b = 9876543210;
    const long int result = a * b;
    for( ; ; )
    {
        vTaskDelay( mainTASK_3_PERIOD_MS );
        printf("Multiplication result: %ld\n", result);
    }
}

static void prvTask4( void * pvParameters )
{
    int list[50] = {5, 8, 10, 15, 20, 30, 45, 50, 60, 70, 80, 90, 100, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480};
    int target = 250;
    int low = 0;
    int high = 49;
    int mid;
    
    for( ; ; )
    {
        vTaskDelay( mainTASK_4_PERIOD_MS );
        while (low <= high)
        {
            mid = (low + high) / 2;
            if (list[mid] == target)
            {
                printf("Element found at index %d\n", mid);
                break;
            }
            else if (list[mid] < target)
            {
                low = mid + 1;
            }
            else
            {
                high = mid - 1;
            }
        }
    }
}

static void prvTask5(void *pvParameters)
{
    int resetFlag = 0;

    for (;;)
    {
        // Take input for reset flag
        scanf("%d", &resetFlag);  // Check if input was successfully read
        
            // Print the reset flag status
        printf("Reset flag: %d\n", resetFlag);
        
        // Ensure that the reset flag is reset to 0 for the next task cycle
        resetFlag = 0;

        // Delay for the task period
        vTaskDelay(mainTASK_5_PERIOD_MS);
    }
}


static void prvInputTask( void * pvParameters )
{
    uint32_t resetInput;

    for( ; ; )
    {
        // Simulate receiving a reset input, like a button press
        // In reality, this would come from an external source like GPIO or an interrupt
        // For demonstration, we'll toggle resetInput between 0 and 1 every 200ms
        resetInput = (resetInput == 1) ? 0 : 1; // Toggle between 1 and 0

        // Send reset input to the queue
        xQueueSend(xQueue, &resetInput, 0);

        vTaskDelay(pdMS_TO_TICKS(200)); // Send every 200ms, for example
    }
}