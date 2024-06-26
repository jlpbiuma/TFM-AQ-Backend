-- SQL to create the required tables with uppercase column names

-- Table for ESTACIONES
CREATE TABLE ESTACIONES (
    ID_ESTACION INT AUTO_INCREMENT PRIMARY KEY,
    ID_ADMINISTRADOR INT NOT NULL,
    NOMBRE VARCHAR(255) NOT NULL,
    LOCALIZACION VARCHAR(255) NOT NULL,
    IP_GATEWAY VARCHAR(50),
    IP_LOCAL VARCHAR(50),
    FECHA_HORA_IP TIMESTAMP
);

-- Table for ESTACIONES_DISPOSITIVOS (assuming many-to-many relationship between ESTACIONES and DISPOSITIVOS)
CREATE TABLE ESTACIONES_DISPOSITIVOS (
    ID_ESTACION INT NOT NULL,
    ID_DISPOSITIVO VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID_ESTACION, ID_DISPOSITIVO),
    FOREIGN KEY (ID_ESTACION) REFERENCES ESTACIONES(ID_ESTACION)
);

-- Table for ESTACIONES_USUARIOS (assuming many-to-many relationship between ESTACIONES and USUARIOS)
CREATE TABLE ESTACIONES_USUARIOS (
    ID_ESTACION INT NOT NULL,
    ID_USUARIO VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID_ESTACION, ID_USUARIO),
    FOREIGN KEY (ID_ESTACION) REFERENCES ESTACIONES(ID_ESTACION)
);

CREATE TABLE MAGNITUDES (
    ID_MAGNITUD INT AUTO_INCREMENT PRIMARY KEY,
    MAGNITUD VARCHAR(50) NOT NULL,
    DESCRIPCION VARCHAR(50) NOT NULL,
    ESCALA VARCHAR(50)
);

CREATE TABLE ESTACIONES_MAGNITUDES (
    ID_ESTACION INT NOT NULL,
    ID_MAGNITUD INT NOT NULL,
    PRIMARY KEY (ID_ESTACION, ID_MAGNITUD),
    FOREIGN KEY (ID_ESTACION) REFERENCES ESTACIONES(ID_ESTACION),
    FOREIGN KEY (ID_MAGNITUD) REFERENCES MAGNITUDES(ID_MAGNITUD)
);

-- Table for MEDIDA
CREATE TABLE MEDIDAS (
    ID_MEDIDA INT AUTO_INCREMENT PRIMARY KEY,
    ID_MAGNITUD INT NOT NULL,
    ID_ESTACION INT NOT NULL,
    VALOR DOUBLE PRECISION NOT NULL,    
    FECHA_HORA TIMESTAMP NOT NULL,
    FOREIGN KEY (ID_MAGNITUD) REFERENCES MAGNITUDES(ID_MAGNITUD),
    FOREIGN KEY (ID_ESTACION) REFERENCES ESTACIONES(ID_ESTACION)
);

-- Table for LOGS
CREATE TABLE LOGS (
    ID_LOG INT AUTO_INCREMENT PRIMARY KEY,
    ENDPOINT VARCHAR(255) NOT NULL,
    METHOD VARCHAR(10) NOT NULL,
    STATUS_CODE INT NOT NULL,
    IP_ADDRESS VARCHAR(50),
    TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    REQUEST_BODY TEXT,
    RESPONSE_BODY TEXT
);
