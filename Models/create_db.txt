CREATE TABLE scenario(
  ID varchar(36) NOT NULL,
  ants_quantity INT NOT NULL,
  total_food INT NOT NULL,
  map_food INT NOT NULL,
  elapsed FLOAT NOT NULL,
  status VARCHAR(30) NOT NULL,
  PRIMARY KEY (ID) );
 

CREATE TABLE anthill
(
  ID VARCHAR(2) NOT NULL,
  food_quantity INT NOT NULL,
  scenario_id varchar(36) NOT NULL,
  FOREIGN KEY (scenario_id) REFERENCES scenario(ID),
  PRIMARY KEY (ID, scenario_id)
);


CREATE TABLE ant
(
  ID SERIAL NOT NULL,
  scenario_id varchar(36) not null,
  anthill_id VARCHAR(2) not null,
  status varchar(30) NOT NULL,
  total_food INT NOT NULL,
  primary key (ID, scenario_id,anthill_id),
  FOREIGN KEY (scenario_id, anthill_id) REFERENCES anthill(scenario_id,ID)
);



select * from scenario s ;
select * from anthill a ;
select * from ant a ;