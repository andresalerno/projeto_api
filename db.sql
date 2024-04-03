create database db;
use db;

create table task (
id int auto_increment primary key,
description varchar(255) not null,
due_date date,
status ENUM('peding', 'completed') default 'peding'
);