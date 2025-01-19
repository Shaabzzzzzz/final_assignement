#include <stdio.h>
#include <time.h>
#include <math.h>  


int rows = 5;  // Number of rows for GPS

// Dummy values for GPS and temperature data
float GPS[5][3][3] = {
    {{0, 0, 0}},
    {{0, 0, 0}},
    {{2, 0, 0}},
    {{2, 2, 0}},
    {{4, 2, 2}}
};
double temp_raw[] = {0, 0.5, 1, 1.5, 2}; // Example temperature data

int lenght=sizeof(temp_raw)/sizeof(temp_raw[0]);

// Function prototypes
double calculate_distance_3d(double x1, double y1, double z1, double x2, double y2, double z2);
double calculate_total_distance(float GPS[5][3][3], int rows);
float time_per_km(float GPS[][3][3], float time_spent);
double elevation(float GPS[][3][3], int rows);
void scheduler();

int main() {
    scheduler();
    return 0;
}

// Function to calculate 3D distance between two points
double calculate_distance_3d(double x1, double y1, double z1, double x2, double y2, double z2) {
    double dx = x2 - x1;
    double dy = y2 - y1;
    double dz = z2 - z1;
    return sqrt(dx * dx + dy * dy + dz * dz);
}

// Function to calculate total distance
double calculate_total_distance(float GPS[5][3][3], int rows) {
    double total_distance = 0.0;
    
    for (int i = 0; i < rows - 1; i++) 
	{
        double x1 = GPS[i][0][0], y1 = GPS[i][0][1], z1 = GPS[i][0][2];
        double x2 = GPS[i+1][0][0], y2 = GPS[i+1][0][1], z2 = GPS[i+1][0][2];
        total_distance += calculate_distance_3d(x1, y1, z1, x2, y2, z2);
    }
    
    return total_distance;
}

// Function to calculate time per kilometer
float time_per_km(float GPS[][3][3], float time_spent) {
    double total_distance = calculate_total_distance(GPS, rows);
    return (time_spent / total_distance);  // Time per km in seconds
}

// Function to calculate elevation
double elevation(float GPS[][3][3], int rows) {
    double elevation = 0.0;
    for (int i = 0; i < rows - 1; i++) {
        double z1 = GPS[i][0][2];
        double z2 = GPS[i+1][0][2];
        elevation += z2 - z1;
    }
    return elevation;
}

// Function to calculate temperature
double temperature(double temp_raw[], int length) {
    double temp = 0.0;
    for (int i = 0; i < length; i++)
	 {
        temp += 25.0 * temp_raw[i];  
    }
    return temp;
}

// Scheduler function to handle timed tasks
void scheduler() {
    float seconds;

    for (int i = 0; i < 10; i++) {
        clock_t start = clock();  // Start clock for the iteration

        // Simulate task execution
        sleep(1);

        clock_t end = clock();  // End clock after task execution
        seconds = (float)(end - start) / CLOCKS_PER_SEC;  // Calculate time in seconds

        printf("Distance: %.2f meters\n", calculate_total_distance(GPS, rows));
        sleep(2);

        printf("Time per km is %.2f minutes\n", time_per_km(GPS, seconds));
        sleep(1);

        printf("Elevation is %.2f meters\n", elevation(GPS, rows));
        sleep(1);

        printf("Temperature is %.2f°C\n", temperature(temp_raw,lenght));
        sleep(2);

        printf("Time taken for iteration %d: %.2f seconds\n\n", i+1, seconds);
    }
}
