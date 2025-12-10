/* Table structure for Centro */
CREATE TABLE Centro (
   id int NOT NULL AUTO_INCREMENT,
   nombre varchar(60) NOT NULL,
   correo varchar(50) DEFAULT NULL,
   telefono varchar(9) DEFAULT NULL,
   movil varchar(9) DEFAULT NULL,
   direccion varchar(80) NOT NULL,
   localidad varchar(30) NOT NULL,
   provincia varchar(30) NOT NULL,
   cp varchar(6) NOT NULL,
   PRIMARY KEY (id),
   UNIQUE KEY centro_unico (nombre, cp)
);


/* Table structure for Farmacia */
CREATE TABLE Farmacia (
   id int NOT NULL,
   PRIMARY KEY (id),
   CONSTRAINT fk_id_farmacia FOREIGN KEY (id) REFERENCES Centro(id) ON DELETE CASCADE ON UPDATE CASCADE
);


/* Table structure for Farmacia_hospitalaria */
CREATE TABLE Farmacia_hospitalaria (
   id int NOT NULL,
   PRIMARY KEY (id),
   CONSTRAINT fk_id_far_hospitalaria FOREIGN KEY (id) REFERENCES Centro(id) ON DELETE CASCADE ON UPDATE CASCADE
);


/* Table structure for Persona */
CREATE TABLE Persona (
   id int NOT NULL AUTO_INCREMENT,
   nombre varchar(60) NOT NULL,
   PRIMARY KEY(id),
   CONSTRAINT nombre_no_vacio CHECK (nombre != '')
);


/* Table structure for Tutoriza */
CREATE TABLE Tutoriza (
   id_persona int NOT NULL,
   id_centro int NOT NULL,
   PRIMARY KEY(id_persona, id_centro),
   CONSTRAINT fk_id_persona FOREIGN KEY (id_persona) REFERENCES Persona(id) ON DELETE CASCADE ON UPDATE CASCADE,
   CONSTRAINT fk_id_centro FOREIGN KEY (id_centro) REFERENCES Centro(id) ON DELETE CASCADE ON UPDATE CASCADE
);


/* Table structure for Listado_fechas */
CREATE TABLE Listado_fechas (
   id int NOT NULL AUTO_INCREMENT,
   fecha_ini date NOT NULL,
   fecha_fin date NOT NULL,
   PRIMARY KEY (id),
   UNIQUE KEY inicio_fin_unicos (fecha_ini, fecha_fin),
   CONSTRAINT fecha_fin_mayor_fecha_ini CHECK (fecha_fin > fecha_ini)
);



/* Table structure for Listado_farmacias */
CREATE TABLE Listado_farmacias (
   id_fecha int NOT NULL,
   id_centro int NOT NULL,
   PRIMARY KEY (id_fecha, id_centro),
   CONSTRAINT fk_id_fecha FOREIGN KEY (id_fecha) REFERENCES Listado_fechas(id) ON DELETE CASCADE,
   CONSTRAINT fk_id_farmacia FOREIGN KEY (id_centro) REFERENCES Farmacia(id) ON DELETE CASCADE
);


/* Table structure for Listado_farmacias_hospitalarias */
CREATE TABLE Listado_farmacias_hospitalarias (
   id_fecha int NOT NULL,
   id_centro int NOT NULL,
   PRIMARY KEY (id_fecha, id_centro),
   CONSTRAINT fk_id_fecha FOREIGN KEY (id_fecha) REFERENCES Listado_fechas(id) ON DELETE CASCADE,
   CONSTRAINT fk_id_farmacia_hospitalaria FOREIGN KEY (id_centro) REFERENCES Farmacia_hospitalaria(id) ON DELETE CASCADE
);



/* Table structure for Usuario */
CREATE TABLE Usuario (
   id int NOT NULL AUTO_INCREMENT,
   nombre varchar(20) NOT NULL,
   password varchar(97) NOT NULL, /* tamaño hash según algoritmo Argon2 */
   correo varchar(50),
   PRIMARY KEY (id),
   UNIQUE KEY (nombre)
);