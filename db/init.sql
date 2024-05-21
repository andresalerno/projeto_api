CREATE DATABASE IF NOT EXISTS CSVRegister;
USE CSVRegister;

/* CREATE TABLE IF NOT EXISTS RegistroIndividual (
id_reg int primary key not null auto_increment,
dia_reg varchar(7) not null,
data_reg date not null,
hora_reg time not null,
umidade_solo_reg double not null,
umidade_ambiente_reg double not null,
temperatura_reg double not null,
volume_reg double not null
); */



CREATE TABLE IF NOT EXISTS Estufa(
    est_dh datetime not null,
    est_um_solo double not null,
    est_um_amb double not null,
    est_temp double not null,
    est_vol_aq double not null
);