#include <vector>
#include <iostream>
#include <random>
#include <cstdlib>
#include <string>
#include <mutex>
#include <thread>
using namespace std;

#include "food.cpp"

// ************************************** MAP STRUCTURES **************************************
// visualization auxiliar functions
void gotoxy(int x, int y) { printf("%c[%d;%df", 0x1B, y, x); }
void clrscr(void) { system("clear"); }

// tail mutex
mutex TailMutex;

/*
Tail Structure
 */
struct space_unit
{
    int ant_number = 0;
    int pheromone_life = 0;

    bool has_anthill = false;

    int w_pheromone_food_direction;
    int h_pheromone_food_direction;

    // bool has_food = false;
    food *current_food = NULL;

    // Visualization of the unit
    string visualization = " ";

    void set_ant() { ant_number++; }
    void remove_ant() { ant_number--; }

    void set_anthill() { has_anthill = true; }
    void remove_anthill() { has_anthill = false; }

    void set_pheromone(int quantity) { pheromone_life = quantity; }
    void decay_pheromone()
    {
        if (pheromone_life > 0)
        {
            pheromone_life--;
        }
        if (pheromone_life == 0)
        {
            h_pheromone_food_direction = 0;
            w_pheromone_food_direction = 0;
        }
    }

    bool has_food()
    {
        if (current_food != NULL)
        {
            if ((*current_food).current_quantity > 0)
            {
                return true;
            }
        }
        return false;
    }

    void set_food(food *pointer)
    {
        current_food = pointer;
    }

    food *get_food()
    {
        return current_food;
    }

    void generate_visualization()
    {
        if (has_anthill)
        {
            visualization = "\033[1;41m \033[0m";
        }
        else if (has_food())
        {
            visualization = "\033[1;43m \033[0m";
        }
        else if (ant_number > 0)
        {
            visualization = "\033[1;31m*\033[0m";
        }
        else if (pheromone_life > 0)
        {
            visualization = "\033[1;35m•\033[0m";
        }
        else
        {
            visualization = " ";
        }
    }

    void show()
    {
        this->generate_visualization();
        cout << visualization;
    }
};

/*
Space Structure
 */
struct space
{
    // Space dimension
    int width;
    int height;

    vector<vector<space_unit>> map; // Matrix with space_unit

    // ******************* CONSTRUCTOR **************************
    space(int h_dimension, int w_dimension)
    {
        width = w_dimension;
        height = h_dimension;

        for (int i = 0; i < h_dimension; i++)
        {
            map.push_back(vector<space_unit>());
            for (int j = 0; j < w_dimension; j++)
            {
                map[i].push_back(*new space_unit());
            }
        }
    };

    // escrita
    void set_ant_map(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).set_ant();
    } // Set an ant at (i,j) position in the space
    void remove_ant_map(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).remove_ant();
    } // Remove an ant at (i,j) position
    void set_pheromone_map(int i, int j, int quantity)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).set_pheromone(quantity);
    } // Set pheromone to terminal visualizationat position (i,j)
    void decay_pheromone_map(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).decay_pheromone();
    } // Remove a pheromone at (i,j) position
    void set_anthill_map(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).set_anthill();
    } // Set anthill to terminal visualization at position (i,j)
    void remove_anthill_map(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).remove_anthill();
    } // Remove an anthill at (i,j) position

    void set_phe_w_direction(int i, int j, int direction)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).w_pheromone_food_direction = direction;
    } // Remove an anthill at (i,j) position
    void set_phe_h_direction(int i, int j, int direction)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        (*check_position(i, j)).w_pheromone_food_direction = direction;
    } // Remove an anthill at (i,j) position

    // leitura
    bool check_food(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        return (*check_position(i, j)).has_food();
    }
    int check_phe_life(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        return (*check_position(i, j)).pheromone_life;
    }

    // void try_get_food(int i, int j) { (*check_position(i,j)).get_food(); }

    // int w_phe_food_di(int i, int j) { (*check_position(i,j)); }
    int h_phe_food_di(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        return (*check_position(i, j)).h_pheromone_food_direction;
    }
    int w_phe_food_di(int i, int j)
    {
        const lock_guard<std::mutex> lock(TailMutex);
        return (*check_position(i, j)).w_pheromone_food_direction;
    }

    space_unit *check_position(int i, int j)
    {
        // const lock_guard<std::mutex> lock(TailMutex);
        return &(map[i][j]);
    }

    // //***************************************** Update the terminal //*****************************************
    void show_map()
    {

        // Lines to clear the teminal
        int x = 0, y = 10;
        clrscr();
        gotoxy(x, y);

        // Upper wall
        for (int i = 0; i < width + 2; i++)
        {
            cout << "#";
        }

        cout << "\n";

        // Left and right wall
        for (int i = 0; i < height; i++)
        {

            cout << "#";

            for (int j = 0; j < width; j++)
            {
                map[i][j].show();
                decay_pheromone_map(i, j);
            }

            cout << "#";
            cout << "\n";
        }

        // Down wall
        for (int i = 0; i < width + 2; i++)
        {
            cout << "#";
        }
        cout << "\n";
    }
};

/*
Space Structure
//  */
// struct space
// {
//     // Space dimension
//     int width;
//     int height;

//     vector<vector<space_unit>> map; // Matrix with space_unit

//     // ******************* CONSTRUCTOR **************************
//     space(int h_dimension, int w_dimension)
//     {
//         width = w_dimension;
//         height = h_dimension;

//         for (int i = 0; i < h_dimension; i++)
//         {
//             map.push_back(vector<space_unit>());
//             for (int j = 0; j < w_dimension; j++)
//             {
//                 map[i].push_back(*new space_unit());
//             }
//         }
//     };

//     // escrita
//     void set_ant_map(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         (*check_position(i, j)).set_ant();
//     } // Set an ant at (i,j) position in the space
//     void remove_ant_map(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         (*check_position(i, j)).remove_ant();
//     } // Remove an ant at (i,j) position
//     void set_pheromone_map(int i, int j, int quantity)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         (*check_position(i, j)).set_pheromone(quantity);
//     } // Set pheromone to terminal visualizationat position (i,j)
//     void decay_pheromone_map(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         (*check_position(i, j)).decay_pheromone();
//     } // Remove a pheromone at (i,j) position
//     void set_anthill_map(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         (*check_position(i, j)).set_anthill();
//     } // Set anthill to terminal visualization at position (i,j)
//     void remove_anthill_map(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         (*check_position(i, j)).remove_anthill();
//     } // Remove an anthill at (i,j) position

//     void set_phe_w_direction(int i, int j, int direction) {
//         (*check_position(i, j)).w_pheromone_food_direction = direction;
//     } // Remove an anthill at (i,j) position
//     void set_phe_h_direction(int i, int j, int direction) {
//         (*check_position(i, j)).w_pheromone_food_direction = direction;
//     } // Remove an anthill at (i,j) position

//     // leitura
//     bool check_food(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         return (*check_position(i, j)).has_food();
//     }
//     int check_phe_life(int i, int j)
//     {
//         const lock_guard<std::mutex> lock(TailMutex);
//         return (*check_position(i, j)).pheromone_life;
//     }

//     // void try_get_food(int i, int j) { (*check_position(i,j)).get_food(); }

//     // int w_phe_food_di(int i, int j) { (*check_position(i,j)); }
//     int h_phe_food_di(int i, int j) {
//         return (*check_position(i, j)).h_pheromone_food_direction;
//     }
//     int w_phe_food_di(int i, int j) {
//         return (*check_position(i, j)).w_pheromone_food_direction;
//         }

//     space_unit *check_position(int i, int j)
//     {
//         // const lock_guard<std::mutex> lock(TailMutex);
//         return &(map[i][j]);
//     }

//     // //***************************************** Update the terminal //*****************************************
//     void show_map()
//     {

//         // Lines to clear the teminal
//         int x = 0, y = 10;
//         clrscr();
//         gotoxy(x, y);

//         // Upper wall
//         for (int i = 0; i < width + 2; i++)
//         {
//             cout << "#";
//         }

//         cout << "\n";

//         // Left and right wall
//         for (int i = 0; i < height; i++)
//         {

//             cout << "#";

//             for (int j = 0; j < width; j++)
//             {
//                 map[i][j].show();
//                 decay_pheromone_map(i, j);
//             }

//             cout << "#";
//             cout << "\n";
//         }

//         // Down wall
//         for (int i = 0; i < width + 2; i++)
//         {
//             cout << "#";
//         }
//         cout << "\n";
//     }
// };
