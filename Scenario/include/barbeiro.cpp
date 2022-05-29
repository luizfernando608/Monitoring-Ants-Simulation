# define CHAIRS 5
#include "semaphore.cpp"

Semaphore FoodFoodSemaphore;

FoodSemaphore customers = 0;
FoodSemaphore barbers = 0;
// FoodSemaphore mutex = 1;
int waiting = 0;

void barber() {

        while (true) {
            // Accept a customer
            // (sleep if there is no customers)
            down(&customers);
            down(&mutex);

            waiting = waiting - 1;
            
            // Make the barber available
            up(&barbers);
            up(&mutex);

            // Execute the operation
            cut_hait();
        }
}


void customer(){
    // Check if can wait
    down(&mutex);

    if (waiting < CHAIRS) {

        // Check-in
        waiting = waiting + 1;
        up(&customers);
        up(&mutex);
        
        down(&barbers); // Wait for the barber
       
        get_haircut();  // Execute the operation
    } 
    
    else{
        up(&mutex);  // Maximum limit reached, skipping
    }

}











