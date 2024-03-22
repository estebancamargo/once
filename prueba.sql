CREATE DATABASE IF NOT EXISTS Agenda777;
USE Agenda777;

CREATE TABLE personas (
    idper INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombreper VARCHAR(60) NOT NULL,
    apellidoper VARCHAR(60) NOT NULL,
    emailper VARCHAR(60) NOT NULL,
    dirper VARCHAR(60) NOT NULL,
    telper VARCHAR(60) NOT NULL,
    usuarioper VARCHAR(60) NOT NULL,
    contraper VARCHAR(255) NOT NULL,
    roles VARCHAR(20) NOT NULL,
    userId INT UNIQUE NOT NULL
);

CREATE TABLE canciones (
    idCan INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(60) NOT NULL,
    artista VARCHAR(60) NOT NULL,
    genero VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion VARCHAR(10) NOT NULL,
    Alanzamiento DATE NOT NULL,
    img BLOB,
    id_cancion VARCHAR(36) UNIQUE NOT NULL
);

CREATE TABLE compras (
    pk_id_compra INT AUTO_INCREMENT PRIMARY KEY,
    fechaCompra DATE NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    userId INT NOT NULL,
    id_cancion INT NOT NULL,
    mPago VARCHAR(50) NOT NULL,
    FOREIGN KEY (userId) REFERENCES personas(userId),
    FOREIGN KEY (id_cancion) REFERENCES canciones(idCan)
);




describe canciones;
select * from canciones;	

describe personas;
select * from personas;
delete from personas;

SELECT compras.pk_id_compra, compras.fechaCompra, compras.precio AS precio_compra, personas.nombreper, personas.apellidoper, canciones.titulo, compras.mPago 
FROM compras 
INNER JOIN personas ON compras.userId = personas.userId 
INNER JOIN canciones ON compras.id_cancion = canciones.idCan;

    userId INT UNIQUE NOT NULL
);

CREATE TABLE canciones (
    idCan INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(60) NOT NULL,
    artista VARCHAR(60) NOT NULL,
    genero VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion VARCHAR(10) NOT NULL,
    Alanzamiento DATE NOT NULL,
    img BLOB,
    id_cancion VARCHAR(36) UNIQUE NOT NULL
);

CREATE TABLE compras (
    pk_id_compra INT AUTO_INCREMENT PRIMARY KEY,
    fechaCompra DATE NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    userId INT NOT NULL,
    id_cancion INT NOT NULL,
    mPago VARCHAR(50) NOT NULL,
    FOREIGN KEY (userId) REFERENCES personas(userId),
    FOREIGN KEY (id_cancion) REFERENCES canciones(idCan)
);




describe canciones;
select * from canciones;	

describe personas; 
select * from personas;
delete from personas;

SELECT compras.pk_id_compra, compras.fechaCompra, compras.precio AS precio_compra, personas.nombreper, personas.apellidoper, canciones.titulo, compras.mPago 
FROM compras 
INNER JOIN personas ON compras.userId = personas.userId 
INNER JOIN canciones ON compras.id_cancion = canciones.idCan;



