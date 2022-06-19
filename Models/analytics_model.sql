CREATE TABLE scenario
(
  ID VARCHAR(36) NOT NULL unique,
  anthill_id VARCHAR(2) NOT NULL,
  ants_id SERIAL NOT NULL,
  ants_searching FLOAT NOT NULL,
  ants_carring FLOAT NOT NULL,
  total_food INT NOT NULL,
  anthill_food FLOAT NOT NULL,
  trafic_food FLOAT NOT NULL,
  elapsed FLOAT NOT NULL,
  prob_win FLOAT NOT NULL,
  PRIMARY KEY (ID)
);


CREATE TABLE Global
(
  num_scenarios INT NOT NULL,
  num_anthills INT NOT NULL,
  num_ants INT NOT NULL,
  ants_searching FLOAT NOT NULL,
  ants_carring FLOAT NOT NULL,
  total_food INT NOT NULL,
  map_food FLOAT NOT NULL,
  anthill_food FLOAT NOT NULL,
  trafic_food FLOAT NOT NULL,
  mean_executing_time FLOAT NOT NULL,
  min_time_scenario VARCHAR(36) NOT NULL,
  min_time_time FLOAT NOT NULL,
  max_time_scenairio VARCHAR(36) NOT NULL,
  max_time_time FLOAT NOT NULL,
  mean_food_stored_per_ant INT NOT NULL,
  max_food_stored INT NOT NULL
);