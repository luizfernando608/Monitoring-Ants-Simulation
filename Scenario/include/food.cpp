

struct food
{
    int max_quantity;
    int current_quantity = 0;
    int replacement_rate;

    // constructor
    food(int int_quantity, int rep_rate){
        current_quantity = int_quantity;
        max_quantity = int_quantity;
        replacement_rate = rep_rate;
    }

    void update(){
        // for (int i = 0; i < (*current_map).map[h_position][w_position].ant_number; i++)
        // {
        //     decay_quantity();
        //     if(current_quantity<=0){
        //         reset_quantity();
        //         break;
        //     }
        // }
        
    }

    void decay_quantity(){current_quantity = current_quantity - 1;}
    void reset_quantity(){current_quantity = max_quantity;}

};