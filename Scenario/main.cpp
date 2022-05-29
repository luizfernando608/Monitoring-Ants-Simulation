
// #include "include/scenarios.cpp"
#include "include/structures.cpp"
#include <chrono>
#include <thread>


int main(int argc, char const *argv[])
{

    // ****************** DEFINE SCENARIO ****************** 

    int NUM_THREADS = 3; // Total number of threads    
    int map_h = 15; //Map height
    int map_w = 20;//Map Width
    int simulation_time = 1400; //Simulation total time in seconds
    int pheromone_timelife = 30; //Pheromone time life (in simulation time unit)
    int ant_field_of_vision = 5; //Ant field of vision
    int max_ants_food = 9; //Number max of ants that can collect food 
    int number_of_ants = 3; // Total number of Ants
    int food_quantity = 3;  // Total food quantity
    int rep_rate = 1; // Food replacement Rate

    vector<int> anthill_position = {0, 0}; //Anthill position vector indicates (height, width)
    vector<int> food_position = {10, 15}; //Food position vector indicates (height, width)


    // ****************** INICIALIZATE ******************

    space simulation(map_h, map_w);
    anthill sauvas(anthill_position[0],anthill_position[1],number_of_ants,ant_field_of_vision,pheromone_timelife, &simulation);

    food bolo(food_quantity,rep_rate);
    simulation.map[food_position[0]][food_position[1]].set_food(&bolo);


    // simulation time counter
    long long elapsed = 0;
    auto startTime = chrono::steady_clock::now();

    // ****************** MULTI THREAD *****************

 
    do{

        AntsCounter = 0; // reset ants global counter

        // process ants in threads
        vector<std::thread*> threadList;
        threadList.reserve(NUM_THREADS);
        for (int threadInx=0; threadInx < NUM_THREADS; threadInx++) {
                thread * thread;
                thread = new std::thread(&anthill::ant_moves,&sauvas);
                threadList.push_back(thread);
        }

        for (std::thread * thread : threadList) {
            thread->join();
            cout << "\033[1;31mDeletando thread\033[0m " << endl;
            delete thread;
        }

        // update map
        bolo.update();
        simulation.show_map();

       
        std::this_thread::sleep_for(std::chrono::milliseconds(300));

        auto endTime = chrono::steady_clock::now();
        elapsed += chrono::duration_cast<chrono::seconds>(endTime - startTime).count();

    }while (elapsed <= simulation_time);

    return 0;
}
