
drop table if exists formigueiro;
drop table if exists cenario;

CREATE TABLE cenario (
  id_cenario SERIAL PRIMARY KEY NOT null,
  status VARCHAR(100) NOT NULL,
  tempo_execucao float,
  quantidade_total_comida INTEGER 
);  

CREATE TABLE formigueiro(
	id_formigueiro integer primary key not null,
    quantidade_comida INTEGER,
    quantidade_formiga_carregando INTEGER,
    quantidade_formiga_procurando INTEGER,
    maximo_carregado_formiga INTEGER,
    id_cenario integer,
    foreign key(id_cenario) references cenario(id_cenario)
);
