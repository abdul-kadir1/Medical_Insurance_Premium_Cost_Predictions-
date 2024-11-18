create database health_insurance;
USE health_insurance;

CREATE TABLE insurance_data (
    age INT,
    sex INT,
    weight FLOAT,
    bmi FLOAT,
    no_of_dependents INT,
    smoker INT,
    diabetes INT,
    regular_ex INT,
    predicted_cost FLOAT
);
select * from insurance_data 