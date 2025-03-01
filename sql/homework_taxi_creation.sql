-- Active: 1740832533975@@ich-edit.edu.itcareerhub.de@3306@111124_Starodubov_Taxi
create table Vehicles (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Production_year int,
    Model varchar(30),
    Plate_number varchar(10),
    Color char(6),
    VIN varchar (30),
    Class char(10)
);

create table Drivers (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Vehicle_id int UNIQUE,
    Foreign Key (Vehicle_id) REFERENCES Vehicles(ID),
    First_name varchar(30),
    Last_name varchar(30),
    Driver_license varchar (30),
    Phone_number int,
    DOB date,
    Rating decimal (3,2),
    Hire_date date,
    Salary decimal (20 ,2)
);

create table Reviews (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Rating int,
    Comment varchar (1000),
    Review_date datetime
);

create table Clients(
    ID int PRIMARY KEY AUTO_INCREMENT,
    First_name varchar (50),
    Last_name varchar (50),
    DOB datetime,
    Gender char(1),
    Phone_number int,
    Email varchar (50)
);

create table Tarifs(
    ID int PRIMARY KEY AUTO_INCREMENT,
    Class varchar (20),
    Coefficient decimal (4, 2)
);

create table Companies (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Name varchar (20),
    Location varchar (255)
);

create table Orders (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Price decimal,
    Client_id int,
    Foreign Key (Client_id) REFERENCES Clients(ID),
    Start_point_long decimal (15, 12),
    Start_point_lat decimal (15, 12),
    End_point_long decimal (15, 12),
    End_point_lat decimal (15, 12),
    Driver_id int,
    Foreign Key (Driver_id) REFERENCES Drivers(ID),
    Start_date datetime,
    End_date datetime,
    Distance decimal,
    Review_id int,
    Foreign Key (Review_id) REFERENCES Reviews(ID),
    Tarif_id int,
    Foreign Key (Tarif_id) REFERENCES Tarifs(ID),
    Order_type int,
    Status int,
    Companies_id int,
    Foreign Key (Companies_id) REFERENCES Companies(ID)
);