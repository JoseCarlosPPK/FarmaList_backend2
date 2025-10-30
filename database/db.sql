/* Table structure for Convocatoria */
CREATE TABLE Convocatoria (
  id int NOT NULL AUTO_INCREMENT,
  fecha_ini date NOT NULL,
  fecha_fin date NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY inicio_fin_unicos (fecha_ini, fecha_fin),
  CONSTRAINT fecha_fin_mayor_fecha_ini CHECK (fecha_fin > fecha_ini)
);


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


/* Table structure for Usuario */
CREATE TABLE Usuario (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(20) NOT NULL,
  password varchar(97) NOT NULL,
  correo varchar(50),
  permisos int DEFAULT 0 NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (nombre)
);


/* Table structure for Listado */
CREATE TABLE Listado (
  id_convocatoria int NOT NULL,
  id_centro int DEFAULT NULL,
  nombre varchar(60) NOT NULL,
  correo varchar(50) DEFAULT NULL,
  telefono varchar(9) DEFAULT NULL,
  movil varchar(9) DEFAULT NULL,
  direccion varchar(80) NOT NULL,
  localidad varchar(30) NOT NULL,
  provincia varchar(30) NOT NULL,
  cp varchar(6) NOT NULL,
  num_plazas int DEFAULT 1 NOT NULL,
  PRIMARY KEY (id_convocatoria, nombre, cp),
  CONSTRAINT fk_convocatoria_listado FOREIGN KEY (id_convocatoria) REFERENCES Convocatoria(id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_centro_listado FOREIGN KEY (id_centro) REFERENCES Centro(id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT num_plazas_positivo CHECK (num_plazas > 0)
);


/* Table structure for Listado_farmacias */
CREATE TABLE Listado_farmacias (
  id_convocatoria int NOT NULL,
  nombre varchar(60) NOT NULL,
  cp varchar(6) NOT NULL,
  PRIMARY KEY (id_convocatoria, nombre, cp),
  CONSTRAINT fk_listado_farmacias FOREIGN KEY (id_convocatoria, nombre, cp) REFERENCES Listado(id_convocatoria, nombre, cp) ON DELETE CASCADE ON UPDATE CASCADE
);


/* Table structure for Listado_farmacias_hospitalarias */
CREATE TABLE Listado_farmacias_hospitalarias (
  id_convocatoria int NOT NULL,
  nombre varchar(60) NOT NULL,
  cp varchar(6) NOT NULL,
  PRIMARY KEY (id_convocatoria, nombre, cp),
  CONSTRAINT fk_listado_farmacias_hospitalarias FOREIGN KEY (id_convocatoria, nombre, cp) REFERENCES Listado(id_convocatoria, nombre, cp) ON DELETE CASCADE ON UPDATE CASCADE
);


/* Table structure for Tutoriza_listado */
CREATE TABLE Tutoriza_listado (
  id_persona int NOT NULL,
  id_convocatoria int NOT NULL,
  nombre varchar(60) NOT NULL,
  cp varchar(6) NOT NULL,
  PRIMARY KEY(id_persona, id_convocatoria, nombre, cp),
  CONSTRAINT fk_id_persona_listado FOREIGN KEY (id_persona) REFERENCES Persona(id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_listado FOREIGN KEY (id_convocatoria, nombre, cp) REFERENCES Listado(id_convocatoria, nombre, cp) ON DELETE CASCADE ON UPDATE CASCADE
);
