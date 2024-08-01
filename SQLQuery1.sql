CREATE TABLE Temperaturas (
    Ciudad NVARCHAR(100),
    Fecha DATE,
    TemperaturaMax DECIMAL(5, 2),
    TemperaturaMin DECIMAL(5, 2)
);

INSERT INTO Temperaturas (Ciudad, Fecha, TemperaturaMax, TemperaturaMin) VALUES
('Buenos Aires', '2024-07-01', 22.5, 14.3),
('Córdoba', '2024-07-01', 24.1, 12.8),
('Mendoza', '2024-07-01', 20.4, 10.2),
('Rosario', '2024-07-01', 23.0, 15.1),
('Tucumán', '2024-07-01', 25.5, 16.2);

