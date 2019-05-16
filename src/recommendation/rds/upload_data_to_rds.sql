-- show all databases
-- SHOW databases;

-- create DB 'Flex_ads' and use it 
-- CREATE DATABASE Flex_ads;
-- USE Flex_ads;

-- create table for aisles.csv 
-- Applying to other data too ! 
CREATE TABLE aisles(
   aisle_id INT(4),
   aisle VARCHAR(32),
   PRIMARY KEY (aisle_id)
   );
   
   
-- upload aisles.csv to aisles TABLE
-- use local file directory, ignoring csv's header
LOAD DATA LOCAL INFILE '/Users/jisoo/Downloads/instacart-market-basket-analysis/aisles.csv' INTO TABLE aisles FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
   
