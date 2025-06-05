CREATE DATABASE pragma;

CREATE TABLE pragma.transactions (
   `time` date DEFAULT NULL,
   `price` int DEFAULT NULL,
   `user_id` int DEFAULT NULL
 );

 CREATE TABLE IF NOT EXISTS pragma.transactions_stats (
    id INT PRIMARY KEY DEFAULT 1,
    total_count INT DEFAULT 0,
    total_sum DOUBLE DEFAULT 0,
    total_min DOUBLE DEFAULT NULL,
    total_max DOUBLE DEFAULT NULL
);
INSERT IGNORE INTO pragma.transactions_stats (id) VALUES (1);
 
