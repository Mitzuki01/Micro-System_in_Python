create database contato;

use contato;


create table contato(
	id INT NOT NULL auto_increment primary key,
    nome VARCHAR(150),
    email VARCHAR(150),
    telefone VARCHAR(11),
    tipoTelefone VARCHAR(12)
);