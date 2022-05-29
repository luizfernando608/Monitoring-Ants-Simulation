#include <vector>
using namespace std;


// ********************* Scenario 1 *********************


int NUM_THREADS = 2; // Total number of threads
int map_h = 15; //Map height
int map_w = 30;//Map Width
int simulation_time = 1200; //Simulation total time in seconds
int pheromone_timelife = 30; //Pheromone time life (in simulation time unit)
int ant_field_of_vision = 1; //Ant field of vision
int max_ants_food = 5; //Number max of ants that can collect food 
int number_of_ants = 30; // Total number of Ants
int food_quantity = 100;  // Total food quantity

vector<int> anthill_position = {0, 0}; //Anthill position vector indicates (height, width)
vector<int> food_position = {12, 20}; //Food position vector indicates (height, width)


// // ********************* Scenario 2 *********************

// int NUM_THREADS = 1; // Total number of threads
// int map_h = 15; //Map height
// int map_w = 30;//Map Width
// int simulation_time = 1200; //Simulation total time in seconds
// int pheromone_timelife = 30; //Pheromone time life (in simulation time unit)
// int ant_field_of_vision = 1; //Ant field of vision
// int max_ants_food = 5; //Number max of ants that can collect food 
// int number_of_ants = 30; // Total number of Ants
// int food_quantity = 100;  // Total food quantity

// vector<int> anthill_position = {0, 0}; //Anthill position vector indicates (height, width)
// vector<int> food_position = {12, 20}; //Food position vector indicates (height, width)


// // ********************* Scenario 3 *********************

// int NUM_THREADS = 1; // Total number of threads
// int map_h = 15; //Map height
// int map_w = 30;//Map Width
// int simulation_time = 1200; //Simulation total time in seconds
// int pheromone_timelife = 30; //Pheromone time life (in simulation time unit)
// int ant_field_of_vision = 1; //Ant field of vision
// int max_ants_food = 5; //Number max of ants that can collect food 
// int number_of_ants = 30; // Total number of Ants
// int food_quantity = 100;  // Total food quantity

// vector<int> anthill_position = {0, 0}; //Anthill position vector indicates (height, width)
// vector<int> food_position = {12, 20}; //Food position vector indicates (height, width)
